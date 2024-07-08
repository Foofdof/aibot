from aiogram import Router
from .commands import router as commands_router
from .operations import router as operation_router
from .statistics import router as stat_router

router = Router(name=__name__)

router.include_router(commands_router)
router.include_router(operation_router)
router.include_router(stat_router)
