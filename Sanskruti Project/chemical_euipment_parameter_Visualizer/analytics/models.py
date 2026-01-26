from django.db import models


class EquipmentDataset(models.Model):
	name = models.CharField(max_length=255)
	filename = models.CharField(max_length=255)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	row_count = models.PositiveIntegerField(default=0)
	columns = models.JSONField(default=list, blank=True)
	summary = models.JSONField(default=dict, blank=True)
	raw_file = models.FileField(upload_to='datasets/', null=True, blank=True)

	class Meta:
		ordering = ['-uploaded_at']

	def __str__(self) -> str:  # pragma: no cover - simple display helper
		return f"{self.name} ({self.filename})"


class EquipmentRecord(models.Model):
	dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='records')
	equipment_name = models.CharField(max_length=255)
	equipment_type = models.CharField(max_length=255, blank=True)
	flowrate = models.FloatField(null=True, blank=True)
	pressure = models.FloatField(null=True, blank=True)
	temperature = models.FloatField(null=True, blank=True)

	class Meta:
		indexes = [
			models.Index(fields=['dataset']),
			models.Index(fields=['equipment_type']),
		]

	def __str__(self) -> str:  # pragma: no cover - simple display helper
		return self.equipment_name
