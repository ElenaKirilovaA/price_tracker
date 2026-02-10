from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import MinValueValidator, MinLengthValidator


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('title', models.CharField(
                    unique=True,
                    max_length=100,
                    validators=[MinLengthValidator(2)]
                )),
                ('description', models.TextField(
                    blank=True,
                    null=True
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),

                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
                ('url', models.URLField()),
                ('current_price', models.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    validators=[MinValueValidator(0.01)]
                )),
                ('updated_at', models.DateTimeField(auto_now=True)),


                ('category', models.ForeignKey(
                    to='catalog.Category',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='products'
                )),
                ('tag', models.ManyToManyField(
                    to='catalog.Tag',
                    related_name='products',
                    blank=True
                )),
            ],
        ),
    ]
