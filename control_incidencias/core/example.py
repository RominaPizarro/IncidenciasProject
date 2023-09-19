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
        
    estados = stado.objects.filter(nombre__contains=filter)
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
            context['error'] = e.__str__ 
            
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
            context['error'] = e.__str__
    context['estado'] = estado
    return render(request, 'admin/estado/edit.html', context)

@login_required
@role_required('admin')
def estado_delete(request, id):
    estado = get_object_or_404(Estado, pk=id)
    try:
        estado.delete()
        request.session['success'] = 'Estado eliminado'
    except Exception as e:
        request.session['error'] = 'No se pudo eliminar el estado' + e.__str__
    
    return redirect('estado_index')