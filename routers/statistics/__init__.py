__all__ = ("router", )

from aiogram import Router
from .stat import router as stat_router

router = Router()

router.include_router(stat_router)