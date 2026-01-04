# CrystalDB v2.0

**Modern crystallography experiment and data collection system**

A production-ready REST API for managing crystallography experiments, materials, solvents, and measurement data. Built with FastAPI, SQLAlchemy 2.0, and modern Python best practices.

## Features

- **RESTful API**: Full CRUD operations for all resources
- **Type Safety**: Full type hints with Pydantic validation
- **Database Migrations**: Managed with Alembic
- **Containerized**: Docker and Docker Compose support
- **Tested**: Comprehensive test suite with pytest
- **Production-Ready**: Logging, error handling, and monitoring
- **Modern Stack**: Python 3.11+, FastAPI, SQLAlchemy 2.0

## Tech Stack

- **Framework**: FastAPI 0.109+
- **ORM**: SQLAlchemy 2.0+ with MySQL/MariaDB
- **Validation**: Pydantic 2.5+
- **Database**: MySQL 8.0
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest with coverage
- **Code Quality**: black, ruff, mypy, pre-commit

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crystalDB
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize database and import data**
   ```bash
   docker-compose exec api python scripts/init_db.py
   docker-compose exec api python scripts/import_data.py
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development

1. **Prerequisites**
   - Python 3.11+
   - MySQL 8.0+
   - pip or poetry

2. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Update DATABASE_* variables for your MySQL instance
   ```

4. **Initialize database**
   ```bash
   python scripts/init_db.py
   python scripts/import_data.py
   ```

5. **Run the development server**
   ```bash
   python -m crystaldb.main
   ```

   Or with auto-reload:
   ```bash
   uvicorn crystaldb.main:app --reload
   ```

## Project Structure

```
crystalDB/
├── src/crystaldb/          # Main application code
│   ├── api/                # FastAPI routers and endpoints
│   │   └── routers/        # Resource-specific routers
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration management
│   │   ├── exceptions.py   # Custom exceptions
│   │   └── logging.py      # Logging configuration
│   ├── db/                 # Database configuration
│   │   ├── base.py         # SQLAlchemy base
│   │   └── session.py      # Database session management
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic schemas
│   └── main.py             # Application entry point
├── scripts/                # Utility scripts
│   ├── init_db.py          # Database initialization
│   └── import_data.py      # Data import from CSV
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── data/                   # Data files (CSV, etc.)
├── logs/                   # Application logs
├── pyproject.toml          # Project configuration
├── Dockerfile              # Docker image definition
└── docker-compose.yml      # Docker services configuration
```

## API Endpoints

### Materials

- `GET /api/v1/materials` - List all materials
- `GET /api/v1/materials/{id}` - Get specific material
- `POST /api/v1/materials` - Create new material
- `PUT /api/v1/materials/{id}` - Update material
- `DELETE /api/v1/materials/{id}` - Delete material
- `GET /api/v1/materials/search/by-name/{name}` - Search by name
- `GET /api/v1/materials/search/by-cas/{cas}` - Search by CAS number

### Solvents

- `GET /api/v1/solvents` - List all solvents
- `GET /api/v1/solvents/{id}` - Get specific solvent
- `POST /api/v1/solvents` - Create new solvent
- `PUT /api/v1/solvents/{id}` - Update solvent
- `DELETE /api/v1/solvents/{id}` - Delete solvent

### Experiments

- `GET /api/v1/experiments` - List all experiments
- `GET /api/v1/experiments/{id}` - Get specific experiment
- `POST /api/v1/experiments` - Create new experiment
- `PUT /api/v1/experiments/{id}` - Update experiment
- `DELETE /api/v1/experiments/{id}` - Delete experiment

Full API documentation available at `/docs` when running the server.

## Database Schema

The system uses 6 main tables:

- **users**: Researcher accounts and authentication
- **materials**: Chemical compounds used in experiments
- **solvents**: Solvents used in crystallization
- **experiments**: Experiment setup and configuration
- **morphologies**: Crystal physical characteristics
- **measurements**: Crystallographic measurement data

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/crystaldb --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

### Code Quality

```bash
# Install pre-commit hooks
pre-commit install

# Run all checks manually
pre-commit run --all-files

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for all available options:

- **Database**: Connection settings, pooling
- **API**: Host, port, workers
- **Security**: Secret keys, token expiration
- **Logging**: Log level, file paths

## Production Deployment

1. **Use environment variables** for all sensitive configuration
2. **Enable HTTPS** with reverse proxy (nginx, Traefik)
3. **Set up monitoring** (Prometheus, Grafana)
4. **Configure backups** for MySQL database
5. **Use secrets management** (Vault, AWS Secrets Manager)
6. **Set appropriate CORS** origins in production
7. **Scale with** multiple API workers or containers

## Migration from v1.0

The v1.0 Jupyter notebooks have been replaced with:

- **Database initialization**: `scripts/init_db.py`
- **Data import**: `scripts/import_data.py`
- **API access**: RESTful endpoints instead of direct DB access

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Documentation: http://localhost:8000/docs

## Changelog

### v2.0.0 (2026-01-04)

- Complete rewrite with modern Python stack
- FastAPI REST API
- SQLAlchemy 2.0 with type hints
- Pydantic validation
- Docker containerization
- Comprehensive test suite
- Production-ready logging and error handling
