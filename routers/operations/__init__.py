__all__ = ("router", )

from aiogram import Router

from .operations import router as operations_router

router = Router()

router.include_router(operations_router)