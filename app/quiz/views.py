from aiohttp_apispec import querystring_schema, request_schema, response_schema
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest

from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data['title']
        if self.store.quizzes.get_theme_by_title(title):
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeSchema().dump(themes))



class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        title = self.data['title']
        theme_id = self.data['theme_id']
        theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme:
            raise HTTPNotFound
        answers = self.data['answers']
        if len(answers) == 1:
            raise HTTPBadRequest
        if not any(answer['is_correct'] == False for answer in answers) or not any(
                answer['is_correct'] == True for answer in answers):
            raise HTTPBadRequest
        question = await self.store.quizzes.create_question(title=title, theme_id=self.data['theme_id'],
                                                            answers=answers)
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.quizzes.list_questions()
        return json_response(data=QuestionSchema().dump(questions))
