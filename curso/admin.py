from django.contrib import admin
from curso.models import Curso

class CursoAdmin(admin.ModelAdmin):

    list_display = ('nome_curso', 'value')
admin.site.register(Curso, CursoAdmin)
