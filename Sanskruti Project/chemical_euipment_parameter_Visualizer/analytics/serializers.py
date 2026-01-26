from rest_framework import serializers

from .models import EquipmentDataset, EquipmentRecord


class EquipmentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentRecord
        fields = (
            'id',
            'equipment_name',
            'equipment_type',
            'flowrate',
            'pressure',
            'temperature',
        )


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentDataset
        fields = (
            'id',
            'name',
            'filename',
            'uploaded_at',
            'row_count',
            'columns',
            'summary',
        )
