from ninja import NinjaAPI

from notcms.blog.api import router as blog_router
from notcms.music.api import router as music_router
from notcms.photo.api import router as photo_router
from notcms.schemas import HealthResponse

api = NinjaAPI(
    title="bozbalci API",
    version="2.0.0",
    description="""\
<p>This is the programmatic interface to my <strike>life</strike> website.</p>
<p>Use responsibly and with caution. I may introduce breaking changes at will!</p>""",
)

api.add_router("/blog/", blog_router, tags=["blog"])
api.add_router("/music/", music_router, tags=["music"])
api.add_router("/gallery/", photo_router, tags=["gallery"])


@api.get("/health", response=HealthResponse)
def health(request):
    return HealthResponse(motd="bozbalci API is healthy")
