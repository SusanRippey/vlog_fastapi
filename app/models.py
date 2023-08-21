from sqlalchemy import Boolean, Column, Integer, String,TIMESTAMP,text,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    # Foreign key constraints
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="cascade"),nullable=False)
    # relationship constraints
    owner = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    phone_no = Column(String, nullable=False)
    # Establish the reverse relationship with the "posts" attribute
    posts = relationship("Post", back_populates="owner")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="cascade"), primary_key=True)
