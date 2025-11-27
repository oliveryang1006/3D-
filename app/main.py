from fastapi import FastAPI

from .api import admin, member, merchant, preview

app = FastAPI(title="苏宁银河国际酒店电子会员管理系统")


@app.get("/health")
def health_check():
    return {"status": "ok"}


def include_routes(application: FastAPI) -> None:
    application.include_router(admin.router)
    application.include_router(merchant.router)
    application.include_router(member.router)
    application.include_router(preview.router)


include_routes(app)
