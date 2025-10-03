# QR DigitalMenu API
## Prerequisites

- Python 3.13 installed on your system
- PostgreSQL
- Git installed
- `uv` installed (see installation instructions below)

## Installation

### 1. Install uv

**On macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
On Windows:
```bash

powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Alternative installation methods:
```bash

# Using pip
pip install uv

# Using pipx
pipx install uv
```
2. Clone the Repository via SSH
```bash

git clone git@github.com:almircoo/qrmenuapi.git
cd qrmenuapi
```

Project Setup
1. Create Virtual Environment and Install Dependencies
```bash

# Create virtual environment and install dependencies from pyproject.toml
uv sync

# Or if you need to specify Python version
uv sync --python 3.13
```
2. Activate the Virtual Environment
```bash

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# OR
.venv\Scripts\activate     # On Windows

# With uv, you can also run commands directly without activation
uv run python manage.py [command]
```
3. Environment Configuration

Create environment file if needed:
```bash

# Copy environment template (if provided)
cp .env.example .env

# Edit environment variables
nano .env  # or use your preferred editor
```
Common environment variables to set:
```env

DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
DATABASE_NAME=****
DATABASE_USER=****
DATABASE_PASSWORD=*******
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```
4. Database Setup
```bash

# Run migrations
uv run python manage.py migrate

# Create superuser (optional)
uv run python manage.py createsuperuser
```

Running the Development Server
```bash

# Using uv run
uv run python manage.py runserver
```
Common Management Commands
```bash

# Create new migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Run tests
uv run python manage.py test

# Start Django shell
uv run python manage.py shell

# Check project health
uv run python manage.py check
```