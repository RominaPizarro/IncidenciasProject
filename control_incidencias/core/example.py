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
            area.user.nombre = request.POST.get('nombre')
            area.user.descripcion = request.POST.get('descripcion')
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
    
    redirect('area_index')