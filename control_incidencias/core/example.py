def exists_requerimiento(codigo):
    try:
        Requerimiento.objects.get(codigo=codigo)                
        return True
    except Requerimiento.DoesNotExist:
        return False

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
        
    requerimientos = stado.objects.filter(codigo__contains=filter)
    context['filter'] = filter
    context['requerimientos'] = requerimientos
    
    return render(request, 'admin/requerimiento/index.html', context)
    

@login_required
@role_required('admin')
def requerimiento_create(request):
    context = {}
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo')
            descripcion = request.POST.get('descripcion')
            
            if exists_requerimiento(codigo):
                raise Exception('Ya existe un requerimiento con el mismo codigo')
                      
            Requerimiento.objects.create(codigo=codigo, descripcion=descripcion)
            
            context['success'] = 'Requerimiento registrado' 
            
        except Exception as e:
            context['error'] = e.__str__ 
            
    return render(request, 'admin/requerimiento/create.html', context)

@login_required
@role_required('admin')
def requerimiento_update(request, id):
    requerimiento = get_object_or_404(Requerimiento, pk=id)
    context = {}    
    
    if request.method == 'POST':
        try:
            requerimiento.codigo = request.POST.get('codigo')
            requerimiento.descripcion = request.POST.get('descripcion')
            requerimiento.save()
            
            request.session['success'] = 'Requerimiento actualizado'

            return redirect('requerimiento_index')
        except Exception as e:
            context['error'] = e.__str__
    context['requerimiento'] = requerimiento
    return render(request, 'admin/requerimiento/edit.html', context)

@login_required
@role_required('admin')
def requerimiento_delete(request, id):
    requerimiento = get_object_or_404(Requerimiento, pk=id)
    try:
        requerimiento.delete()
        request.session['success'] = 'Requerimiento eliminado'
    except Exception as e:
        request.session['error'] = 'No se pudo eliminar el requerimiento' + e.__str__
    
    return redirect('requerimiento_index')