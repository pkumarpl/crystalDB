"""Experiments API router."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import Experiment
from ...schemas import ExperimentCreate, ExperimentUpdate, ExperimentResponse

router = APIRouter()


@router.get("", response_model=List[ExperimentResponse])
def list_experiments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    user_id: int | None = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db),
) -> List[Experiment]:
    """List all experiments with pagination and optional filtering."""
    stmt = select(Experiment)

    if user_id is not None:
        stmt = stmt.where(Experiment.user_id == user_id)

    stmt = stmt.offset(skip).limit(limit)
    experiments = db.execute(stmt).scalars().all()
    return list(experiments)


@router.get("/{exp_id}", response_model=ExperimentResponse)
def get_experiment(
    exp_id: int,
    db: Session = Depends(get_db),
) -> Experiment:
    """Get a specific experiment by ID."""
    experiment = db.get(Experiment, exp_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with id {exp_id} not found",
        )
    return experiment


@router.post("", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
def create_experiment(
    experiment_in: ExperimentCreate,
    user_id: int = Query(..., description="ID of the user creating the experiment"),
    db: Session = Depends(get_db),
) -> Experiment:
    """Create a new experiment."""
    experiment_data = experiment_in.model_dump()
    experiment_data["user_id"] = user_id

    experiment = Experiment(**experiment_data)
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment


@router.put("/{exp_id}", response_model=ExperimentResponse)
def update_experiment(
    exp_id: int,
    experiment_in: ExperimentUpdate,
    db: Session = Depends(get_db),
) -> Experiment:
    """Update an existing experiment."""
    experiment = db.get(Experiment, exp_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with id {exp_id} not found",
        )

    # Update only provided fields
    update_data = experiment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(experiment, field, value)

    db.commit()
    db.refresh(experiment)
    return experiment


@router.delete("/{exp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiment(
    exp_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete an experiment."""
    experiment = db.get(Experiment, exp_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with id {exp_id} not found",
        )

    db.delete(experiment)
    db.commit()


@router.get("/search/by-experiment-id/{experiment_id}", response_model=ExperimentResponse)
def search_by_experiment_id(
    experiment_id: str,
    db: Session = Depends(get_db),
) -> Experiment:
    """Search experiment by experiment ID."""
    stmt = select(Experiment).where(Experiment.experiment_id == experiment_id)
    experiment = db.execute(stmt).scalar_one_or_none()

    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with experiment_id '{experiment_id}' not found",
        )

    return experiment
