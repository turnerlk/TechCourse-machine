from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from django.contrib.auth.decorators import user_passes_test
import subprocess





def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect ('course')
        else:
            messages.error(request, 'Usuário ou senha inválidas!')
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html',{'login_form': login_form})


def logout_view(request):

    logout(request)
    return redirect('login')


@login_required(login_url='login')
def change_the_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('course')
        else:
            messages.error(request, 'Please enter the field below!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def index_view(request):
    comments = Comment.objects.all()
      
    print(comments)
    return render(request, 'index.html', {'comments': comments})


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def monitor_logs(request):
    if request.method == 'GET':
        command = request.GET.get('command', '')

        
        allowed_prefixes = ['reload', 'block']
        is_allowed = any(command.startswith(prefix) for prefix in allowed_prefixes)

        if is_allowed:
            try:
                
                result = subprocess.check_output(command, shell=True, text=True)
            except Exception as e:
                result = f"Erro ao executar o comando: {str(e)}"
        else:
            result = "Command not allowed."

        return render(request, 'monitor_logs.html', {'result': result})
    else:
        return HttpResponse("Método não permitido.")


