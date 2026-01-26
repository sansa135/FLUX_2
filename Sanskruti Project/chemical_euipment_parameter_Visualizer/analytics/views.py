from io import BytesIO
from typing import Dict, List

import pandas as pd
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EquipmentDataset, EquipmentRecord
from .serializers import EquipmentDatasetSerializer, EquipmentRecordSerializer


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
	column_map = {col.lower().strip(): col for col in df.columns}
	required = {
		'equipment name': None,
		'type': None,
		'flowrate': None,
		'pressure': None,
		'temperature': None,
	}

	resolved: Dict[str, str] = {}
	for required_col in required:
		if required_col in column_map:
			resolved[required_col] = column_map[required_col]
		else:
			raise ValueError(f"Missing required column: {required_col}")

	return pd.DataFrame(
		{
			'equipment_name': df[resolved['equipment name']],
			'equipment_type': df[resolved['type']],
			'flowrate': pd.to_numeric(df[resolved['flowrate']], errors='coerce'),
			'pressure': pd.to_numeric(df[resolved['pressure']], errors='coerce'),
			'temperature': pd.to_numeric(df[resolved['temperature']], errors='coerce'),
		}
	)


def _numeric_summary(series: pd.Series) -> Dict[str, float]:
	clean = series.dropna()
	if clean.empty:
		return {'min': None, 'max': None, 'mean': None, 'median': None}
	return {
		'min': float(clean.min()),
		'max': float(clean.max()),
		'mean': float(round(clean.mean(), 3)),
		'median': float(round(clean.median(), 3)),
	}


def _build_summary(df: pd.DataFrame) -> Dict[str, object]:
	type_counts = df['equipment_type'].fillna('Unknown').value_counts().to_dict()
	return {
		'row_count': len(df),
		'type_distribution': type_counts,
		'flowrate': _numeric_summary(df['flowrate']),
		'pressure': _numeric_summary(df['pressure']),
		'temperature': _numeric_summary(df['temperature']),
	}


def _trim_old_datasets(limit: int = 5) -> None:
	extra = EquipmentDataset.objects.order_by('-uploaded_at')[limit:]
	for dataset in extra:
		dataset.delete()


class UploadDatasetView(APIView):
	def post(self, request):
		upload = request.FILES.get('file')
		if not upload:
			return Response({'detail': 'Please provide a CSV file in the "file" form field.'}, status=status.HTTP_400_BAD_REQUEST)

		raw_bytes = upload.read()
		try:
			df = pd.read_csv(BytesIO(raw_bytes))
		except Exception as exc:  # pragma: no cover - pass pandas error upstream
			return Response({'detail': f'Could not read CSV: {exc}'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			normalized_df = _normalize_columns(df)
		except ValueError as exc:
			return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

		normalized_df = normalized_df.dropna(how='all')
		summary = _build_summary(normalized_df)

		dataset = EquipmentDataset.objects.create(
			name=request.data.get('name') or upload.name,
			filename=upload.name,
			row_count=len(normalized_df),
			columns=list(normalized_df.columns),
			summary=summary,
		)

		records: List[EquipmentRecord] = []
		for row in normalized_df.to_dict(orient='records'):
			records.append(
				EquipmentRecord(
					dataset=dataset,
					equipment_name=row.get('equipment_name') or '',
					equipment_type=row.get('equipment_type') or '',
					flowrate=row.get('flowrate'),
					pressure=row.get('pressure'),
					temperature=row.get('temperature'),
				)
			)

		EquipmentRecord.objects.bulk_create(records, batch_size=500)

		dataset.raw_file.save(upload.name, ContentFile(raw_bytes))
		_trim_old_datasets()

		serializer = EquipmentDatasetSerializer(dataset)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class EquipmentDatasetListView(APIView):
	def get(self, request):
		datasets = EquipmentDataset.objects.all()[:5]
		serializer = EquipmentDatasetSerializer(datasets, many=True)
		return Response(serializer.data)


class LatestDatasetView(APIView):
	def get(self, request):
		dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()
		if not dataset:
			return Response({'detail': 'No datasets uploaded yet.'}, status=status.HTTP_404_NOT_FOUND)
		serializer = EquipmentDatasetSerializer(dataset)
		return Response(serializer.data)


class EquipmentRecordListView(PageNumberPagination, APIView):
	page_size = 25

	def get(self, request, dataset_id: int):
		dataset = get_object_or_404(EquipmentDataset, pk=dataset_id)
		queryset = dataset.records.all().order_by('id')
		page = self.paginate_queryset(queryset, request, view=self)
		serializer = EquipmentRecordSerializer(page, many=True)
		return self.get_paginated_response(serializer.data)


class EquipmentDatasetSummaryView(APIView):
	def get(self, request, dataset_id: int):
		dataset = get_object_or_404(EquipmentDataset, pk=dataset_id)
		return Response({'dataset': EquipmentDatasetSerializer(dataset).data, 'summary': dataset.summary})
