"""Material schemas for validation and serialization."""

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class MaterialBase(BaseModel):
    """Base material schema with common fields."""

    compound_name: str = Field(..., max_length=100)
    chemical_formula: str = Field(..., max_length=50)
    canonical_smile: str
    type: str = Field(..., max_length=50)
    cas_number: str = Field(..., max_length=50)
    product_number: str = Field(..., max_length=50)
    supplier: str = Field(..., max_length=50)


class MaterialCreate(MaterialBase):
    """Schema for creating a new material."""

    pass


class MaterialUpdate(BaseModel):
    """Schema for updating a material."""

    compound_name: str | None = Field(None, max_length=100)
    chemical_formula: str | None = Field(None, max_length=50)
    canonical_smile: str | None = None
    type: str | None = Field(None, max_length=50)
    cas_number: str | None = Field(None, max_length=50)
    product_number: str | None = Field(None, max_length=50)
    supplier: str | None = Field(None, max_length=50)


class MaterialResponse(MaterialBase):
    """Schema for material response."""

    model_config = ConfigDict(from_attributes=True)

    material_id: int
    created_at: datetime
    updated_at: datetime
