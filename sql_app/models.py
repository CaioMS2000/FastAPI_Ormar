import sqlalchemy
import databases
import ormar
from ormar import property_field
from datetime import  datetime
from .database import database, metadata

class MetaMeta():
    database = database
    metadata = metadata


class User(ormar.Model):
    class Meta(MetaMeta):
        tablename: str = "users"
        constraints = [ormar.UniqueColumns("id", "nickname"), ormar.IndexColumns("id", "nickname")]
    
    id: int = ormar.Integer(primary_key=True)
    nickname: str = ormar.String(max_length=20)
    password: str = ormar.String(max_length=256)
    nick_color: str = ormar.String(max_length=7, default = "#000000")
    reg_date: datetime = ormar.DateTime(default = datetime.now)


class Message(ormar.Model):
    class Meta(MetaMeta):
        tablename: str = "messages"
        constraints = [ormar.UniqueColumns("id"), ormar.IndexColumns("id", "owner_id")]
    
    id: int = ormar.Integer(primary_key=True)
    content: str = ormar.String(max_length=500)
    sent_date: datetime = ormar.DateTime(default = datetime.now)
    deleted: bool = ormar.Boolean(default = False)
    owner:Optional[User] = ormar.ForeignKey(User)
    owner_id: int = ormar.Integer(default = owner.id | None)

    @property_field
    def num_char(self):
        return len(self.content)

    # __tablename__ = "message"
    # id = Column(Integer, Sequence('id', start=1, increment=1), primary_key=True, index=True)
    # content = Column(String(500))
    # num_char = Column(Integer, default = 0)
    # sent_date = Column(DateTime, default = datetime.now())
    # deleted = Column(Boolean, default = False)
    # owner_id = Column(Integer, ForeignKey('user.id'))
    # owner = relationship("User", back_populates = "messages")


# class Course(ormar.Model):
#     class Meta:
#         database = database
#         metadata = metadata

#     id: int = ormar.Integer(primary_key=True)
#     name: str = ormar.String(max_length=100)
#     completed: bool = ormar.Boolean(default=False)