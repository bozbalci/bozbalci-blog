from ninja import Router
from ninja.pagination import paginate

from notcms.blog.models import BlogPostPage, NowPostPage
from notcms.blog.schemas import BlogPostSchema, HealthResponse, NowPostSchema

default_router = Router()


@default_router.get("/health", response=HealthResponse)
def health(request):
    return HealthResponse(motd="bozbalci API is healthy")


router = Router()


@router.get("/posts", response=list[BlogPostSchema])
@paginate
def get_blog_posts(request):
    return BlogPostPage.objects.live().order_by("-first_published_at")


@router.get("/now", response=NowPostSchema)
def get_the_last_now_post(request):
    return NowPostPage.objects.live().order_by("-first_published_at").first()


@router.get("/then", response=list[NowPostSchema])
@paginate
def get_all_now_posts(request):
    return NowPostPage.objects.live().order_by("-first_published_at")
