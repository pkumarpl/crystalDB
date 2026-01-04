#!/usr/bin/env python3
"""Import material and solvent data from CSV files."""

import csv
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy.exc import IntegrityError

from crystaldb.core.logging import setup_logging, get_logger
from crystaldb.db import SessionLocal
from crystaldb.models import Material, Solvent

setup_logging()
logger = get_logger(__name__)


def import_materials(csv_path: Path, db_session: Any) -> int:
    """Import materials from CSV file.

    Args:
        csv_path: Path to the materials CSV file
        db_session: Database session

    Returns:
        Number of materials imported
    """
    logger.info(f"Importing materials from {csv_path}")
    count = 0

    try:
        with open(csv_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            for row in reader:
                material = Material(
                    compound_name=row["compoundName"],
                    chemical_formula=row["chemicalFormula"],
                    canonical_smile=row["canonicalSmile"],
                    type=row["type"],
                    cas_number=row["casNumber"].strip(),
                    product_number=row["productNumber"],
                    supplier=row["supplier"],
                )

                try:
                    db_session.add(material)
                    db_session.flush()
                    count += 1
                except IntegrityError as e:
                    logger.warning(f"Skipping duplicate material: {row['compoundName']}")
                    db_session.rollback()
                    continue

        db_session.commit()
        logger.info(f"Successfully imported {count} materials")
        return count

    except Exception as e:
        logger.error(f"Error importing materials: {e}")
        db_session.rollback()
        raise


def import_solvents(csv_path: Path, db_session: Any) -> int:
    """Import solvents from CSV file.

    Args:
        csv_path: Path to the solvents CSV file
        db_session: Database session

    Returns:
        Number of solvents imported
    """
    logger.info(f"Importing solvents from {csv_path}")
    count = 0

    try:
        with open(csv_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            for row in reader:
                solvent = Solvent(
                    solvent_name=row["solventName"],
                    chemical_formula=row["chemicalFormula"],
                    canonical_smile=row["canonicalSmile"],
                    cas_number=row["casNumber"].strip(),
                    product_number=row["productNumber"],
                    supplier=row["supplier"],
                )

                try:
                    db_session.add(solvent)
                    db_session.flush()
                    count += 1
                except IntegrityError as e:
                    logger.warning(f"Skipping duplicate solvent: {row['solventName']}")
                    db_session.rollback()
                    continue

        db_session.commit()
        logger.info(f"Successfully imported {count} solvents")
        return count

    except Exception as e:
        logger.error(f"Error importing solvents: {e}")
        db_session.rollback()
        raise


def main() -> None:
    """Main import function."""
    # Get paths
    base_path = Path(__file__).parent.parent
    material_csv = base_path / "material2.csv"
    solvent_csv = base_path / "solvent.csv"

    # Check if files exist
    if not material_csv.exists():
        logger.error(f"Material CSV file not found: {material_csv}")
        sys.exit(1)

    if not solvent_csv.exists():
        logger.error(f"Solvent CSV file not found: {solvent_csv}")
        sys.exit(1)

    # Create database session
    db = SessionLocal()

    try:
        # Import data
        material_count = import_materials(material_csv, db)
        solvent_count = import_solvents(solvent_csv, db)

        logger.info(f"Import complete! Materials: {material_count}, Solvents: {solvent_count}")

    except Exception as e:
        logger.error(f"Import failed: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
