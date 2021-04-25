from sanic import Sanic
from sanic_cors import CORS
from umongo import MotorAsyncIOInstance

app = Sanic(__name__)
CORS(app)

app.config.update({
    "MONGODB_DATABASE": "lct",
    "MONGODB_URI": "mongodb+srv://user:pass@cluster0.2cssf.mongodb.net/lct?retryWrites=true&w=majority",
    "LAZY_UMONGO": MotorAsyncIOInstance(),
})

app.config.update({
    "API_HOST": "135.181.109.111",
    "API_VERSION": "0.1.2",
    "API_TITLE": "DataPie Backend API",
    "API_DESCRIPTION": "An API for DataPie's hackathon project",
    "API_LICENSE_NAME": " ",
    "API_LICENSE_URL": " "
})

app.config.SWAGGER_UI_CONFIGURATION = {
    'validatorUrl': None,  # Disable Swagger validator
    'displayRequestDuration': True,
    'docExpansion': 'list'
}
