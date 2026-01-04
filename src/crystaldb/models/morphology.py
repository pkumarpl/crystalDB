"""Morphology model for crystal physical characteristics."""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from .experiment import Experiment
    from .measurement import Measurement


class Morphology(Base, TimestampMixin):
    """Crystal morphology and physical characteristics."""

    __tablename__ = "morphologies"

    crst_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exp_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.exp_id"), nullable=False, index=True
    )
    crystal_date: Mapped[date] = mapped_column(Date, nullable=False)
    crystal_type: Mapped[str | None] = mapped_column(String(50))
    crystal_shape: Mapped[str | None] = mapped_column(String(50))
    crystal_color: Mapped[str | None] = mapped_column(String(50))

    # Crystal dimensions (in mm typically)
    crystal_size_a: Mapped[float | None] = mapped_column()
    crystal_size_b: Mapped[float | None] = mapped_column()
    crystal_size_c: Mapped[float | None] = mapped_column()

    # Physical properties
    crystal_melting_temp: Mapped[float | None] = mapped_column()

    # Relationships
    experiment: Mapped["Experiment"] = relationship(back_populates="morphologies")
    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="morphology", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Morphology(id={self.crst_id}, exp_id={self.exp_id}, shape='{self.crystal_shape}')>"
