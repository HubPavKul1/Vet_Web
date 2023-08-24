from django.db import models


class Disease(models.Model):
    """Модель Заболевание"""
    name = models.CharField(max_length=255,
                            verbose_name='наименование болезни'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'diseases'
        verbose_name = 'disease'
        verbose_name_plural = 'diseases'
