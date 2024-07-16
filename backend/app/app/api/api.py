from fastapi import APIRouter
from .endpoints import login, media_files,user,masters,brand_campaigns,cms_settings


api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])

api_router.include_router(user.router ,prefix="/user", tags=["User"])

api_router.include_router(masters.router ,prefix="/masters", tags=["Masters"])

api_router.include_router(media_files.router ,prefix="/media_files", tags=["Media Files"])
api_router.include_router(brand_campaigns.router ,prefix="/brand_campaigns", tags=["Brand Campaigns"])
api_router.include_router(cms_settings.router ,prefix="/cms_settings", tags=["CMS Settings"])