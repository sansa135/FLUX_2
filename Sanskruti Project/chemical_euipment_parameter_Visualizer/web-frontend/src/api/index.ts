import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface EquipmentRecord {
  id: number
  equipment_name: string
  equipment_type: string
  flowrate: number | null
  pressure: number | null
  temperature: number | null
}

export interface DatasetSummary {
  row_count: number
  type_distribution: Record<string, number>
  flowrate: { min: number | null; max: number | null; mean: number; median: number }
  pressure: { min: number | null; max: number | null; mean: number; median: number }
  temperature: { min: number | null; max: number | null; mean: number; median: number }
}

export interface EquipmentDataset {
  id: number
  name: string
  filename: string
  uploaded_at: string
  row_count: number
  columns: string[]
  summary: DatasetSummary
}

export const uploadDataset = (file: File, name?: string) => {
  const formData = new FormData()
  formData.append('file', file)
  if (name) formData.append('name', name)
  return api.post<EquipmentDataset>('/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const getDatasets = () => api.get<EquipmentDataset[]>('/datasets/')

export const getLatestDataset = () => api.get<EquipmentDataset>('/datasets/latest/')

export const getDatasetRecords = (datasetId: number, page: number = 1) =>
  api.get<{ count: number; next: string | null; previous: string | null; results: EquipmentRecord[] }>(
    `/datasets/${datasetId}/records/?page=${page}`
  )

export const getDatasetSummary = (datasetId: number) =>
  api.get<{ dataset: EquipmentDataset; summary: DatasetSummary }>(`/datasets/${datasetId}/summary/`)
