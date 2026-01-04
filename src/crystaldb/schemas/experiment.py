"""Experiment schemas for validation and serialization."""

from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


class ExperimentBase(BaseModel):
    """Base experiment schema with common fields."""

    experiment_id: str = Field(..., max_length=50)
    exp_date: date

    # Required material
    material1_id: int = Field(..., gt=0)
    material1_quantity: float = Field(..., gt=0)
    material1_quantity_unit: str = Field(..., max_length=20)

    # Optional materials
    material2_id: int | None = Field(None, gt=0)
    material2_quantity: float | None = Field(None, gt=0)
    material2_quantity_unit: str | None = Field(None, max_length=20)

    material3_id: int | None = Field(None, gt=0)
    material3_quantity: float | None = Field(None, gt=0)
    material3_quantity_unit: str | None = Field(None, max_length=20)

    material4_id: int | None = Field(None, gt=0)
    material4_quantity: float | None = Field(None, gt=0)
    material4_quantity_unit: str | None = Field(None, max_length=20)

    # Required solvent
    solvent1_id: int = Field(..., gt=0)
    solvent1_quantity: float = Field(..., gt=0)
    solvent1_quantity_unit: str = Field(..., max_length=20)

    # Optional solvents
    solvent2_id: int | None = Field(None, gt=0)
    solvent2_quantity: float | None = Field(None, gt=0)
    solvent2_quantity_unit: str | None = Field(None, max_length=20)

    solvent3_id: int | None = Field(None, gt=0)
    solvent3_quantity: float | None = Field(None, gt=0)
    solvent3_quantity_unit: str | None = Field(None, max_length=20)

    solvent4_id: int | None = Field(None, gt=0)
    solvent4_quantity: float | None = Field(None, gt=0)
    solvent4_quantity_unit: str | None = Field(None, max_length=20)

    # Experimental conditions
    start_solution_temp: float
    crystal_growth_temp: float
    crystallization_method: str | None = Field(None, max_length=100)
    notes: str | None = None


class ExperimentCreate(ExperimentBase):
    """Schema for creating a new experiment."""

    pass


class ExperimentUpdate(BaseModel):
    """Schema for updating an experiment."""

    exp_date: date | None = None
    start_solution_temp: float | None = None
    crystal_growth_temp: float | None = None
    crystallization_method: str | None = Field(None, max_length=100)
    notes: str | None = None


class ExperimentResponse(ExperimentBase):
    """Schema for experiment response."""

    model_config = ConfigDict(from_attributes=True)

    exp_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
