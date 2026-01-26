# Chemical Equipment Parameter Visualizer - Desktop Frontend

PyQt5-based desktop application for visualizing chemical equipment data.

## Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python main.py
```

The desktop application will launch and connect to the Django backend at `http://localhost:8000`.

## Features

- **Upload CSV**: Select and upload CSV files with equipment data
- **View Records**: Browse equipment records in a paginated table
- **Analytics Charts**: Visualize flowrate, pressure, temperature statistics
- **Equipment Type Distribution**: See breakdown by equipment type
- **Dataset Management**: Switch between uploaded datasets

## Requirements

- Backend running at `http://localhost:8000`
- CSV file format as specified in backend README

## Technologies

- PyQt5 5.15+
- Matplotlib 3.8+
- Requests 2.31+
