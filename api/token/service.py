from abc import ABC


from common.models import WorkEmail
from common.db_service import EntityService
from api.schemas import ID
from .schemas import TokenSchema


class TokenService(EntityService[WorkEmail, TokenSchema], ABC):
    model = WorkEmail
    schema = TokenSchema

    async def create_or_update_token(self, token_id: ID, token_data: TokenSchema) -> TokenSchema:
        token = await self.get_item(token_id, raise_exception=False)
        if token is None:
            return await self.create_item(token_data)
        else:
            await self.update_item(token_id, token_data)
        return token

    async def update_token(self, pk: ID, token: str) -> TokenSchema:
        # Получить объект WorkEmail по его ID
        email = await self.get_item(pk)

        # Обновить токен в записи WorkEmail
        email.token = token

        # Сохранить обновленную запись
        updated_email = await self.update_item(pk, email)

        return updated_email
