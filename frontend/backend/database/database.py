import logging

import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from sanic_mongodb_ext import MongoDbExtension

import database.entities as entities


async def upload():
    def csv_parser(path):
        df = pd.read_csv(path)
        return df

    club_df_raw = csv_parser("./data/clubs.csv")
    club_df_raw = club_df_raw.fillna(value="")
    for index, row in club_df_raw.iterrows():
        try:
            new_club = entities.Club(model_id=row.iloc[1], title=str(row.iloc[2]), description=str(row.iloc[3]))
            await new_club.commit()
        except Exception as e:
            logging.debug(e)

    event_df_raw = csv_parser("./data/events.csv")
    event_df_raw = event_df_raw.fillna(value="")
    for index, row in event_df_raw.iterrows():
        try:
            new_event = entities.Event(model_id=row.iloc[0], title=row.iloc[2], author=row.iloc[4], genre=row.iloc[8],
                                       tags=[row.iloc[9], row.iloc[23]], date=row.iloc[12], location=row.iloc[17],
                                       description=row.iloc[16])
            await new_event.commit()
        except Exception as e:
            logging.debug(e)

    books_df_raw = csv_parser("./data/books.csv")
    books_df_raw = books_df_raw.fillna(value="")
    for index, row in books_df_raw.iterrows():
        try:
            new_book = entities.Book(model_id=index, title=row["title"], author=row["author"],
                                     genre=row["genres"], tags=[row["age"]], published_date=row["date"])
            await new_book.commit()
        except Exception as e:
            logging.debug(e)


async def initialize_database(app):
    MongoDbExtension(app)

    client = AsyncIOMotorClient(app.config['MONGODB_URI'])
    database = client[app.config['MONGODB_DATABASE']]
    lazy_umongo = app.config["LAZY_UMONGO"]
    lazy_umongo.init(database)

    logging.debug("Initializing collections...")
    await entities.User.ensure_indexes()
    logging.debug("User document was initialized...")

    await entities.Book.ensure_indexes()
    logging.debug("Book document was initialized...")

    await entities.Club.ensure_indexes()
    logging.debug("Club document was initialized...")

    await entities.Event.ensure_indexes()
    logging.debug("Event document was initialized...")

    logging.debug("Collections were initialized!")

    # await upload()


async def get_books(book_ids):
    items = []
    for book_id in book_ids:
        book = await entities.Book.find_one({"model_id": book_id})
        if book:
            items.append(book.get_info())
    return items


async def get_clubs(club_ids):
    items = []
    for club_id in club_ids:
        club = await entities.Club.find_one({"model_id": club_id})
        if club:
            items.append(club.get_info())
    return items


async def get_events(event_ids):
    items = []
    for event_id in event_ids:
        event = await entities.Club.find_one({"model_id": event_id})
        if event:
            items.append(event.get_info())
    return items
