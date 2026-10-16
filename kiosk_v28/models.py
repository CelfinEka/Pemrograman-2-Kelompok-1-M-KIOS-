from django.db import models
class V28Snapshot(models.Model):
    singleton=models.PositiveSmallIntegerField(default=1,unique=True)
    data=models.JSONField(default=dict)
    revision=models.PositiveBigIntegerField(default=0)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name='V28 persistent state'
    def __str__(self):
        return f'V28 rev {self.revision}'
