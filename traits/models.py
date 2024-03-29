from django.db import models


# Create your models here.
class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __repr__(self) -> str:
        return f"<Trait{self.name}>"
