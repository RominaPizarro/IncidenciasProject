from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .decorators import role_required

from .models import Usuario, Area, Estado, Requerimiento
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.db.models import Q
from django.utils import timezone
from django.utils import dateformat

# Create your views here.


def index(request):
    return render(request, 'index.html')

#AUTH

def login_view(request):
    return render(request, 'auth/login.html')

def reset_password(request):
    
    context = {}
    
    if request.method == 'POST':         
        try:       
            username = request.POST.get('username')
            email = request.POST.get('email')
            
            user = User.objects.get(Q(username=username) & Q(email=email))          
            
            return redirect('change_password', user_id=user.id)
        except Exception as e:
            context = { 'error': 'No se econtró información con los datos ingresados' }
    
    return render(request, 'auth/reset-password.html', context)

def change_password(request, user_id):
    context = {}
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':         
        try:       
            user.set_password(request.POST.get('password'))
            user.save()       
            
            return redirect('login')
        except Exception as e:
            context = { 'error': 'No se pudo cambiar la contraseña' }
    
    context['user'] = user
    return render(request, 'auth/change-password.html', context)

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
            request.session['usuario_username'] = profile.user.username
            request.session['usuario_id'] = profile.id
            
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
            context = { 'error': e.__str__() }
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
def usuario_perfil_admin(request):
    usuario_id = request.session['usuario_id']        
    usuario = Usuario.objects.get(pk=usuario_id)
    
    context = {}
    
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=usuario.user.id)
            user.first_name = request.POST.get('nombres')
            user.last_name = request.POST.get('apellidos')
            user.email = request.POST.get('email')
            user.save()
            
            usuario.telefono = request.POST.get('telefono')
            usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            usuario.save()
            
            request.session['success'] = 'Perfil actualizado'
            
            return redirect('usuario_index')

        except Exception as e:
            context['error'] = 'Error actualizando el perfil. ' + e.__str__()
    
    context['usuario'] = usuario 
    return render(request, 'admin/perfil.html', context)

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
        
    usuarios = Usuario.objects.filter(rut__startswith=filter)
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
            context['error'] = 'No se pudo registrar el usuario. ' + e.__str__() 
            
    return render(request, 'admin/usuario/create.html', context)

@login_required
@role_required('admin')
def usuario_update(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=usuario.user.id)
            user.first_name = request.POST.get('nombres')
            user.last_name = request.POST.get('apellidos')
            user.email = request.POST.get('email')
            user.save()
            
            usuario.telefono = request.POST.get('telefono')
            usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            usuario.role = request.POST.get('role')
            usuario.save()
            
            request.session['success'] = 'Usuario actualizado'

            return redirect('usuario_index')
        except Exception as e:
            context['error'] = 'Error actualizando el usuario. ' + e.__str__()
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
        request.session['error'] = 'No se pudo eliminar el usuario. ' + e.__str__()
    
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
        
    areas = Area.objects.filter(nombre__startswith=filter)
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
            context['error'] = 'No se pudo registrar el área. ' + e.__str__() 
            
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
            context['error'] = 'Error actualizando el área. ' + e.__str__()
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
        request.session['error'] = 'No se pudo eliminar el area. ' + e.__str__()
    
    return redirect('area_index')

#ESTADO
def exists_estado(nombre):
    try:
        Estado.objects.get(nombre=nombre)                
        return True
    except Estado.DoesNotExist:
        return False

@login_required
@role_required('admin')
def estado_index(request):
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
        
    estados = Estado.objects.filter(nombre__startswith=filter)
    context['filter'] = filter
    context['estados'] = estados
    
    return render(request, 'admin/estado/index.html', context)
    

@login_required
@role_required('admin')
def estado_create(request):
    context = {}
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            
            if exists_estado(nombre):
                raise Exception('Ya existe un estado con el mismo nombre')
                      
            Estado.objects.create(nombre=nombre, descripcion=descripcion)
            
            context['success'] = 'Estado registrado' 
            
        except Exception as e:
            context['error'] = 'No se pudo registrar el estado. ' + e.__str__() 
            
    return render(request, 'admin/estado/create.html', context)

@login_required
@role_required('admin')
def estado_update(request, id):
    estado = get_object_or_404(Estado, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            estado.nombre = request.POST.get('nombre')
            estado.descripcion = request.POST.get('descripcion')
            estado.save()
            
            request.session['success'] = 'Estado actualizado'

            return redirect('estado_index')
        except Exception as e:
            context['error'] = e.__str__()
    context['estado'] = 'Error actualizando estado. ' + estado
    return render(request, 'admin/estado/edit.html', context)

@login_required
@role_required('admin')
def estado_delete(request, id):
    estado = get_object_or_404(Estado, pk=id)
    try:
        estado.delete()
        request.session['success'] = 'Estado eliminado'
    except Exception as e:
        request.session['error'] = 'No se pudo eliminar el estado. ' + e.__str__()
    
    return redirect('estado_index')

#REQUERIMIENTO

@login_required
@role_required('admin')
def requerimiento_index(request):
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
       
    requerimientos = Requerimiento.objects.filter(
        Q(codigo__startswith=filter) | 
        Q(estado__nombre__startswith=filter) | 
        Q(area__nombre__startswith=filter) | 
        Q(usuario_reporta__rut__startswith=filter) |
        Q(usuario_asignado__rut__startswith=filter)
        )
    context['filter'] = filter
    context['requerimientos'] = requerimientos
    
    return render(request, 'admin/requerimiento/index.html', context)
    

@login_required
@role_required('admin')
def requerimiento_create(request):
    context = {}
    if request.method == 'POST':
        try:
            codigo = timezone.now().strftime("%Y%m%d%H%M%S")
            descripcion = request.POST.get('descripcion')
            usuario_reporta_id = request.POST.get('usuario_reporta_id')
            area_id = request.POST.get('area_id')
            estado_id = request.POST.get('estado_id')
            
            usuario_reporta = Usuario.objects.get(pk=usuario_reporta_id)
            area = Area.objects.get(pk=area_id)
            estado = Estado.objects.get(pk=estado_id)
                      
            Requerimiento.objects.create(
                codigo=codigo, 
                descripcion=descripcion,
                usuario_reporta=usuario_reporta,
                area=area,
                usuario_asignado=None,
                estado=estado,
                observaciones=None
                )
            
            context['success'] = 'Requerimiento registrado' 
            
        except Exception as e:
            context['error'] = 'Error creando requerimiento. ' + e.__str__()
    
    context['usuarios'] = Usuario.objects.all()
    context['areas'] = Area.objects.all()
    context['estados'] = Estado.objects.all()
            
    return render(request, 'admin/requerimiento/create.html', context)

@login_required
@role_required('admin')
def requerimiento_update(request, id):
    requerimiento = get_object_or_404(Requerimiento, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            requerimiento.descripcion = request.POST.get('descripcion')
            usuario_reporta_id = request.POST.get('usuario_reporta_id')
            area_id = request.POST.get('area_id')
            usuario_asignado_id = request.POST.get('usuario_asignado_id')
            estado_id = request.POST.get('estado_id')
            requerimiento.observaciones = request.POST.get('observaciones')
            
            requerimiento.usuario_reporta = Usuario.objects.get(pk=usuario_reporta_id)
            requerimiento.area = Area.objects.get(pk=area_id)
            if usuario_asignado_id is not None and int(usuario_asignado_id) > 0 :
                requerimiento.usuario_asignado = Usuario.objects.get(pk=usuario_asignado_id)
            requerimiento.estado = Estado.objects.get(pk=estado_id)
            requerimiento.save()
            
            request.session['success'] = 'Requerimiento actualizado'

            return redirect('requerimiento_index')
        except Exception as e:
            context['error'] = 'Error actualizando requerimiento' + e.__str__()
    
    context['requerimiento'] = requerimiento
    context['usuarios'] = Usuario.objects.all()
    context['areas'] = Area.objects.all()
    context['estados'] = Estado.objects.all()
    
    return render(request, 'admin/requerimiento/edit.html', context)

@login_required
@role_required('admin')
def requerimiento_asignar(request, id):
    requerimiento = get_object_or_404(Requerimiento, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            usuario_asignado_id = request.POST.get('usuario_asignado_id')
            estado_id = request.POST.get('estado_id')
            
            requerimiento.usuario_asignado = Usuario.objects.get(pk=usuario_asignado_id)
            requerimiento.estado = Estado.objects.get(pk=estado_id)
            requerimiento.save()
            
            request.session['success'] = 'Requerimiento asignado'

            return redirect('requerimiento_index')
        except Exception as e:
            context['error'] = 'Error asignando requerimiento a usuario. ' + e.__str__()
    
    context['requerimiento'] = requerimiento
    context['usuarios'] = Usuario.objects.all()
    context['estados'] = Estado.objects.all()
    
    return render(request, 'admin/requerimiento/asignar.html', context)

@login_required
@role_required('admin')
def requerimiento_delete(request, id):
    requerimiento = get_object_or_404(Requerimiento, pk=id)
    try:
        requerimiento.delete()
        request.session['success'] = 'Requerimiento eliminado'
    except Exception as e:
        request.session['error'] = 'No se pudo eliminar el requerimiento. ' + e.__str__()
    
    return redirect('requerimiento_index')

#CLIENTE

@login_required
@role_required('cliente')
def dashboard_cliente(request):
    return render(request, 'cliente/dashboard.html')

@login_required
@role_required('cliente')
def usuario_perfil(request):
    usuario_id = request.session['usuario_id']        
    usuario = Usuario.objects.get(pk=usuario_id)
    
    context = {}
    
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=usuario.user.id)
            user.first_name = request.POST.get('nombres')
            user.last_name = request.POST.get('apellidos')
            user.email = request.POST.get('email')
            user.save()
            
            usuario.telefono = request.POST.get('telefono')
            usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            usuario.save()
            
            request.session['success'] = 'Perfil actualizado'
            
            return redirect('mis_requerimientos')

        except Exception as e:
            context['error'] = 'Error actualizando el perfil. ' + e.__str__()
    
    context['usuario'] = usuario 
    return render(request, 'cliente/perfil.html', context)

@login_required
@role_required('cliente')
def mis_requerimientos(request):
    usuario_id = request.session['usuario_id']
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
       
    requerimientos = Requerimiento.objects.filter(
        Q(usuario_asignado_id=usuario_id) & (
        Q(codigo__startswith=filter) | 
        Q(estado__nombre__startswith=filter) | 
        Q(area__nombre__startswith=filter) | 
        Q(usuario_reporta__rut__startswith=filter)
        )
        )
    context['filter'] = filter
    context['requerimientos'] = requerimientos
    
    return render(request, 'cliente/mis-requerimientos.html', context)

@login_required
@role_required('cliente')
def requerimiento_atender(request, id):
    requerimiento = get_object_or_404(Requerimiento, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            requerimiento.observaciones = request.POST.get('observaciones')
            estado_id = request.POST.get('estado_id')
            
            requerimiento.estado = Estado.objects.get(pk=estado_id)
            requerimiento.save()
            
            request.session['success'] = 'Requerimiento atendido'

            return redirect('mis_requerimientos')
        except Exception as e:
            context['error'] = 'Error atendiendo requerimiento. ' + e.__str__()
    
    context['estados'] = Estado.objects.all()
    context['requerimiento'] = requerimiento
    
    return render(request, 'cliente/atender-requerimiento.html', context)

@login_required
@role_required('cliente')
def requerimiento_nuevo(request):
    context = {}
    if request.method == 'POST':
        try:
            codigo = timezone.now().strftime("%Y%m%d%H%M%S")
            descripcion = request.POST.get('descripcion')
            usuario_reporta_id = request.session['usuario_id']
            area_id = request.POST.get('area_id')
            estado_id = request.POST.get('estado_id')
            
            usuario_reporta = Usuario.objects.get(pk=usuario_reporta_id)
            area = Area.objects.get(pk=area_id)
            estado = Estado.objects.get(pk=estado_id)
                      
            Requerimiento.objects.create(
                codigo=codigo, 
                descripcion=descripcion,
                usuario_reporta=usuario_reporta,
                area=area,
                usuario_asignado=None,
                estado=estado,
                observaciones=None
                )
            
            context['success'] = 'Se envió el requerimiento al Administrador' 
            
        except Exception as e:
            context['error'] = 'Error creando requerimiento. ' + e.__str__()
    
    context['areas'] = Area.objects.all()
    context['estados'] = Estado.objects.all()
    
    return render(request, 'cliente/nuevo-requerimiento.html', context)
