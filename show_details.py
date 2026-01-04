#!/usr/bin/env python3
"""Show detailed database content."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from crystaldb.db import SessionLocal
from crystaldb.models import Material, Solvent

def show_materials():
    """Show detailed materials."""
    db = SessionLocal()
    try:
        materials = db.query(Material).limit(10).all()
        total = db.query(Material).count()

        print("=" * 120)
        print(f"MATERIALS TABLE (showing 10 of {total})")
        print("=" * 120)
        print(f"{'ID':<5} {'Compound Name':<45} {'Formula':<15} {'Type':<18} {'CAS Number':<12}")
        print("-" * 120)

        for m in materials:
            print(f"{m.material_id:<5} {m.compound_name[:44]:<45} {m.chemical_formula[:14]:<15} {m.type[:17]:<18} {m.cas_number:<12}")

        print("\n")
    finally:
        db.close()

def show_solvents():
    """Show detailed solvents."""
    db = SessionLocal()
    try:
        solvents = db.query(Solvent).limit(10).all()
        total = db.query(Solvent).count()

        print("=" * 120)
        print(f"SOLVENTS TABLE (showing 10 of {total})")
        print("=" * 120)
        print(f"{'ID':<5} {'Solvent Name':<35} {'Formula':<15} {'CAS Number':<12} {'Supplier':<15}")
        print("-" * 120)

        for s in solvents:
            print(f"{s.solvent_id:<5} {s.solvent_name[:34]:<35} {s.chemical_formula[:14]:<15} {s.cas_number:<12} {s.supplier:<15}")

        print("\n")
    finally:
        db.close()

def show_stats():
    """Show database statistics."""
    db = SessionLocal()
    try:
        print("=" * 120)
        print("DATABASE STATISTICS")
        print("=" * 120)

        material_count = db.query(Material).count()
        solvent_count = db.query(Solvent).count()

        # Count by material type
        from sqlalchemy import func
        material_types = db.query(
            Material.type,
            func.count(Material.material_id).label('count')
        ).group_by(Material.type).all()

        print(f"\n📊 Total Materials: {material_count}")
        print(f"📊 Total Solvents: {solvent_count}")

        print("\n📋 Materials by Type:")
        print("-" * 60)
        for mtype, count in material_types:
            print(f"  {mtype:<25} : {count:>3} compounds")

        print("\n" + "=" * 120)
    finally:
        db.close()

if __name__ == "__main__":
    show_stats()
    print()
    show_materials()
    show_solvents()
