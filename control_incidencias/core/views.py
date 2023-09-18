from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import role_required

from .models import Usuario
from django.contrib.auth.models import User

from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'auth/login.html')

def reset_password(request):
    return render(request, 'auth/reset-password.html')

def inicio_sesion(request): 
    
    messages.success(request, 'bienvendio a la pagina de inicio de sesion')
    
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            profile = Usuario.objects.get(user=user)
            
            request.session['perfil'] = profile.role            
            
            login(request, user)
            
            if profile.role == 'admin':
                return redirect('dashboard_admin')
            elif profile.role == 'cliente':
                return redirect('dashboard_cliente')
            else:
                context = {
                'error' : 'El usuario no tiene rol válido'
                }
                return render(request, 'auth/login.html', context)
        else:
            context = {
                'error' : 'Credenciales incorrectas'
            }
            return render(request, 'auth/login.html', context)
        
    return render(request, 'auth/login.html')

@role_required('cliente','admin')
def logout_view(request):
    logout(request)
    return redirect('inicio_sesion')

def register(request):
    if request.method == 'POST':        
        first_name = request.POST.get('nombres')
        last_name = request.POST.get('apellidos')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        rut = request.POST.get('rut')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        role = 'cliente'
        
        Usuario.objects.create(user=user, role=role, rut=rut, telefono=telefono, fecha_nacimiento=fecha_nacimiento)
        
        return redirect('login_view')
    return render(request, 'auth/register.html')

#ADMIN
@login_required
#@role_required('admin')
def dashboardAdmin(request):
    return render(request, 'admin/index.html')


# @login_required
def usuario_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        role = 'cliente'
        
        Usuario.objects.create(user=user, role=role) 

        return redirect('usuario_list')
    return render(request, 'usuarios/create.html')

# @login_required
def usuario_update(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.save()

        # role = request.POST.get('role')
        # user_profile.role = role
        # user_profile.save() 

        return redirect('usuario_list')
    context = {'usuario': usuario}
    return render(request, 'usuarios/update.html', context)

# @login_required
def usuario_delete(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    context = {'usuario': usuario}
    return render(request, 'usuarios/delete.html', context)


#CLIENTE

#@role_required('cliente')
@login_required
def dashboardCliente(request):
    return render(request, 'cliente/index.html')

