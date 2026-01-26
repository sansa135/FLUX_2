import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { useState, useEffect } from 'react'
import { Bar, Line } from 'react-chartjs-2'
import { getDatasetRecords, getDatasetSummary, getDatasets, uploadDataset } from '../api/index'
import { EquipmentTable } from '../components/EquipmentTable'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

export const Dashboard = () => {
  const [datasets, setDatasets] = useState<any[]>([])
  const [selectedDataset, setSelectedDataset] = useState<any | null>(null)
  const [records, setRecords] = useState<any[]>([])
  const [currentPage, setCurrentPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchDatasets()
  }, [])

  const fetchDatasets = async () => {
    try {
      const res = await getDatasets()
      setDatasets(res.data)
      if (res.data.length > 0) {
        setSelectedDataset(res.data[0])
        fetchRecords(res.data[0].id)
      }
    } catch (err: any) {
      setError(err.message)
    }
  }

  const fetchRecords = async (datasetId: number, page: number = 1) => {
    try {
      setLoading(true)
      const res = await getDatasetRecords(datasetId, page)
      setRecords(res.data.results)
      setCurrentPage(page)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    try {
      setLoading(true)
      await uploadDataset(file)
      fetchDatasets()
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const renderCharts = () => {
    if (!selectedDataset) return null

    const summary = selectedDataset.summary
    const typeLabels = Object.keys(summary.type_distribution)
    const typeValues = Object.values(summary.type_distribution)

    const flowrateData = {
      labels: ['Min', 'Max', 'Mean', 'Median'],
      datasets: [
        {
          label: 'Flowrate',
          data: [
            summary.flowrate.min,
            summary.flowrate.max,
            summary.flowrate.mean,
            summary.flowrate.median,
          ],
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    }

    const typeDistribution = {
      labels: typeLabels,
      datasets: [
        {
          label: 'Equipment Count',
          data: typeValues,
          backgroundColor: 'rgba(153, 102, 255, 0.6)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1,
        },
      ],
    }

    const pressureTemp = {
      labels: ['Min', 'Max', 'Mean', 'Median'],
      datasets: [
        {
          label: 'Pressure',
          data: [
            summary.pressure.min,
            summary.pressure.max,
            summary.pressure.mean,
            summary.pressure.median,
          ],
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.1)',
          tension: 0.3,
        },
        {
          label: 'Temperature',
          data: [
            summary.temperature.min,
            summary.temperature.max,
            summary.temperature.mean,
            summary.temperature.median,
          ],
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.1)',
          tension: 0.3,
        },
      ],
    }

    return (
      <div style={{ marginBottom: '30px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '20px' }}>
          <div style={{
            backgroundColor: 'white',
            padding: '25px',
            borderRadius: '10px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ margin: '0 0 15px 0', color: '#1e3a8a', fontSize: '16px' }}>📈 Flowrate Statistics</h3>
            <Bar data={flowrateData} />
          </div>
          <div style={{
            backgroundColor: 'white',
            padding: '25px',
            borderRadius: '10px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ margin: '0 0 15px 0', color: '#1e3a8a', fontSize: '16px' }}>🏭 Equipment Type Distribution</h3>
            <Bar data={typeDistribution} />
          </div>
        </div>
        <div style={{
          backgroundColor: 'white',
          padding: '25px',
          borderRadius: '10px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#1e3a8a', fontSize: '16px' }}>🌡️ Pressure & Temperature Comparison</h3>
          <div style={{ position: 'relative', height: '300px' }}>
            <Line data={pressureTemp} />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa', fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif" }}>
      {/* Header */}
      <div style={{ backgroundColor: '#1e3a8a', color: 'white', padding: '30px 20px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <h1 style={{ margin: '0 0 5px 0', fontSize: '32px', fontWeight: '700' }}>⚙️ Chemical Equipment Parameter Visualizer</h1>
          <p style={{ margin: '0', opacity: 0.9, fontSize: '14px' }}>Upload, analyze, and visualize equipment data with interactive charts</p>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '30px 20px' }}>
        {/* Error Alert */}
        {error && (
          <div style={{
            padding: '15px 20px',
            backgroundColor: '#fee2e2',
            color: '#991b1b',
            border: '1px solid #fca5a5',
            borderRadius: '8px',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span style={{ fontSize: '20px' }}>⚠️</span>
            <div>
              <strong>Upload Error:</strong> {error}
            </div>
          </div>
        )}

        {/* Upload Section */}
        <div style={{
          backgroundColor: 'white',
          padding: '25px',
          borderRadius: '10px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          marginBottom: '30px'
        }}>
          <h2 style={{ margin: '0 0 15px 0', color: '#1e3a8a', fontSize: '18px' }}>📤 Upload CSV File</h2>
          <div style={{ display: 'flex', gap: '15px', alignItems: 'center', flexWrap: 'wrap' }}>
            <label htmlFor="file-upload" style={{
              padding: '12px 24px',
              backgroundColor: '#3b82f6',
              color: 'white',
              borderRadius: '6px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: '600',
              opacity: loading ? 0.6 : 1,
              transition: 'all 0.3s ease'
            }}>
              {loading ? '⏳ Uploading...' : '📁 Choose CSV File'}
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              disabled={loading}
              style={{ display: 'none' }}
            />
            <span style={{ color: '#666', fontSize: '13px' }}>CSV format: Equipment Name, Type, Flowrate, Pressure, Temperature</span>
          </div>
        </div>

        {/* Dataset Selector */}
        {datasets.length > 0 && (
          <div style={{
            backgroundColor: 'white',
            padding: '25px',
            borderRadius: '10px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '30px'
          }}>
            <h2 style={{ margin: '0 0 15px 0', color: '#1e3a8a', fontSize: '18px' }}>📊 Select Dataset</h2>
            <select
              id="dataset-select"
              value={selectedDataset?.id || ''}
              onChange={(e) => {
                const dataset = datasets.find((d) => d.id === Number(e.target.value))
                setSelectedDataset(dataset)
                if (dataset) fetchRecords(dataset.id)
              }}
              style={{
                padding: '10px 15px',
                borderRadius: '6px',
                border: '2px solid #e5e7eb',
                fontSize: '14px',
                cursor: 'pointer',
                fontWeight: '500',
                minWidth: '300px'
              }}
            >
              {datasets.map((ds) => (
                <option key={ds.id} value={ds.id}>
                  {ds.name} • {ds.row_count} rows • {new Date(ds.uploaded_at).toLocaleDateString()}
                </option>
              ))}
            </select>
          </div>
        )}

        {selectedDataset && (
          <>
            {/* Dataset Info Card */}
          <div style={{
            backgroundColor: 'white',
            padding: '25px',
            borderRadius: '10px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '30px',
            borderLeft: '4px solid #3b82f6'
          }}>
            <h3 style={{ margin: '0 0 15px 0', color: '#1e3a8a', fontSize: '20px' }}>📋 {selectedDataset.name}</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
              <div>
                <p style={{ margin: '0 0 5px 0', color: '#666', fontSize: '12px', textTransform: 'uppercase', fontWeight: '600' }}>Filename</p>
                <p style={{ margin: '0', color: '#1e3a8a', fontSize: '14px', fontWeight: '600' }}>{selectedDataset.filename}</p>
              </div>
              <div>
                <p style={{ margin: '0 0 5px 0', color: '#666', fontSize: '12px', textTransform: 'uppercase', fontWeight: '600' }}>Total Records</p>
                <p style={{ margin: '0', color: '#1e3a8a', fontSize: '14px', fontWeight: '600' }}>{selectedDataset.row_count}</p>
              </div>
              <div>
                <p style={{ margin: '0 0 5px 0', color: '#666', fontSize: '12px', textTransform: 'uppercase', fontWeight: '600' }}>Uploaded</p>
                <p style={{ margin: '0', color: '#1e3a8a', fontSize: '14px', fontWeight: '600' }}>{new Date(selectedDataset.uploaded_at).toLocaleString()}</p>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          {renderCharts()}

          {/* Equipment Records Table */}
          <div style={{
            backgroundColor: 'white',
            padding: '25px',
            borderRadius: '10px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            marginBottom: '30px'
          }}>
            <h3 style={{ margin: '0 0 20px 0', color: '#1e3a8a', fontSize: '18px' }}>📑 Equipment Records</h3>
            <EquipmentTable records={records} />

            {/* Pagination */}
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              gap: '15px',
              marginTop: '20px',
              padding: '15px',
              backgroundColor: '#f3f4f6',
              borderRadius: '8px'
            }}>
              <button
                onClick={() => fetchRecords(selectedDataset.id, currentPage - 1)}
                disabled={currentPage === 1}
                style={{
                  padding: '8px 16px',
                  backgroundColor: currentPage === 1 ? '#d1d5db' : '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: currentPage === 1 ? 'not-allowed' : 'pointer',
                  fontWeight: '600',
                  transition: 'background-color 0.3s ease'
                }}
              >
                ← Previous
              </button>
              <span style={{ fontWeight: '600', color: '#1e3a8a', minWidth: '80px', textAlign: 'center' }}>
                Page {currentPage}
              </span>
              <button
                onClick={() => fetchRecords(selectedDataset.id, currentPage + 1)}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '600',
                  transition: 'background-color 0.3s ease'
                }}
              >
                Next →
              </button>
            </div>
          </div>
        </>
        )}
      </div>
    </div>
  )
}
