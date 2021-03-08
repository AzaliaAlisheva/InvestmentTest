from django.db import models


class Stocks(models.Model):
    name = models.CharField(max_length=20)
    pc = models.FloatField(default=0, blank=True)

    def __str__(self):
        return str(self.name)