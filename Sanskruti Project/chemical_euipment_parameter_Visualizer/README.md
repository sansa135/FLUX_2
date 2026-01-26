# Chemical Equipment Parameter Visualizer - Backend

Django REST API for CSV-based chemical equipment data analysis.

## Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Create Virtual Environment**
   ```bash
   python -m venv env
   source env/Scripts/activate  # Windows
   # or
   source env/bin/activate  # Unix/macOS
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Django Server**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`.

## API Endpoints

### Upload Dataset
- **POST** `/api/upload/`
- **Form Data**: `file` (CSV) + optional `name`
- **Response**: Dataset object with summary stats

### List Datasets
- **GET** `/api/datasets/`
- **Response**: Array of last 5 uploaded datasets

### Get Latest Dataset
- **GET** `/api/datasets/latest/`
- **Response**: Most recently uploaded dataset

### Get Dataset Summary
- **GET** `/api/datasets/{id}/summary/`
- **Response**: Summary stats (min/max/mean/median for numeric fields, type distribution)

### List Equipment Records
- **GET** `/api/datasets/{id}/records/?page=1`
- **Response**: Paginated equipment records (25 per page)

## CSV Format

Required columns:
- `Equipment Name` - Name of the equipment
- `Type` - Equipment type/category
- `Flowrate` - Numeric flowrate value
- `Pressure` - Numeric pressure value
- `Temperature` - Numeric temperature value

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Feed Pump A,Pump,120.5,15.2,38.5
Reactor R-101,Reactor,85.0,12.5,95.0
```

See [sample_equipment_data.csv](../sample_equipment_data.csv) for a complete example.

## Admin Panel

Access at `http://localhost:8000/admin/` with superuser credentials.

## Database

- **Engine**: SQLite (default)
- **Retention**: Last 5 uploaded datasets are retained; older ones are auto-deleted

## Technologies

- Django 6.0+
- Django REST Framework 3.14+
- Pandas 3.0+
- CORS enabled for all origins (development)
