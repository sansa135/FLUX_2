# 🧪 Testing Guide - Chemical Equipment Parameter Visualizer

## Prerequisites
- Django backend running: http://127.0.0.1:8000
- React frontend running: http://localhost:5174

## Test Scenarios

### 1️⃣ CSV Upload Test
**File**: `sample_equipment_data.csv`

**Steps**:
1. Navigate to http://localhost:5174
2. Click **📁 Choose CSV File**
3. Select `sample_equipment_data.csv`
4. Observe upload success message
5. Check dataset appears in dropdown

**Expected Result**: ✅ Dataset loaded with 10 records

---

### 2️⃣ View Dashboard
**Steps**:
1. Dashboard automatically loads first dataset
2. Scroll to see dataset info card
3. View three charts
4. Scroll to equipment records table

**Expected Result**: ✅ All data visible and formatted correctly

---

### 3️⃣ Dataset Selector
**Steps**:
1. Upload another CSV file (or duplicate)
2. Switch between datasets using dropdown
3. Charts and table update accordingly

**Expected Result**: ✅ Data switches without page reload

---

### 4️⃣ Pagination Test
**Steps**:
1. View equipment records table
2. Click **Next →** button
3. If < 26 records, button should still work but show same page
4. Click **← Previous** button

**Expected Result**: ✅ Navigation works smoothly

---

### 5️⃣ Chart Verification
**Charts to check**:

#### Flowrate Statistics
- Bar chart showing Min, Max, Mean, Median
- Should match dataset summary

#### Equipment Type Distribution
- Bar chart with equipment types on Y-axis
- Count on X-axis

#### Pressure & Temperature
- Line chart with two series
- Different colors for each metric

**Expected Result**: ✅ All charts render correctly

---

### 6️⃣ Error Handling
**Test upload error**:
1. Try uploading a non-CSV file
2. Try uploading CSV with missing columns
3. Try uploading empty file

**Expected Result**: ✅ Error message displayed clearly

---

### 7️⃣ Responsive Design
**Test on different screen sizes**:
- Desktop (1200px+)
- Tablet (768px)
- Mobile (320px)

**Expected Result**: ✅ Layout adapts gracefully

---

## Sample CSV Format

For testing, use this format:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Feed Pump A,Pump,120.5,15.2,38.5
Reactor R-101,Reactor,85.0,12.5,95.0
Heat Exchanger E-12,Heat Exchanger,150.0,10.0,75.0
Separator S-7,Separator,98.4,9.8,42.0
Distillation Column C-3,Column,110.2,20.5,68.0
Compressor K-5,Compressor,200.0,30.0,55.0
Storage Tank T-9,Tank,40.0,1.2,30.0
Filter F-2,Filter,60.0,8.5,33.5
Cooler C-15,Cooler,130.0,7.5,25.0
Furnace H-22,Furnace,175.0,18.0,120.0
```

---

## API Testing (Optional)

### Get All Datasets
```bash
curl http://localhost:8000/api/datasets/
```

### Get Latest Dataset
```bash
curl http://localhost:8000/api/datasets/latest/
```

### Get Records (Page 1)
```bash
curl http://localhost:8000/api/datasets/1/records/?page=1
```

### Upload CSV
```bash
curl -X POST \
  -F "file=@sample_equipment_data.csv" \
  -F "name=Test Dataset" \
  http://localhost:8000/api/upload/
```

---

## Known Limitations

- ℹ️ Only 25 records per page (configurable)
- ℹ️ Last 5 datasets retained (older ones auto-deleted)
- ℹ️ No user authentication (development mode)
- ℹ️ CORS enabled for all origins (development only)

---

## Troubleshooting

### Frontend shows 404
- ✅ Check: Is Django backend running on port 8000?
- ✅ Check: vite.config.ts has correct proxy settings
- ✅ Check: Browser console for CORS errors

### Upload fails
- ✅ Check: CSV file format matches requirements
- ✅ Check: All required columns present
- ✅ Check: Django server logs for errors

### Charts not showing
- ✅ Check: Dataset has complete summary stats
- ✅ Check: Browser console for JavaScript errors
- ✅ Check: Chart.js and react-chartjs-2 installed

---

## Success Checklist

- ✅ Django backend running and responding
- ✅ React frontend loading at http://localhost:5174
- ✅ CSV upload works
- ✅ Dashboard displays data
- ✅ Charts render correctly
- ✅ Pagination works
- ✅ Dataset switching works
- ✅ Error messages show on failures
- ✅ Responsive design works

---

**All systems ready for production deployment! 🚀**
