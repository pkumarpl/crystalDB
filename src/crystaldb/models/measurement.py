"""Measurement model for crystallographic measurements."""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from .experiment import Experiment
    from .morphology import Morphology


class Measurement(Base, TimestampMixin):
    """Crystallographic measurement data from diffraction."""

    __tablename__ = "measurements"

    measr_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exp_id: Mapped[int] = mapped_column(
        ForeignKey("experiments.exp_id"), nullable=False, index=True
    )
    crst_id: Mapped[int] = mapped_column(
        ForeignKey("morphologies.crst_id"), nullable=False, index=True
    )
    measurement_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    measr_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Crystallographic data
    space_group: Mapped[str | None] = mapped_column(String(50))
    assym_unit_composition: Mapped[str | None] = mapped_column(String(100))
    canonical_smile_crystal_comp: Mapped[str | None] = mapped_column(Text)

    # Measurement conditions
    measurement_temp: Mapped[float | None] = mapped_column()

    # Unit cell parameters
    cell_length_a: Mapped[float | None] = mapped_column()
    cell_length_b: Mapped[float | None] = mapped_column()
    cell_length_c: Mapped[float | None] = mapped_column()
    cell_angle_alpha: Mapped[float | None] = mapped_column()
    cell_angle_beta: Mapped[float | None] = mapped_column()
    cell_angle_gamma: Mapped[float | None] = mapped_column()
    cell_volume: Mapped[float | None] = mapped_column()

    # Equipment
    diff_measurement_device: Mapped[str | None] = mapped_column(String(100))

    # Relationships
    experiment: Mapped["Experiment"] = relationship(back_populates="measurements")
    morphology: Mapped["Morphology"] = relationship(back_populates="measurements")

    def __repr__(self) -> str:
        return f"<Measurement(id={self.measr_id}, measurement_id='{self.measurement_id}', space_group='{self.space_group}')>"
