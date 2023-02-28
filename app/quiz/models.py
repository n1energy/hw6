from __future__ import annotations
from dataclasses import dataclass

from sqlalchemy import Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: int | None
    title: str


@dataclass
class Question:
    id: int | None
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"
    id = Column(BigInteger, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    questions = relationship("QuestionModel", back_populates="themes")

    def to_dataclass(self) -> Theme:
        return Theme(id=self.id, title=self.title)

class QuestionModel(db):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    theme_id = Column(BigInteger, ForeignKey("themes.id", ondelete="CASCADE"))
    themes = relationship("ThemeModel", back_populates="questions")


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(BigInteger, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    question_id = Column(BigInteger, ForeignKey("questions.id", ondelete="CASCADE"))
