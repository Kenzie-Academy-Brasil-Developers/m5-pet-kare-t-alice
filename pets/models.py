from django.db import models


# Create your models here.
class SexChoice(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    DEFAULT = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=4, decimal_places=2)

    group = models.ForeignKey(
        "groups.Group", 
        on_delete=models.PROTECT, 
        related_name="pets"
    )
    sex = models.CharField(
        max_length=20,
        choices=SexChoice.choices,
        default=SexChoice.DEFAULT
    )
    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="pets",
    )
