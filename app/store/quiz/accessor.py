from sqlalchemy import select
from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme, ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        async with self.app.database.session.begin() as s:
            theme = await s.add(ThemeModel(title=title))
            await s.commit()
        return theme.to_dataclass()

    async def get_theme_by_title(self, title: str) -> Theme | None:
        async with self.app.database.session.begin() as s:
            query = select(ThemeModel).where(ThemeModel.title == title)
            result = await s.execute(query)
            theme = result.scalars().first()
            if theme:
                return theme.to_dataclass()

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        async with self.app.database.session.begin() as s:
            query = select(ThemeModel).where(ThemeModel.id == id_)
            result = await s.execute(query)
            theme = result.scalars().first()
            if theme:
                return theme.to_dataclass()

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session.begin() as s:
            query = select(ThemeModel)
            result = await s.execute(query)
            themes = result.scalars().all()
            if themes:
                return [theme.to_dataclass() for theme in themes]

    async def create_answers(
        self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        raise NotImplemented

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        raise NotImplemented

    async def get_question_by_title(self, title: str) -> Question | None:
        raise NotImplemented

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        raise NotImplemented
