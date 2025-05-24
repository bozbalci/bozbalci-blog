from ninja import ModelSchema, Schema
from pydantic import Field
from wagtail.images.models import AbstractRendition

from notcms.blog.models import BlogPostPage, NowPostPage


class HealthResponse(Schema):
    motd: str


class RenditionSchema(ModelSchema):
    url: str = Field(None, alias="file.url")
    alt: str = Field(None, alias="alt")

    class Config:
        model = AbstractRendition
        model_fields = ["width", "height"]


class BlogPostSchema(ModelSchema):
    url: str = Field(None, alias="get_full_url")

    class Config:
        model = BlogPostPage
        model_fields = ["title", "date", "intro"]


class NowPostSchema(ModelSchema):
    url: str = Field(None, alias="get_full_url")

    class Config:
        model = NowPostPage
        model_fields = ["title", "date"]
