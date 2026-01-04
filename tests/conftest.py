"""Pytest configuration and fixtures."""

import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient

from crystaldb.db.base import Base
from crystaldb.db import get_db
from crystaldb.api.app import create_app
from crystaldb.models import User, Material, Solvent


# Test database URL (use SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    app = create_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_material(db_session) -> Material:
    """Create a sample material for testing."""
    material = Material(
        compound_name="Test Compound",
        chemical_formula="H2O",
        canonical_smile="O",
        type="test",
        cas_number="7732-18-5",
        product_number="TEST001",
        supplier="Test Supplier",
    )
    db_session.add(material)
    db_session.commit()
    db_session.refresh(material)
    return material


@pytest.fixture
def sample_solvent(db_session) -> Solvent:
    """Create a sample solvent for testing."""
    solvent = Solvent(
        solvent_name="Test Solvent",
        chemical_formula="H2O",
        canonical_smile="O",
        cas_number="7732-18-5",
        product_number="TEST001",
        supplier="Test Supplier",
    )
    db_session.add(solvent)
    db_session.commit()
    db_session.refresh(solvent)
    return solvent
