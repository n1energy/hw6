from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        admin = await self.store.admins.get_by_email(self.data['email'])
        if not admin or not admin.is_password_valid(self.data['password']):
            raise HTTPForbidden
        admin_json = AdminSchema().dump(admin)
        # session['admin'] = admin_json
        return json_response(data=admin_json)


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        if self.request.admin:
            return json_response(data=AdminSchema().dump(self.request.admin))
        raise HTTPUnauthorized
