"""Measurement schemas for validation and serialization."""

from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


class MeasurementBase(BaseModel):
    """Base measurement schema with common fields."""

    measurement_id: str = Field(..., max_length=50)
    measr_date: date
    space_group: str | None = Field(None, max_length=50)
    assym_unit_composition: str | None = Field(None, max_length=100)
    canonical_smile_crystal_comp: str | None = None
    measurement_temp: float | None = None
    cell_length_a: float | None = Field(None, gt=0)
    cell_length_b: float | None = Field(None, gt=0)
    cell_length_c: float | None = Field(None, gt=0)
    cell_angle_alpha: float | None = Field(None, gt=0, le=180)
    cell_angle_beta: float | None = Field(None, gt=0, le=180)
    cell_angle_gamma: float | None = Field(None, gt=0, le=180)
    cell_volume: float | None = Field(None, gt=0)
    diff_measurement_device: str | None = Field(None, max_length=100)


class MeasurementCreate(MeasurementBase):
    """Schema for creating a new measurement."""

    exp_id: int = Field(..., gt=0)
    crst_id: int = Field(..., gt=0)


class MeasurementUpdate(BaseModel):
    """Schema for updating a measurement."""

    measr_date: date | None = None
    space_group: str | None = Field(None, max_length=50)
    assym_unit_composition: str | None = Field(None, max_length=100)
    canonical_smile_crystal_comp: str | None = None
    measurement_temp: float | None = None
    cell_length_a: float | None = Field(None, gt=0)
    cell_length_b: float | None = Field(None, gt=0)
    cell_length_c: float | None = Field(None, gt=0)
    cell_angle_alpha: float | None = Field(None, gt=0, le=180)
    cell_angle_beta: float | None = Field(None, gt=0, le=180)
    cell_angle_gamma: float | None = Field(None, gt=0, le=180)
    cell_volume: float | None = Field(None, gt=0)
    diff_measurement_device: str | None = Field(None, max_length=100)


class MeasurementResponse(MeasurementBase):
    """Schema for measurement response."""

    model_config = ConfigDict(from_attributes=True)

    measr_id: int
    exp_id: int
    crst_id: int
    created_at: datetime
    updated_at: datetime
