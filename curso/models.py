from django.db import models


def validate_any_file(value):
    pass

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nome_curso = models.CharField(max_length=200)
    value = models.FloatField(blank=True, null=True)
    foto = models.FileField(upload_to='cursos/', blank=True, null=True, validators=[validate_any_file])
    

    def __str__(self):
        return self.nome_curso
