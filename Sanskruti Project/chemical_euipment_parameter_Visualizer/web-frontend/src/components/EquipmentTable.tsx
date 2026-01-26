import { EquipmentRecord } from '../api/index'

interface EquipmentTableProps {
  records: EquipmentRecord[]
}

export const EquipmentTable = ({ records }: EquipmentTableProps) => {
  return (
    <div style={{ overflowX: 'auto', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        fontSize: '13px'
      }}>
        <thead>
          <tr style={{ backgroundColor: '#1e3a8a' }}>
            <th style={{
              padding: '15px',
              textAlign: 'left',
              color: 'white',
              fontWeight: '600',
              borderBottom: '2px solid #1e3a8a'
            }}>Equipment Name</th>
            <th style={{
              padding: '15px',
              textAlign: 'left',
              color: 'white',
              fontWeight: '600',
              borderBottom: '2px solid #1e3a8a'
            }}>Type</th>
            <th style={{
              padding: '15px',
              textAlign: 'center',
              color: 'white',
              fontWeight: '600',
              borderBottom: '2px solid #1e3a8a'
            }}>Flowrate</th>
            <th style={{
              padding: '15px',
              textAlign: 'center',
              color: 'white',
              fontWeight: '600',
              borderBottom: '2px solid #1e3a8a'
            }}>Pressure</th>
            <th style={{
              padding: '15px',
              textAlign: 'center',
              color: 'white',
              fontWeight: '600',
              borderBottom: '2px solid #1e3a8a'
            }}>Temperature</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record, idx) => (
            <tr key={record.id} style={{
              backgroundColor: idx % 2 === 0 ? '#f9fafb' : 'white',
              borderBottom: '1px solid #e5e7eb',
              transition: 'background-color 0.2s ease'
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#f0f4ff')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = idx % 2 === 0 ? '#f9fafb' : 'white')}
            >
              <td style={{ padding: '12px 15px', color: '#1e3a8a', fontWeight: '500' }}>{record.equipment_name}</td>
              <td style={{ padding: '12px 15px', color: '#666' }}>
                <span style={{
                  padding: '4px 12px',
                  backgroundColor: '#dbeafe',
                  color: '#1e40af',
                  borderRadius: '6px',
                  fontSize: '12px',
                  fontWeight: '600'
                }}>{record.equipment_type}</span>
              </td>
              <td style={{ padding: '12px 15px', color: '#666', textAlign: 'center' }}>{record.flowrate ? record.flowrate.toFixed(2) : 'N/A'}</td>
              <td style={{ padding: '12px 15px', color: '#666', textAlign: 'center' }}>{record.pressure ? record.pressure.toFixed(2) : 'N/A'}</td>
              <td style={{ padding: '12px 15px', color: '#666', textAlign: 'center' }}>{record.temperature ? record.temperature.toFixed(2) : 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {records.length === 0 && (
        <div style={{
          padding: '30px',
          textAlign: 'center',
          color: '#999'
        }}>
          📭 No records found. Upload a CSV file to get started.
        </div>
      )}
    </div>
  )
}
