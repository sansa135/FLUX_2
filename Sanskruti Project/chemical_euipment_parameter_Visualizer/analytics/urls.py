from django.urls import path

from .views import (
    EquipmentDatasetListView,
    EquipmentDatasetSummaryView,
    EquipmentRecordListView,
    LatestDatasetView,
    UploadDatasetView,
)

urlpatterns = [
    path('upload/', UploadDatasetView.as_view(), name='upload-dataset'),
    path('datasets/', EquipmentDatasetListView.as_view(), name='dataset-list'),
    path('datasets/latest/', LatestDatasetView.as_view(), name='dataset-latest'),
    path('datasets/<int:dataset_id>/summary/', EquipmentDatasetSummaryView.as_view(), name='dataset-summary'),
    path('datasets/<int:dataset_id>/records/', EquipmentRecordListView.as_view(), name='dataset-records'),
]
