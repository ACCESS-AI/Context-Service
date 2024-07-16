from typing import Dict, Union
from fastapi import APIRouter, BackgroundTasks

from app.services.context_service import ContextService

context_service = ContextService()
context_router = APIRouter()

@context_router.put("/contexts/create")
async def create_context(payload: Union[Dict, None], background_tasks: BackgroundTasks):
    return context_service.create_context(background_tasks=background_tasks, payload=payload)


@context_router.get("/contexts/{course_slug}/status")
async def get_context(course_slug: str): 
    return context_service.get_context(course_slug=course_slug)