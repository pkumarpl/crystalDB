"""Material model for chemical compounds used in experiments."""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base, TimestampMixin


class Material(Base, TimestampMixin):
    """Material (chemical compound) used in crystallization experiments."""

    __tablename__ = "materials"

    material_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    compound_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    chemical_formula: Mapped[str] = mapped_column(String(50), nullable=False)
    canonical_smile: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    cas_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    product_number: Mapped[str] = mapped_column(String(50), nullable=False)
    supplier: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"<Material(id={self.material_id}, name='{self.compound_name}', formula='{self.chemical_formula}')>"
