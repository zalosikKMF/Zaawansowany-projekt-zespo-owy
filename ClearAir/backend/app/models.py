from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    latitude: Mapped[float] = mapped_column(Numeric(10, 7))
    longitude: Mapped[float] = mapped_column(Numeric(10, 7))
    altitude: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    country: Mapped[str] = mapped_column(String(2), default="PL")
    indoor: Mapped[bool] = mapped_column(Boolean, default=False)
    exact_location: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    sensors: Mapped[list["Sensor"]] = relationship(back_populates="location")


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))
    sensor_type: Mapped[str] = mapped_column(String(32))
    manufacturer: Mapped[str | None] = mapped_column(String(64), nullable=True)
    pin: Mapped[str | None] = mapped_column(String(8), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    location: Mapped["Location"] = relationship(back_populates="sensors")
    measurements: Mapped[list["Measurement"]] = relationship(back_populates="sensor")


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id", ondelete="CASCADE"))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pm10: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    pm25: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    pm1: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    temperature: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    humidity: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    pressure: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    sensor: Mapped["Sensor"] = relationship(back_populates="measurements")


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="running")
    records_fetched: Mapped[int | None] = mapped_column(Integer, default=0)
    records_saved: Mapped[int | None] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
