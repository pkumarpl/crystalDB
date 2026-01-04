"""Solvent schemas for validation and serialization."""

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class SolventBase(BaseModel):
    """Base solvent schema with common fields."""

    solvent_name: str = Field(..., max_length=100)
    chemical_formula: str = Field(..., max_length=50)
    canonical_smile: str
    cas_number: str = Field(..., max_length=50)
    product_number: str = Field(..., max_length=50)
    supplier: str = Field(..., max_length=50)


class SolventCreate(SolventBase):
    """Schema for creating a new solvent."""

    pass


class SolventUpdate(BaseModel):
    """Schema for updating a solvent."""

    solvent_name: str | None = Field(None, max_length=100)
    chemical_formula: str | None = Field(None, max_length=50)
    canonical_smile: str | None = None
    cas_number: str | None = Field(None, max_length=50)
    product_number: str | None = Field(None, max_length=50)
    supplier: str | None = Field(None, max_length=50)


class SolventResponse(SolventBase):
    """Schema for solvent response."""

    model_config = ConfigDict(from_attributes=True)

    solvent_id: int
    created_at: datetime
    updated_at: datetime
