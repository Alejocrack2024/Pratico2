from django.db import models

class Oficina(models.Model):
    """Model definition for Oficina."""

    nombre = models.CharField(verbose_name="Nombre", max_length=50)
    nombre_corto = models.CharField(verbose_name="Nombre Corto", max_length=20)

    class Meta:
        """Meta definition for Oficina."""

        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'

    def __str__(self):
        """Unicode representation of Oficina."""
        return f"{self.nombre} {self.nombre_corto}"
