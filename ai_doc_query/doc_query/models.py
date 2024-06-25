import datetime
from mongoengine import *
from enum import Enum

class MessageType(Enum):
    USER = "user"
    BOT = "bot"


class User(Document):
    email = EmailField(required = True, unique = True)
    password = StringField(required=True)
    auth_token = StringField(reqiured = True)

    def __str__(self):
        return self.email
    


class Chat(Document):
    title = StringField(max_length=100, unique = True, required = True)
    creation_timestamp = DateTimeField(default=datetime.datetime.now())
    owner = ReferenceField(User , reverse_delete_rule=CASCADE)

    def __str__(self):
        return self.title



class Message(Document):
    msg_txt = StringField(min_length=1)
    creation_timestamp = DateTimeField(default = datetime.datetime.now())
    chat = ReferenceField(Chat, reverse_delete_rule=CASCADE)
    type = EnumField(MessageType , choices = [MessageType.USER , MessageType.BOT])

    def __str__(self):
        return self.msg_txt + " " + self.type
    

    
class File(Document):
    name = StringField(min_length=1 , max_length=20)
    chat = ReferenceField(Chat,reverse_delete_rule=CASCADE)
    file = FileField(required = True)

    def __str__(self):
        return self.name