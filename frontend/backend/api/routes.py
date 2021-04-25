import random
from functools import wraps

import sanic.response
from bson.json_util import dumps
from sanic_openapi import doc, swagger_blueprint

from api.blueprints import authentication_blueprint
from api.models import UserModel, ItemModel
from database.database import get_books, get_events, get_clubs
from database.entities import User, Book
from ml.inference_nlp import get_rec


async def check_request_for_authorization_status(request):
    cookie = request.cookies.get("login_token")
    user = await User.find_one({"salt": cookie})
    if user:
        request.args["username"] = user.username
        return True
    else:
        return False


def authorized(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        # run some method that checks the request
        # for the client's authorization status
        is_authorized = await check_request_for_authorization_status(request)

        if is_authorized:
            # the user is authorized.
            # run the handler method and return the response
            response = await f(request, *args, **kwargs)
            return response
        else:
            # the user is not authorized.
            return sanic.response.json({'ok': False, "data": "Not authorized"}, 403)

    return decorated_function


async def initialize_routes(app):
    app.blueprint(swagger_blueprint)

    @app.route("/")
    @doc.exclude(True)
    async def root_handler(request):
        return sanic.response.json({"ok": True, "data": "Everything should work now!"})

    @app.get("/items/get")
    @doc.summary("Get items for user")
    @doc.description("Get all items for given user. User must be authorized to get theirs items.")
    @doc.response(200, {"ok": bool, "data": doc.List(ItemModel)}, description="Valid response")
    @authorized
    async def items_get(request):
        username = request.args.get("username")
        user = await User.find_one({"username": username})
        books = [(await Book.find_one({"model_id": x})).title
                 for x in user.books]
        ml_response = {
            "books": get_rec('./ml/dataset/books_fin.csv', 'title', 'title',
                             books),
            "clubs": get_rec('./ml/dataset/clubs_fin.csv', 'event_name', 'description',
                             books),
            "events": get_rec('./ml/dataset/events_fin.csv', 'event_name', 'description',
                              books)
        }
        items = await get_books(ml_response["books"]) + await get_clubs(ml_response["clubs"]) + await get_events(ml_response["events"])
        response = sanic.response.json({"ok": True, "data": items}, dumps=dumps)
        return response

    @app.get("/items/get/<username>")
    @doc.summary("Get items for user")
    @doc.description("Get all items for given user.")
    @doc.response(200, {"ok": bool, "data": doc.List(ItemModel)}, description="Valid response")
    async def items_get_username(request, username):
        user = await User.find_one({"username": username})
        books = [(await Book.find_one({"model_id": x})).title
                 for x in user.books]
        ml_response = {
            "books": get_rec('./ml/dataset/books_fin.csv', 'title', 'title',
                             books),
            "clubs": get_rec('./ml/dataset/clubs_fin.csv', 'event_name', 'description',
                             books),
            "events": get_rec('./ml/dataset/events_fin.csv', 'event_name', 'description',
                              books)
        }
        items = await get_books(ml_response["books"]) + \
                await get_clubs(ml_response["clubs"]) + \
                await get_events(ml_response["events"])
        response = sanic.response.json({"ok": True, "data": items}, dumps=dumps)
        return response

    @authentication_blueprint.get('/login')
    @doc.summary("Login route")
    @doc.description('This is a login route to login in the system.')
    @doc.consumes(doc.String(name="username", description="The username of the user"), required=True)
    @doc.consumes(doc.String(name="password", description="The password of the user"), required=True)
    @doc.response(200, {"ok": bool}, description="Valid response")
    @doc.response(400, {"ok": bool, "data": str}, description="Invalid password")
    @doc.response(404, {"ok": bool, "data": str}, description="No such user exists")
    async def login(request):
        user = await User.find_one({"username": request.args.get("username")})
        if not user:
            response = sanic.response.json({"ok": False, "data": "No such user exists"})
            return response
        user_pass = hash(str(user.password))
        request_pass = hash(str(request.args.get("password")))
        if str(user_pass) == str(request_pass):
            response = sanic.response.json({"ok": True})
            response.cookies["login_token"] = user.salt
        else:
            response = sanic.response.json({"ok": False, "data": "Invalid password"})
        return response

    @authentication_blueprint.post("/register")
    @doc.summary("Register route")
    @doc.description('This is a register route to register in the system.')
    @doc.consumes(UserModel, content_type="application/json", location="body", required=True)
    @doc.response(200, {"ok": bool}, description="Valid response")
    @doc.response(400, {"ok": bool, "data": str}, description="Invalid password")
    @doc.response(409, {"ok": bool, "data": str}, description="This username already exists")
    async def register(request):
        does_user_exist = await User.find_one({"username": request.json["username"]})
        if not does_user_exist:
            user_salt = str(random.getrandbits(128))
            user = User(username=request.json["username"], password=request.json["password"], salt=user_salt)
            await user.commit()
            response = sanic.response.json({"ok": True})
            response.cookies["login_token"] = user_salt
            return response
        else:
            return sanic.response.json({"ok": False, "data": "This username already exists"})

    app.blueprint(authentication_blueprint)
