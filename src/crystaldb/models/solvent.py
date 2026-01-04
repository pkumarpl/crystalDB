"""Solvent model for solvents used in crystallization."""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base, TimestampMixin


class Solvent(Base, TimestampMixin):
    """Solvent used in crystallization experiments."""

    __tablename__ = "solvents"

    solvent_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    solvent_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    chemical_formula: Mapped[str] = mapped_column(String(50), nullable=False)
    canonical_smile: Mapped[str] = mapped_column(Text, nullable=False)
    cas_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    product_number: Mapped[str] = mapped_column(String(50), nullable=False)
    supplier: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"<Solvent(id={self.solvent_id}, name='{self.solvent_name}', formula='{self.chemical_formula}')>"
