# Chemical Equipment Parameter Visualizer

Full-stack application for analyzing and visualizing chemical equipment data from CSV files.

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── analytics/                      # Django app for CSV processing & APIs
│   ├── migrations/
│   ├── models.py                   # EquipmentDataset, EquipmentRecord models
│   ├── serializers.py              # DRF serializers
│   ├── views.py                    # API endpoints
│   ├── urls.py                     # API routes
│   ├── admin.py                    # Django admin config
│   └── ...
├── chemical_euipment_parameter_Visualizer/
│   ├── settings.py                 # Django settings (CORS, REST_FRAMEWORK, etc.)
│   ├── urls.py                     # Root URL config
│   └── ...
├── web-frontend/                   # React + TypeScript frontend
│   ├── src/
│   │   ├── api/index.ts            # Axios client & API types
│   │   ├── components/             # Reusable components
│   │   ├── pages/Dashboard.tsx     # Main dashboard page
│   │   └── ...
│   ├── vite.config.ts
│   ├── package.json
│   └── README.md
├── desktop-frontend/               # PyQt5 desktop frontend
│   ├── services/api_client.py      # API client for desktop
│   ├── ui/main_window.py           # Main PyQt5 window
│   ├── main.py                     # Entry point
│   ├── requirements.txt
│   └── README.md
├── sample_equipment_data.csv       # Example CSV file
├── requirements.txt                # Backend dependencies
├── manage.py
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Activate virtual environment
source env/Scripts/activate  # Windows
# or
source env/bin/activate     # Unix/macOS

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Backend available at: **http://localhost:8000**

### 2. Web Frontend Setup

```bash
cd web-frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend available at: **http://localhost:3000**

### 3. Desktop Frontend Setup

```bash
cd desktop-frontend

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📊 API Endpoints

All endpoints are under `/api/`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/` | Upload CSV file |
| GET | `/datasets/` | List last 5 datasets |
| GET | `/datasets/latest/` | Get most recent dataset |
| GET | `/datasets/{id}/summary/` | Dataset summary stats |
| GET | `/datasets/{id}/records/?page=1` | Paginated equipment records |

## 📝 CSV Format

Required columns (case-insensitive):
- `Equipment Name` - Equipment identifier
- `Type` - Equipment category
- `Flowrate` - Numeric value
- `Pressure` - Numeric value
- `Temperature` - Numeric value

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Feed Pump A,Pump,120.5,15.2,38.5
Reactor R-101,Reactor,85.0,12.5,95.0
```

See [sample_equipment_data.csv](sample_equipment_data.csv) for more examples.

## 🎯 Features

### Backend
- ✅ CSV parsing and validation
- ✅ Automatic data normalization
- ✅ Summary statistics (min/max/mean/median)
- ✅ Type distribution analysis
- ✅ Pagination (25 records per page)
- ✅ Last 5 datasets retention
- ✅ Admin interface

### Web Frontend
- ✅ CSV upload form
- ✅ Dataset dropdown selector
- ✅ Equipment data table with pagination
- ✅ Flowrate bar chart
- ✅ Equipment type distribution chart
- ✅ Pressure & temperature line chart

### Desktop Frontend
- ✅ CSV upload via file dialog
- ✅ Tabbed interface (Records/Charts/Summary)
- ✅ Equipment table with pagination
- ✅ Matplotlib visualization (4-subplot chart)
- ✅ Background API requests (threading)

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0, DRF 3.14, Pandas 3.0 |
| **Web Frontend** | React 18, TypeScript, Vite, Chart.js |
| **Desktop Frontend** | PyQt5, Matplotlib, Requests |
| **Database** | SQLite |
| **Version Control** | Git/GitHub |

## 📋 Data Retention Policy

- Maximum **5 datasets** stored in database
- Older datasets auto-deleted when new ones are uploaded
- Raw CSV files preserved in media folder

## 🔧 Admin Panel

Access at `http://localhost:8000/admin/` to:
- View/edit uploaded datasets
- View/edit equipment records
- Manage data retention

## 📚 Documentation

- [Backend README](./README.md)
- [Web Frontend README](./web-frontend/README.md)
- [Desktop Frontend README](./desktop-frontend/README.md)

## 🐛 Troubleshooting

### Frontend can't reach backend?
- Ensure Django server is running on port 8000
- Check CORS settings in `settings.py` (should be `CORS_ALLOW_ALL_ORIGINS = True` for dev)

### CSV upload fails?
- Verify column names match required format
- Ensure numeric columns contain valid numbers
- Check file size (should be reasonable for SQLite)

### Desktop app won't start?
- Verify PyQt5 is installed: `pip install PyQt5`
- Ensure backend is running
- Check API URL in `services/api_client.py`

## 📦 Deployment

### Production Considerations
- Set `DEBUG = False` in settings
- Use proper SECRET_KEY
- Configure allowed hosts
- Use PostgreSQL instead of SQLite
- Enable CSRF protection (CORS_ALLOW_ALL_ORIGINS → False)
- Use environment variables for secrets

## 📄 License

[Your License Here]

## 👤 Author

[Your Name]

## 📞 Support

For issues or questions, please contact or create an issue on GitHub.
