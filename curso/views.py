from django.shortcuts import render
from curso.models import Curso
from django.views.generic import DetailView

def curso_view(request):
    
        
    cursos = Curso.objects.all()
    

    query = request.GET.get("q")
    if query:
        sql = f"SELECT * FROM curso_curso WHERE nome_curso LIKE '%{query}%'" 
        
        cursos = Curso.objects.raw(sql)

    return render(request, 'curso.html', {'cursos': cursos, 'user':request.user})

class CouseDetailView(DetailView):
    model = Curso
    template_name = 'base_generic.html'


