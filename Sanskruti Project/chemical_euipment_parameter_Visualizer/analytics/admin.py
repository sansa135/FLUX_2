from django.contrib import admin

from .models import EquipmentDataset, EquipmentRecord


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
	list_display = ('name', 'filename', 'row_count', 'uploaded_at')
	search_fields = ('name', 'filename')
	readonly_fields = ('uploaded_at', 'row_count')


@admin.register(EquipmentRecord)
class EquipmentRecordAdmin(admin.ModelAdmin):
	list_display = ('equipment_name', 'equipment_type', 'dataset')
	list_filter = ('equipment_type',)
	search_fields = ('equipment_name',)
