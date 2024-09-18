from fastapi import APIRouter
from .endpoints import careers,article_files,pro_Series,dashboard,dropdown,report,login, media_files,user,masters,brand_campaigns,cms_settings,notification,article


api_router = APIRouter()

api_router.include_router(pro_Series.router, prefix="/pro_stories",tags=["ProStories"])
api_router.include_router(article_files.router, tags=["ArticleFiles"])
api_router.include_router(careers.router, tags=["Carreers"])
api_router.include_router(dashboard.router, tags=["Dashboard"])
api_router.include_router(report.router, tags=["Report"])
api_router.include_router(dropdown.router, tags=["Dropdown"])
api_router.include_router(login.router, tags=["Login"])

api_router.include_router(user.router ,tags=["User"])

api_router.include_router(masters.router ,prefix="/master",tags=["Masters"])

api_router.include_router(media_files.router ,prefix="/media_files", tags=["Media Files"])
api_router.include_router(brand_campaigns.router,prefix="/brand_campaigns",tags=["Brand Campaigns"])
api_router.include_router(cms_settings.router ,prefix="/cms_settings",tags=["CMS Settings"])
api_router.include_router(notification.router ,prefix="/notification" , tags=["Notification"])
api_router.include_router(article.router ,prefix="/article" ,tags=["Article"])