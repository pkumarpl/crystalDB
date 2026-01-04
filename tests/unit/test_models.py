"""Unit tests for database models."""

import pytest
from sqlalchemy.orm import Session

from crystaldb.models import Material, Solvent


def test_create_material(db_session: Session):
    """Test creating a material."""
    material = Material(
        compound_name="Sodium Chloride",
        chemical_formula="NaCl",
        canonical_smile="[Na+].[Cl-]",
        type="inorganic salt",
        cas_number="7647-14-5",
        product_number="S9888",
        supplier="Sigma-Aldrich",
    )

    db_session.add(material)
    db_session.commit()
    db_session.refresh(material)

    assert material.material_id is not None
    assert material.compound_name == "Sodium Chloride"
    assert material.created_at is not None
    assert material.updated_at is not None


def test_create_solvent(db_session: Session):
    """Test creating a solvent."""
    solvent = Solvent(
        solvent_name="Water",
        chemical_formula="H2O",
        canonical_smile="O",
        cas_number="7732-18-5",
        product_number="W3500",
        supplier="Sigma-Aldrich",
    )

    db_session.add(solvent)
    db_session.commit()
    db_session.refresh(solvent)

    assert solvent.solvent_id is not None
    assert solvent.solvent_name == "Water"
    assert solvent.created_at is not None


def test_material_repr(sample_material: Material):
    """Test material representation."""
    repr_str = repr(sample_material)
    assert "Material" in repr_str
    assert "Test Compound" in repr_str
