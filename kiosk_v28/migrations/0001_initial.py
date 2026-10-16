from django.db import migrations,models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[migrations.CreateModel(name='V28Snapshot',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),('singleton',models.PositiveSmallIntegerField(default=1,unique=True)),('data',models.JSONField(default=dict)),('revision',models.PositiveBigIntegerField(default=0)),('updated_at',models.DateTimeField(auto_now=True))]) ]
