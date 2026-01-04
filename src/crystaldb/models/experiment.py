"""Experiment model for crystallization experiments."""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .morphology import Morphology
    from .measurement import Measurement


class Experiment(Base, TimestampMixin):
    """Crystallization experiment setup and configuration."""

    __tablename__ = "experiments"

    exp_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True)
    experiment_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    exp_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Materials (up to 4 materials can be used)
    material1_id: Mapped[int] = mapped_column(
        ForeignKey("materials.material_id"), nullable=False
    )
    material1_quantity: Mapped[float] = mapped_column(nullable=False)
    material1_quantity_unit: Mapped[str] = mapped_column(String(20), nullable=False)

    material2_id: Mapped[int | None] = mapped_column(ForeignKey("materials.material_id"))
    material2_quantity: Mapped[float | None] = mapped_column()
    material2_quantity_unit: Mapped[str | None] = mapped_column(String(20))

    material3_id: Mapped[int | None] = mapped_column(ForeignKey("materials.material_id"))
    material3_quantity: Mapped[float | None] = mapped_column()
    material3_quantity_unit: Mapped[str | None] = mapped_column(String(20))

    material4_id: Mapped[int | None] = mapped_column(ForeignKey("materials.material_id"))
    material4_quantity: Mapped[float | None] = mapped_column()
    material4_quantity_unit: Mapped[str | None] = mapped_column(String(20))

    # Solvents (up to 4 solvents can be used)
    solvent1_id: Mapped[int] = mapped_column(ForeignKey("solvents.solvent_id"), nullable=False)
    solvent1_quantity: Mapped[float] = mapped_column(nullable=False)
    solvent1_quantity_unit: Mapped[str] = mapped_column(String(20), nullable=False)

    solvent2_id: Mapped[int | None] = mapped_column(ForeignKey("solvents.solvent_id"))
    solvent2_quantity: Mapped[float | None] = mapped_column()
    solvent2_quantity_unit: Mapped[str | None] = mapped_column(String(20))

    solvent3_id: Mapped[int | None] = mapped_column(ForeignKey("solvents.solvent_id"))
    solvent3_quantity: Mapped[float | None] = mapped_column()
    solvent3_quantity_unit: Mapped[str | None] = mapped_column(String(20))

    solvent4_id: Mapped[int | None] = mapped_column(ForeignKey("solvents.solvent_id"))
    solvent4_quantity: Mapped[float | None] = mapped_column()
    solvent4_quantity_unit: Mapped[str | None] = mapped_column(String(20))

    # Experimental conditions
    start_solution_temp: Mapped[float] = mapped_column(nullable=False)
    crystal_growth_temp: Mapped[float] = mapped_column(nullable=False)
    crystallization_method: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="experiments")
    morphologies: Mapped[list["Morphology"]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan"
    )
    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Experiment(id={self.exp_id}, experiment_id='{self.experiment_id}', date='{self.exp_date}')>"
