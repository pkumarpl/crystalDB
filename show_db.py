#!/usr/bin/env python3
"""Show database tables and content."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import inspect, text
from crystaldb.db import engine, SessionLocal
from crystaldb.models import Material, Solvent, User, Experiment, Morphology, Measurement

def show_tables():
    """Show all tables and their schemas."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("=" * 80)
    print("DATABASE TABLES")
    print("=" * 80)

    for table_name in tables:
        print(f"\n📊 Table: {table_name}")
        print("-" * 80)

        columns = inspector.get_columns(table_name)
        print(f"{'Column Name':<30} {'Type':<20} {'Nullable':<10}")
        print("-" * 80)

        for col in columns:
            col_type = str(col['type'])
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"{col['name']:<30} {col_type:<20} {nullable:<10}")

    print("\n" + "=" * 80)

def show_data():
    """Show sample data from each table."""
    db = SessionLocal()

    try:
        print("\n" + "=" * 80)
        print("DATABASE CONTENT")
        print("=" * 80)

        # Materials
        materials = db.query(Material).limit(5).all()
        print(f"\n📦 MATERIALS (showing 5 of {db.query(Material).count()})")
        print("-" * 80)
        for m in materials:
            print(f"ID: {m.material_id:3d} | {m.compound_name:<40} | {m.chemical_formula:<15} | CAS: {m.cas_number}")

        # Solvents
        solvents = db.query(Solvent).limit(5).all()
        print(f"\n🧪 SOLVENTS (showing 5 of {db.query(Solvent).count()})")
        print("-" * 80)
        for s in solvents:
            print(f"ID: {s.solvent_id:3d} | {s.solvent_name:<40} | {s.chemical_formula:<15} | CAS: {s.cas_number}")

        # Users
        users_count = db.query(User).count()
        print(f"\n👥 USERS: {users_count} records")

        # Experiments
        experiments_count = db.query(Experiment).count()
        print(f"\n🔬 EXPERIMENTS: {experiments_count} records")

        # Morphologies
        morphologies_count = db.query(Morphology).count()
        print(f"\n💎 MORPHOLOGIES: {morphologies_count} records")

        # Measurements
        measurements_count = db.query(Measurement).count()
        print(f"\n📏 MEASUREMENTS: {measurements_count} records")

        print("\n" + "=" * 80)

    finally:
        db.close()

if __name__ == "__main__":
    show_tables()
    show_data()
