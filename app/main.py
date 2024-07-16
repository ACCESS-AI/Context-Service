from app.model.output_adapter.posgres_stats_orm import initialize_database
from fastapi import FastAPI
from app.routers.context_router import context_router

app = FastAPI()
initialize_database()
app.include_router(router=context_router)




