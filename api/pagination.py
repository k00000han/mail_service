from fastapi import Query
from fastapi_pagination import Page

Page = Page.with_custom_options(
    size=Query(20, ge=1, le=20),
)
