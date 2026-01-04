"""Materials API router."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...core.exceptions import NotFoundException
from ...db import get_db
from ...models import Material
from ...schemas import MaterialCreate, MaterialUpdate, MaterialResponse

router = APIRouter()


@router.get("", response_model=List[MaterialResponse])
def list_materials(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db),
) -> List[Material]:
    """List all materials with pagination."""
    stmt = select(Material).offset(skip).limit(limit)
    materials = db.execute(stmt).scalars().all()
    return list(materials)


@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),
) -> Material:
    """Get a specific material by ID."""
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with id {material_id} not found",
        )
    return material


@router.post("", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(
    material_in: MaterialCreate,
    db: Session = Depends(get_db),
) -> Material:
    """Create a new material."""
    material = Material(**material_in.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(
    material_id: int,
    material_in: MaterialUpdate,
    db: Session = Depends(get_db),
) -> Material:
    """Update an existing material."""
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with id {material_id} not found",
        )

    # Update only provided fields
    update_data = material_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(material, field, value)

    db.commit()
    db.refresh(material)
    return material


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a material."""
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with id {material_id} not found",
        )

    db.delete(material)
    db.commit()


@router.get("/search/by-cas/{cas_number}", response_model=List[MaterialResponse])
def search_by_cas(
    cas_number: str,
    db: Session = Depends(get_db),
) -> List[Material]:
    """Search materials by CAS number."""
    stmt = select(Material).where(Material.cas_number == cas_number)
    materials = db.execute(stmt).scalars().all()
    return list(materials)


@router.get("/search/by-name/{name}", response_model=List[MaterialResponse])
def search_by_name(
    name: str,
    db: Session = Depends(get_db),
) -> List[Material]:
    """Search materials by compound name (partial match)."""
    stmt = select(Material).where(Material.compound_name.contains(name))
    materials = db.execute(stmt).scalars().all()
    return list(materials)
