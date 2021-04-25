from sanic_openapi import doc


class UserModel:
    username = doc.String("The name of your user account.")
    password = doc.String("The password of your user account.")


class AdditionalInformationModel:
    title = doc.String("Key of an additional information on the item.")
    data = doc.String("Additional information on the item.")


class ItemModel:
    picture = doc.String("The URL to the item's picture.")
    title = doc.String("Name of the item.")
    metatype = doc.String("Meta type of the item.")
    type = doc.String("Type of the item.")
    description = doc.String("Short description of the item.")
    tags = doc.List(doc.String("Tag for an item."))
    additional = doc.List(AdditionalInformationModel)
