from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.BooleanField("Estado", default=True)
    created_date = models.DateField(
        "Fecha de creación", auto_now=False, auto_now_add=True
    )
    modified_date = models.DateField(
        "Fecha de modificación", auto_now=True, auto_now_add=False
    )
    deleted_date = models.DateTimeField(
        "Fecha de eliminación",
        null=True,
        blank=True,
    )
    historical = HistoricalRecords(user_model="users.User", inherit=True)

    class Meta:
        abstract = True
        verbose_name = "BaseModel"
        verbose_name_plural = "BaseModel"

    def soft_delete(self):
        self.state = False
        self.deleted_date = timezone.now()
        self.save(update_fields=["state", "deleted_date"])
