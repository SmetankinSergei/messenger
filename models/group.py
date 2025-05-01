from sqlalchemy import Column, Integer, ForeignKey, Table, String
from sqlalchemy.orm import relationship

from db.database import Base


group_members = Table(
    "group_members", Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True)
)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))

    members = relationship("User", secondary=group_members, backref="groups")
