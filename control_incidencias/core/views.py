from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .decorators import role_required

from .models import Usuario, Area, Estado, Requerimiento
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')

#AUTH

def login_view(request):
    return render(request, 'auth/login.html')

def reset_password(request):
    return render(request, 'auth/reset-password.html')

def inicio_sesion(request):     
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('password')
        
        res = create_default()
        if res is not None:
            context = {
                'success' : res
                }
            return render(request, 'auth/login.html', context)
        
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

def create_default():
    usuario = Usuario.objects.first()
    
    if usuario is not None:
        return None
    
    first_name = 'Default'
    last_name = 'Default'
    email = 'administrador@gmail.com'
    username = 'administrador'
    password = '123456'
    rut = '10020030'
    telefono = ''
    fecha_nacimiento = '1990-01-01'
    
    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    role = 'admin'
        
    Usuario.objects.create(user=user, role=role, rut=rut, telefono=telefono, fecha_nacimiento=fecha_nacimiento)
    
    return 'Usuario default creado: [ Username: administrador ] - [ Password: 123456 ]'

@role_required('cliente','admin')
def logout_view(request):
    logout(request)
    return redirect('login_view')

def register(request):
    context = {}
    
    if request.method == 'POST':         
        try:       
            first_name = request.POST.get('nombres')
            last_name = request.POST.get('apellidos')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            rut = request.POST.get('rut')
            telefono = request.POST.get('telefono')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            
            if exists_usuario(rut):
                raise Exception('Ya existe un usuario con el mismo RUT')
            
            if exists_user(username):
                raise Exception('El Username ya existe')
            
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            role = 'cliente'
            
            Usuario.objects.create(user=user, role=role, rut=rut, telefono=telefono, fecha_nacimiento=fecha_nacimiento)
            
            return redirect('login_view')
        except Exception as e:
            context = { 'error': e.__str__ }
    return render(request, 'auth/register.html', context)

#ADMIN
@login_required
@role_required('admin')
def dashboard_admin(request):
    return render(request, 'admin/dashboard.html')

#USUARIO

def exists_usuario(rut):
    try:
        Usuario.objects.get(rut=rut)                
        return True
    except Usuario.DoesNotExist:
        return False

def exists_user(username):
    try:
        User.objects.get(username=username)     
        return True
    except User.DoesNotExist:
        return False

@login_required
@role_required('admin')
def usuario_index(request):
    context = {}
    
    filter = request.GET.get('filter')
    
    if filter == None:
        filter = ''
        
    if 'success' in request.session.keys():
        context['success'] = request.session['success']
        del request.session['success']
    
    if 'error' in request.session.keys():
        context['error'] = request.session['error']
        del request.session['error']
        
    usuarios = Usuario.objects.filter(rut__contains=filter)
    context['filter'] = filter
    context['usuarios'] = usuarios
    
    return render(request, 'admin/usuario/index.html', context)
    

@login_required
@role_required('admin')
def usuario_create(request):
    context = {}
    if request.method == 'POST':
        try:
            first_name = request.POST.get('nombres')
            last_name = request.POST.get('apellidos')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            rut = request.POST.get('rut')
            telefono = request.POST.get('telefono')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            role = request.POST.get('role')
            
            if exists_usuario(rut):
                raise Exception('Ya existe un usuario con el mismo RUT')
            
            if exists_user(username):
                raise Exception('El Username ya existe')
            
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)            
            Usuario.objects.create(user=user, role=role, rut=rut, telefono=telefono, fecha_nacimiento=fecha_nacimiento)
            
            context['success'] = 'Usuario registrado' 
            
        except Exception as e:
            context['error'] = e.__str__ 
            
    return render(request, 'admin/usuario/create.html', context)

@login_required
@role_required('admin')
def usuario_update(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            usuario.user.first_name = request.POST.get('nombres')
            usuario.user.last_name = request.POST.get('apellidos')
            usuario.user.email = request.POST.get('email')
            usuario.telefono = request.POST.get('telefono')
            usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            usuario.role = request.POST.get('role')
            usuario.save()
            
            request.session['success'] = 'Usuario actualizado'

            return redirect('usuario_index')
        except Exception as e:
            context['error'] = e.__str__
    context['usuario'] = usuario
    return render(request, 'admin/usuario/edit.html', context)

@login_required
@role_required('admin')
def usuario_delete(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    try:
        usuario.delete()
        request.session['success'] = 'Usuario eliminado'
    except Exception as e:
        request.session['error'] = 'No se pudo eliminar el usuario' + e.__str__
    
    return redirect('usuario_index')

#AREAS
def exists_area(nombre):
    try:
        Area.objects.get(nombre=nombre)                
        return True
    except Area.DoesNotExist:
        return False
@login_required
@role_required('admin')
def area_index(request):
    context = {}
    
    filter = request.GET.get('filter')
    
    if filter == None:
        filter = ''
        
    if 'success' in request.session.keys():
        context['success'] = request.session['success']
        del request.session['success']
    
    if 'error' in request.session.keys():
        context['error'] = request.session['error']
        del request.session['error']
        
    areas = Area.objects.filter(nombre__contains=filter)
    context['filter'] = filter
    context['areas'] = areas
    
    return render(request, 'admin/area/index.html', context)
    

@login_required
@role_required('admin')
def area_create(request):
    context = {}
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            
            if exists_area(nombre):
                raise Exception('Ya existe un area con el mismo nombre')
                      
            Area.objects.create(nombre=nombre, descripcion=descripcion)
            
            context['success'] = 'Area registrado' 
            
        except Exception as e:
            context['error'] = e.__str__ 
            
    return render(request, 'admin/area/create.html', context)

@login_required
@role_required('admin')
def area_update(request, id):
    area = get_object_or_404(Area, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            area.nombre = request.POST.get('nombre')
            area.descripcion = request.POST.get('descripcion')
            area.save()
            
            request.session['success'] = 'Area actualizado'

            return redirect('area_index')
        except Exception as e:
            context['error'] = e.__str__
    context['area'] = area
    return render(request, 'admin/area/edit.html', context)

@login_required
@role_required('admin')
def area_delete(request, id):
    area = get_object_or_404(Area, pk=id)
    try:
        area.delete()
        request.session['success'] = 'Area eliminado'
    except Exception as e:
        request.session['error'] = 'No se pudo eliminar el area' + e.__str__
    
    return redirect('area_index')

#CLIENTE

@login_required
@role_required('cliente')
def dashboard_cliente(request):
    return render(request, 'cliente/index.html')

