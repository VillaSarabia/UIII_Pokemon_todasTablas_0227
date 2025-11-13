from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Pedido, Producto, SetExpansion, Carta, DetalleProducto

# ==========================================
# VISTA DE INICIO
# ==========================================
def inicio_Pokemon(request):
    return render(request, 'inicio.html')

# ==========================================
# VISTAS PARA CLIENTES
# ==========================================
def agregar_cliente(request):
    if request.method == 'POST':
        try:
            # Verificar si el email ya existe
            email = request.POST['email']
            if Cliente.objects.filter(email=email).exists():
                mensaje_error = f"El email '{email}' ya está registrado. Usa un email diferente."
                return render(request, 'clientes/agregar_cliente.html', {
                    'error_message': mensaje_error,
                    'form_data': request.POST
                })
            
            # Crear el cliente
            Cliente.objects.create(
                nombre_cliente=request.POST['nombre_cliente'],
                email=email,
                direccion=request.POST['direccion'],
                telefono=request.POST['telefono'],
                puntos_lealtad=int(request.POST['puntos_lealtad']),
                tipo_entrenador=request.POST['tipo_entrenador']
            )
            return redirect('ver_cliente')
            
        except Exception as e:
            mensaje_error = f"Error al crear el cliente: {str(e)}"
            return render(request, 'clientes/agregar_cliente.html', {
                'error_message': mensaje_error,
                'form_data': request.POST
            })
    
    return render(request, 'clientes/agregar_cliente.html')

def ver_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/ver_cliente.html', {'clientes': clientes})

def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/actualizar_cliente.html', {'cliente': cliente})

def realizar_actualizacion_cliente(request, cliente_id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.nombre_cliente = request.POST['nombre_cliente']
        cliente.email = request.POST['email']
        cliente.direccion = request.POST['direccion']
        cliente.telefono = request.POST['telefono']
        cliente.puntos_lealtad = int(request.POST['puntos_lealtad'])
        cliente.tipo_entrenador = request.POST['tipo_entrenador']
        cliente.save()
        return redirect('ver_cliente')
    return redirect('ver_cliente')

def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_cliente')
    return render(request, 'clientes/borrar_cliente.html', {'cliente': cliente})

# ==========================================
# VISTAS PARA PRODUCTOS
# ==========================================
def agregar_producto(request):
    if request.method == 'POST':
        try:
            Producto.objects.create(
                nombre_producto=request.POST['nombre_producto'],
                descripcion=request.POST['descripcion'],
                precio=float(request.POST['precio']),  # Cambiado a float
                stock_actual=int(request.POST['stock_actual']),
                categoria=request.POST['categoria'],
                generacion=int(request.POST['generacion']),
                es_legendario='es_legendario' in request.POST
            )
            return redirect('ver_producto')
        except Exception as e:
            mensaje_error = f"Error al crear el producto: {str(e)}"
            return render(request, 'productos/agregar_producto.html', {
                'error_message': mensaje_error,
                'form_data': request.POST
            })
    return render(request, 'productos/agregar_producto.html')

def ver_producto(request):
    productos = Producto.objects.all()
    return render(request, 'productos/ver_producto.html', {'productos': productos})

def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/actualizar_producto.html', {'producto': producto})

def realizar_actualizacion_producto(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        producto.nombre_producto = request.POST['nombre_producto']
        producto.descripcion = request.POST['descripcion']
        producto.precio = float(request.POST['precio'])  # Cambiado a float
        producto.stock_actual = int(request.POST['stock_actual'])
        producto.categoria = request.POST['categoria']
        producto.generacion = int(request.POST['generacion'])
        producto.es_legendario = 'es_legendario' in request.POST
        producto.save()
        return redirect('ver_producto')
    return redirect('ver_producto')

def borrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_producto')
    return render(request, 'productos/borrar_producto.html', {'producto': producto})

# ==========================================
# VISTAS PARA PEDIDOS
# ==========================================
def agregar_pedido(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        try:
            # Obtener cliente seleccionado
            cliente_id = request.POST['cliente']
            cliente = Cliente.objects.get(id=cliente_id)
            
            # Crear el pedido
            pedido = Pedido.objects.create(
                cliente=cliente,
                estado_pedido=request.POST['estado_pedido'],
                total_monto=float(request.POST['total_monto']),  # Cambiado a float
                metodo_pago=request.POST['metodo_pago'],
                codigo_rastreo=request.POST['codigo_rastreo'],
                fecha_entrega_estimada=request.POST['fecha_entrega_estimada'] or None,
                es_pago_verificado='es_pago_verificado' in request.POST
            )
            
            # Asignar productos al pedido (si se seleccionaron)
            producto_ids = request.POST.getlist('productos')
            if producto_ids:
                productos_seleccionados = Producto.objects.filter(id__in=producto_ids)
                for producto in productos_seleccionados:
                    # Crear detalle de producto para cada producto seleccionado
                    DetalleProducto.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=1,
                        precio_unitario=float(producto.precio),  # Cambiado a float
                        descuento_aplicado=0.00
                    )
            
            return redirect('ver_pedido')
            
        except Exception as e:
            mensaje_error = f"Error al crear el pedido: {str(e)}"
            return render(request, 'pedidos/agregar_pedido.html', {
                'error_message': mensaje_error,
                'clientes': clientes,
                'productos': productos,
                'form_data': request.POST
            })
    
    return render(request, 'pedidos/agregar_pedido.html', {
        'clientes': clientes,
        'productos': productos
    })

def ver_pedido(request):
    pedidos = Pedido.objects.all().select_related('cliente')
    return render(request, 'pedidos/ver_pedido.html', {'pedidos': pedidos})

def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    clientes = Cliente.objects.all()
    
    return render(request, 'pedidos/actualizar_pedido.html', {
        'pedido': pedido,
        'clientes': clientes
    })

def realizar_actualizacion_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        cliente = Cliente.objects.get(id=request.POST['cliente'])
        
        pedido.cliente = cliente
        pedido.estado_pedido = request.POST['estado_pedido']
        pedido.total_monto = float(request.POST['total_monto'])  # Cambiado a float
        pedido.metodo_pago = request.POST['metodo_pago']
        pedido.codigo_rastreo = request.POST['codigo_rastreo']
        pedido.fecha_entrega_estimada = request.POST['fecha_entrega_estimada'] or None
        pedido.es_pago_verificado = 'es_pago_verificado' in request.POST
        pedido.save()
        
        return redirect('ver_pedido')
    return redirect('ver_pedido')

def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('ver_pedido')
    return render(request, 'pedidos/borrar_pedido.html', {'pedido': pedido})

# ==========================================
# VISTAS PARA SET EXPANSION
# ==========================================
def agregar_set(request):
    if request.method == 'POST':
        try:
            SetExpansion.objects.create(
                nombre_set=request.POST['nombre_set'],
                abreviatura=request.POST['abreviatura'],
                fecha_lanzamiento=request.POST['fecha_lanzamiento'],
                num_cartas_total=int(request.POST['num_cartas_total']),
                es_reciente='es_reciente' in request.POST,
                simbolo_set=request.POST['simbolo_set'],
                idioma=request.POST['idioma']
            )
            return redirect('ver_set')
        except Exception as e:
            mensaje_error = f"Error al crear el set: {str(e)}"
            return render(request, 'sets/agregar_set.html', {
                'error_message': mensaje_error,
                'form_data': request.POST
            })
    return render(request, 'sets/agregar_set.html')

def ver_set(request):
    sets = SetExpansion.objects.all()
    return render(request, 'sets/ver_set.html', {'sets': sets})

def actualizar_set(request, set_id):
    set_expansion = get_object_or_404(SetExpansion, id=set_id)
    return render(request, 'sets/actualizar_set.html', {'set_expansion': set_expansion})

def realizar_actualizacion_set(request, set_id):
    if request.method == 'POST':
        set_expansion = get_object_or_404(SetExpansion, id=set_id)
        set_expansion.nombre_set = request.POST['nombre_set']
        set_expansion.abreviatura = request.POST['abreviatura']
        set_expansion.fecha_lanzamiento = request.POST['fecha_lanzamiento']
        set_expansion.num_cartas_total = int(request.POST['num_cartas_total'])
        set_expansion.es_reciente = 'es_reciente' in request.POST
        set_expansion.simbolo_set = request.POST['simbolo_set']
        set_expansion.idioma = request.POST['idioma']
        set_expansion.save()
        return redirect('ver_set')
    return redirect('ver_set')

def borrar_set(request, set_id):
    set_expansion = get_object_or_404(SetExpansion, id=set_id)
    if request.method == 'POST':
        set_expansion.delete()
        return redirect('ver_set')
    return render(request, 'sets/borrar_set.html', {'set_expansion': set_expansion})

# ==========================================
# VISTAS PARA CARTAS
# ==========================================
def agregar_carta(request):
    sets = SetExpansion.objects.all()
    if request.method == 'POST':
        try:
            set_expansion = SetExpansion.objects.get(id=request.POST['set_expansion'])
            Carta.objects.create(
                set_expansion=set_expansion,
                nombre_carta=request.POST['nombre_carta'],
                num_carta_en_set=request.POST['num_carta_en_set'],
                tipo_pokemon=request.POST['tipo_pokemon'],
                rareza=request.POST['rareza'],
                es_holo='es_holo' in request.POST,
                condicion_carta=request.POST['condicion_carta'],
                valor_mercado_usd=float(request.POST['valor_mercado_usd'])  # Cambiado a float
            )
            return redirect('ver_carta')
        except Exception as e:
            mensaje_error = f"Error al crear la carta: {str(e)}"
            return render(request, 'cartas/agregar_carta.html', {
                'error_message': mensaje_error,
                'sets': sets,
                'form_data': request.POST
            })
    return render(request, 'cartas/agregar_carta.html', {'sets': sets})

def ver_carta(request):
    cartas = Carta.objects.all().select_related('set_expansion')
    return render(request, 'cartas/ver_carta.html', {'cartas': cartas})

def actualizar_carta(request, carta_id):
    carta = get_object_or_404(Carta, id=carta_id)
    sets = SetExpansion.objects.all()
    return render(request, 'cartas/actualizar_carta.html', {
        'carta': carta,
        'sets': sets
    })

def realizar_actualizacion_carta(request, carta_id):
    if request.method == 'POST':
        carta = get_object_or_404(Carta, id=carta_id)
        set_expansion = SetExpansion.objects.get(id=request.POST['set_expansion'])
        carta.set_expansion = set_expansion
        carta.nombre_carta = request.POST['nombre_carta']
        carta.num_carta_en_set = request.POST['num_carta_en_set']
        carta.tipo_pokemon = request.POST['tipo_pokemon']
        carta.rareza = request.POST['rareza']
        carta.es_holo = 'es_holo' in request.POST
        carta.condicion_carta = request.POST['condicion_carta']
        carta.valor_mercado_usd = float(request.POST['valor_mercado_usd'])  # Cambiado a float
        carta.save()
        return redirect('ver_carta')
    return redirect('ver_carta')

def borrar_carta(request, carta_id):
    carta = get_object_or_404(Carta, id=carta_id)
    if request.method == 'POST':
        carta.delete()
        return redirect('ver_carta')
    return render(request, 'cartas/borrar_carta.html', {'carta': carta})

# ==========================================
# VISTAS PARA DETALLE PRODUCTO
# ==========================================
def agregar_detalle(request):
    pedidos = Pedido.objects.all()
    productos = Producto.objects.all()
    if request.method == 'POST':
        try:
            pedido = Pedido.objects.get(id=request.POST['pedido'])
            producto = Producto.objects.get(id=request.POST['producto'])
            DetalleProducto.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=int(request.POST['cantidad']),
                precio_unitario=float(request.POST['precio_unitario']),  # Cambiado a float
                descuento_aplicado=float(request.POST['descuento_aplicado']),  # Cambiado a float
                es_item_digital='es_item_digital' in request.POST,
                observacion_item=request.POST['observacion_item']
            )
            return redirect('ver_detalle')
        except Exception as e:
            mensaje_error = f"Error al crear el detalle: {str(e)}"
            return render(request, 'detalles/agregar_detalle.html', {
                'error_message': mensaje_error,
                'pedidos': pedidos,
                'productos': productos,
                'form_data': request.POST
            })
    return render(request, 'detalles/agregar_detalle.html', {
        'pedidos': pedidos,
        'productos': productos
    })

def ver_detalle(request):
    detalles = DetalleProducto.objects.all().select_related('pedido', 'producto')
    return render(request, 'detalles/ver_detalle.html', {'detalles': detalles})

def actualizar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetalleProducto, id=detalle_id)
    pedidos = Pedido.objects.all()
    productos = Producto.objects.all()
    return render(request, 'detalles/actualizar_detalle.html', {
        'detalle': detalle,
        'pedidos': pedidos,
        'productos': productos
    })

def realizar_actualizacion_detalle(request, detalle_id):
    if request.method == 'POST':
        detalle = get_object_or_404(DetalleProducto, id=detalle_id)
        pedido = Pedido.objects.get(id=request.POST['pedido'])
        producto = Producto.objects.get(id=request.POST['producto'])
        detalle.pedido = pedido
        detalle.producto = producto
        detalle.cantidad = int(request.POST['cantidad'])
        detalle.precio_unitario = float(request.POST['precio_unitario'])  # Cambiado a float
        detalle.descuento_aplicado = float(request.POST['descuento_aplicado'])  # Cambiado a float
        detalle.es_item_digital = 'es_item_digital' in request.POST
        detalle.observacion_item = request.POST['observacion_item']
        detalle.save()
        return redirect('ver_detalle')
    return redirect('ver_detalle')

def borrar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetalleProducto, id=detalle_id)
    if request.method == 'POST':
        detalle.delete()
        return redirect('ver_detalle')
    return render(request, 'detalles/borrar_detalle.html', {'detalle': detalle})