from django.db import models


class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class ProgramContentFile(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='programs/')
    label = models.CharField(max_length=200, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-end_date', 'id']

    def __str__(self) -> str:
        return self.label or self.file.name

    @property
    def is_pdf(self) -> bool:
        return self.file.name.lower().endswith('.pdf')


class ProgramContentSchedule(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='schedules')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['start_date', 'end_date', 'id']

    def __str__(self) -> str:
        if self.end_date:
            return f"{self.start_date} - {self.end_date}"
        return str(self.start_date)


class ProgramContentScheduleList(models.Model):
    schedule = models.ForeignKey(ProgramContentSchedule, on_delete=models.CASCADE, related_name='items')
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ['start_time', 'end_time', 'id']

    def __str__(self) -> str:
        if self.end_time:
            return f"{self.start_time} - {self.end_time}"
        return str(self.start_time)
