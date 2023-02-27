from hashlib import sha256
import typing

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        await self.create_admin(email=self.app.config.admin.email, password=self.app.config.admin.password)
    
    async def get_by_email(self, email: str) -> Admin | None:
        async with self.app.database.session.begin() as s:
            query = select(AdminModel).where(AdminModel.email==email)
            admin = s.scalars(query)
            if admin:
                return admin

    async def create_admin(self, email: str, password: str) -> Admin:
        encoded_password = sha256(str(password).encode()).hexdigest()
        admin = AdminModel(email=email, password=encoded_password)
        async with self.app.database.session.begin() as s:
            s.add(admin)
            await s.commit
        return admin
