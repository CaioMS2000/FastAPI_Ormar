import ormar
from ormar import property_field
from datetime import datetime
from .database import database, metadata


class MetaMeta():
    database = database
    metadata = metadata


class User(ormar.Model):
    class Meta(MetaMeta):
        tablename: str = "users"
        constraints = [ormar.UniqueColumns(
            "id", "nickname"), ormar.IndexColumns("id", "nickname")]

    id: int = ormar.Integer(primary_key=True)
    nickname: str = ormar.String(max_length=20)
    password: str = ormar.String(max_length=256)
    nick_color: str = ormar.String(max_length=7, default="#000000")
    reg_date: datetime = ormar.DateTime(default=datetime.now)


class Message(ormar.Model):
    class Meta(MetaMeta):
        tablename: str = "messages"
        constraints = [ormar.UniqueColumns("id"), ormar.IndexColumns("id")]

    id: int = ormar.Integer(primary_key=True)
    owner = ormar.ForeignKey(User)
    content: str = ormar.String(max_length=500)
    sent_date: datetime = ormar.DateTime(default=datetime.now)
    deleted: bool = ormar.Boolean(default=False)

    @property_field
    def num_char(self):
        return len(self.content)
