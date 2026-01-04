"""Morphology schemas for validation and serialization."""

from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


class MorphologyBase(BaseModel):
    """Base morphology schema with common fields."""

    crystal_date: date
    crystal_type: str | None = Field(None, max_length=50)
    crystal_shape: str | None = Field(None, max_length=50)
    crystal_color: str | None = Field(None, max_length=50)
    crystal_size_a: float | None = Field(None, gt=0)
    crystal_size_b: float | None = Field(None, gt=0)
    crystal_size_c: float | None = Field(None, gt=0)
    crystal_melting_temp: float | None = None


class MorphologyCreate(MorphologyBase):
    """Schema for creating a new morphology."""

    exp_id: int = Field(..., gt=0)


class MorphologyUpdate(BaseModel):
    """Schema for updating a morphology."""

    crystal_date: date | None = None
    crystal_type: str | None = Field(None, max_length=50)
    crystal_shape: str | None = Field(None, max_length=50)
    crystal_color: str | None = Field(None, max_length=50)
    crystal_size_a: float | None = Field(None, gt=0)
    crystal_size_b: float | None = Field(None, gt=0)
    crystal_size_c: float | None = Field(None, gt=0)
    crystal_melting_temp: float | None = None


class MorphologyResponse(MorphologyBase):
    """Schema for morphology response."""

    model_config = ConfigDict(from_attributes=True)

    crst_id: int
    exp_id: int
    created_at: datetime
    updated_at: datetime
