# Web Frontend - React + TypeScript

React-based web frontend for visualizing chemical equipment data.

## Setup

### Prerequisites
- Node.js 16+ with npm

### Installation

1. **Install Dependencies**
   ```bash
   npm install
   ```

### Running the Application

```bash
npm run dev
```

The frontend will start at `http://localhost:3000` and proxy API calls to the Django backend.

### Building for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

## Features

- **CSV Upload**: Upload equipment data files
- **Dataset Management**: View last 5 uploaded datasets
- **Data Tables**: Paginated equipment records (25 per page)
- **Charts**: 
  - Flowrate statistics (bar chart)
  - Equipment type distribution
  - Pressure & Temperature comparison (line chart)
- **Summary Statistics**: Min/max/mean/median for numeric fields

## Requirements

- Backend running at `http://localhost:8000`
- Proper CORS configuration on backend

## Technologies

- React 18.3+
- TypeScript
- Vite 5.3+
- Axios 1.7+
- Chart.js 4.4+
- React-ChartJS-2 5.2+
