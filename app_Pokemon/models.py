from django.db import models

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, blank=True, default='')
    fecha_registro = models.DateField(auto_now_add=True)
    puntos_lealtad = models.IntegerField(default=0)
    tipo_entrenador = models.CharField(max_length=50, default='Entrenador')
    
    def __str__(self):
        return self.nombre_cliente

class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(
        max_length=50,
        choices=[('P', 'Pendiente'), ('E', 'Enviado'), ('T', 'Entregado')],
        default='P'
    )
    total_monto = models.FloatField(default=0.00)  # Cambiado a FloatField
    metodo_pago = models.CharField(max_length=50, default='Efectivo')
    codigo_rastreo = models.CharField(max_length=100, blank=True, default='')
    fecha_entrega_estimada = models.DateField(null=True, blank=True)
    es_pago_verificado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"Pedido N°{self.id} de {self.cliente.nombre_cliente}"

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100, default='Producto Pokemon')
    descripcion = models.TextField(default='Descripción del producto')
    precio = models.FloatField(default=0.00)  # Cambiado a FloatField
    stock_actual = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50, default='General')
    generacion = models.IntegerField(default=1)
    es_legendario = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre_producto

class SetExpansion(models.Model):
    nombre_set = models.CharField(max_length=150, unique=True, default='Nuevo Set')
    abreviatura = models.CharField(max_length=10, unique=True, default='SET')
    fecha_lanzamiento = models.DateField(auto_now_add=True)
    num_cartas_total = models.IntegerField(default=0)
    es_reciente = models.BooleanField(default=True)
    simbolo_set = models.CharField(max_length=10, default='★')
    idioma = models.CharField(max_length=50, default='Español')
    
    def __str__(self):
        return f"{self.nombre_set} ({self.abreviatura})"

class Carta(models.Model):
    CONDICION_CHOICES = [
        ('NM', 'Near Mint'),
        ('LP', 'Lightly Played'),
        ('MP', 'Moderately Played'),
        ('HP', 'Heavily Played')
    ]
    
    set_expansion = models.ForeignKey(
        SetExpansion,
        on_delete=models.PROTECT,
        related_name='cartas'
    )
    nombre_carta = models.CharField(max_length=150, default='Nueva Carta')
    num_carta_en_set = models.CharField(max_length=10, default='001/000')
    tipo_pokemon = models.CharField(max_length=50, default='Normal')
    rareza = models.CharField(max_length=50, default='Común')
    es_holo = models.BooleanField(default=False)
    condicion_carta = models.CharField(
        max_length=50,
        choices=CONDICION_CHOICES,
        default='NM'
    )
    valor_mercado_usd = models.FloatField(default=0.00)  # Cambiado a FloatField
    
    def __str__(self):
        return f"{self.nombre_carta} ({self.num_carta_en_set})"

class DetalleProducto(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_pedido'
    )
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.FloatField(default=0.00)  # Cambiado a FloatField
    descuento_aplicado = models.FloatField(default=0.00)  # Cambiado a FloatField
    es_item_digital = models.BooleanField(default=False)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    observacion_item = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre_producto} en Pedido {self.pedido.id}"