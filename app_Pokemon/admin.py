from django.contrib import admin
from .models import Cliente, Pedido, Producto, SetExpansion, Carta, DetalleProducto

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_cliente', 'email', 'telefono', 'puntos_lealtad', 'tipo_entrenador']
    search_fields = ['nombre_cliente', 'email']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_pedido', 'estado_pedido', 'total_monto', 'es_pago_verificado']
    list_filter = ['estado_pedido', 'fecha_pedido', 'es_pago_verificado']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'precio', 'stock_actual', 'categoria', 'generacion', 'es_legendario']
    list_filter = ['categoria', 'generacion', 'es_legendario']

# 👇 NUEVOS MODELOS REGISTRADOS
@admin.register(SetExpansion)
class SetExpansionAdmin(admin.ModelAdmin):
    list_display = ['nombre_set', 'abreviatura', 'fecha_lanzamiento', 'num_cartas_total', 'es_reciente', 'idioma']
    list_filter = ['es_reciente', 'idioma', 'fecha_lanzamiento']

@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ['nombre_carta', 'set_expansion', 'num_carta_en_set', 'tipo_pokemon', 'rareza', 'valor_mercado_usd']
    list_filter = ['tipo_pokemon', 'rareza', 'es_holo', 'condicion_carta']
    search_fields = ['nombre_carta', 'set_expansion__nombre_set']

@admin.register(DetalleProducto)
class DetalleProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'producto', 'cantidad', 'precio_unitario', 'es_item_digital']
    list_filter = ['es_item_digital', 'fecha_agregado']