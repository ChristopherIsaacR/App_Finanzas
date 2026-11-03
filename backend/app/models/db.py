"""Modelos de base de datos (SQLAlchemy 2.0).

Incluye tablas de usuarios y perfiles desde ahora, para que la plataforma
sea multiusuario cuando pase de proyecto personal a público.
"""
import datetime as dt

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


class Base(DeclarativeBase):
    pass


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(200))
    asset_type: Mapped[str | None] = mapped_column(String(30))  # EQUITY, ETF...
    currency: Mapped[str | None] = mapped_column(String(10))
    prices: Mapped[list["PriceDaily"]] = relationship(back_populates="instrument")


class PriceDaily(Base):
    """Precios diarios. Se guarda la fuente y la fecha de descarga de cada dato."""
    __tablename__ = "prices_daily"
    __table_args__ = (UniqueConstraint("instrument_id", "date", name="uq_instrument_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"), index=True)
    date: Mapped[dt.date] = mapped_column(Date, index=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)  # ajustado por dividendos y splits
    volume: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(30))
    fetched_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now)
    instrument: Mapped[Instrument] = relationship(back_populates="prices")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now)
    profiles: Mapped[list["InvestorProfileRow"]] = relationship(back_populates="user")


class InvestorProfileRow(Base):
    __tablename__ = "investor_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    objetivo: Mapped[str] = mapped_column(String(30))
    horizonte_anios: Mapped[int] = mapped_column(Integer)
    tolerancia_riesgo: Mapped[str] = mapped_column(String(10))
    max_caida_tolerada: Mapped[float] = mapped_column(Float)
    capital_inicial: Mapped[float] = mapped_column(Float)
    aporte_mensual: Mapped[float] = mapped_column(Float)
    experiencia: Mapped[str] = mapped_column(String(15))
    user: Mapped[User] = relationship(back_populates="profiles")
