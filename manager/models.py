from django.db import models


class Disk(models.Model):
    """Модель диска"""

    choices = (
        ('mount', 'mount'),
        ('umount', 'umount'),
    )

    name = models.CharField(max_length=200, unique=True, blank=False)
    size = models.IntegerField('Disk size in Gb')
    mount_point = models.CharField(max_length=300, unique=True,
                                   blank=True, null=True)
    mount_state = models.CharField(max_length=7, choices=choices)
    format = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, {self.size}, {self.mount_point}'
