from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.api.deps import get_current_admin_user
from app.core.templates import templates

router = APIRouter()

@router.get("/activity", response_class=HTMLResponse)
async def admin_activity_dashboard(
    request: Request,
    # admin = Depends(get_current_admin_user),
):
    return templates.TemplateResponse(
        "admin/activity.html",
        {
            "request": request,
            # "admin": admin,
            "ws_url": "/ws/admin/activity",
        },
    )


@router.get("/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request},
    )
