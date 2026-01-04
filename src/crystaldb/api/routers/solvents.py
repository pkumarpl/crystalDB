"""Solvents API router."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import Solvent
from ...schemas import SolventCreate, SolventUpdate, SolventResponse

router = APIRouter()


@router.get("", response_model=List[SolventResponse])
def list_solvents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db),
) -> List[Solvent]:
    """List all solvents with pagination."""
    stmt = select(Solvent).offset(skip).limit(limit)
    solvents = db.execute(stmt).scalars().all()
    return list(solvents)


@router.get("/{solvent_id}", response_model=SolventResponse)
def get_solvent(
    solvent_id: int,
    db: Session = Depends(get_db),
) -> Solvent:
    """Get a specific solvent by ID."""
    solvent = db.get(Solvent, solvent_id)
    if not solvent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solvent with id {solvent_id} not found",
        )
    return solvent


@router.post("", response_model=SolventResponse, status_code=status.HTTP_201_CREATED)
def create_solvent(
    solvent_in: SolventCreate,
    db: Session = Depends(get_db),
) -> Solvent:
    """Create a new solvent."""
    solvent = Solvent(**solvent_in.model_dump())
    db.add(solvent)
    db.commit()
    db.refresh(solvent)
    return solvent


@router.put("/{solvent_id}", response_model=SolventResponse)
def update_solvent(
    solvent_id: int,
    solvent_in: SolventUpdate,
    db: Session = Depends(get_db),
) -> Solvent:
    """Update an existing solvent."""
    solvent = db.get(Solvent, solvent_id)
    if not solvent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solvent with id {solvent_id} not found",
        )

    # Update only provided fields
    update_data = solvent_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(solvent, field, value)

    db.commit()
    db.refresh(solvent)
    return solvent


@router.delete("/{solvent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_solvent(
    solvent_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a solvent."""
    solvent = db.get(Solvent, solvent_id)
    if not solvent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solvent with id {solvent_id} not found",
        )

    db.delete(solvent)
    db.commit()


@router.get("/search/by-name/{name}", response_model=List[SolventResponse])
def search_by_name(
    name: str,
    db: Session = Depends(get_db),
) -> List[Solvent]:
    """Search solvents by name (partial match)."""
    stmt = select(Solvent).where(Solvent.solvent_name.contains(name))
    solvents = db.execute(stmt).scalars().all()
    return list(solvents)
