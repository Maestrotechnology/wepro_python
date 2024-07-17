from fastapi import APIRouter
from .endpoints import dashboard,dropdown,login, media_files,user,masters,brand_campaigns,cms_settings,notification,article


api_router = APIRouter()

api_router.include_router(dashboard.router, tags=["Dashboard"])
api_router.include_router(dropdown.router, tags=["Dropdown"])
api_router.include_router(login.router, tags=["Login"])

api_router.include_router(user.router , tags=["User"])

api_router.include_router(masters.router ,tags=["Masters"])

api_router.include_router(media_files.router , tags=["Media Files"])
api_router.include_router(brand_campaigns.router , tags=["Brand Campaigns"])
api_router.include_router(cms_settings.router , tags=["CMS Settings"])
api_router.include_router(notification.router , tags=["Notification"])
api_router.include_router(article.router , tags=["Article"])