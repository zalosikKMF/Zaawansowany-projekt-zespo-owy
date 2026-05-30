import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.database import async_session, engine
from app.models import Base
from app.services.sync import run_sync

logger = logging.getLogger("clearair")
scheduler = AsyncIOScheduler()


async def scheduled_sync():
    async with async_session() as session:
        try:
            log = await run_sync(session)
            logger.info("Sync OK: fetched=%s saved=%s", log.records_fetched, log.records_saved)
        except Exception:
            logger.exception("Sync failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler.add_job(
        scheduled_sync,
        "interval",
        minutes=settings.sync_interval_minutes,
        id="sensor_sync",
        replace_existing=True,
    )
    scheduler.start()
    await scheduled_sync()

    yield

    scheduler.shutdown(wait=False)
    await engine.dispose()


app = FastAPI(
    title="ClearAir API",
    description="System monitorowania jakosci powietrza - Polska (Sensor.Community)",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
