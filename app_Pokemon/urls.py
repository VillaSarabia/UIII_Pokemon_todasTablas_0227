from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_Pokemon, name='inicio_Pokemon'),
    
    # URLs para Clientes
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('ver-cliente/', views.ver_cliente, name='ver_cliente'),
    path('actualizar-cliente/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('realizar-actualizacion-cliente/<int:cliente_id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('borrar-cliente/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
    
    # URLs para Productos
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('ver-producto/', views.ver_producto, name='ver_producto'),
    path('actualizar-producto/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('realizar-actualizacion-producto/<int:producto_id>/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
    path('borrar-producto/<int:producto_id>/', views.borrar_producto, name='borrar_producto'),
    
    # URLs para Pedidos
    path('agregar-pedido/', views.agregar_pedido, name='agregar_pedido'),
    path('ver-pedido/', views.ver_pedido, name='ver_pedido'),
    path('actualizar-pedido/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('realizar-actualizacion-pedido/<int:pedido_id>/', views.realizar_actualizacion_pedido, name='realizar_actualizacion_pedido'),
    path('borrar-pedido/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),
    
    # URLs para Set Expansion
    path('agregar-set/', views.agregar_set, name='agregar_set'),
    path('ver-set/', views.ver_set, name='ver_set'),
    path('actualizar-set/<int:set_id>/', views.actualizar_set, name='actualizar_set'),
    path('realizar-actualizacion-set/<int:set_id>/', views.realizar_actualizacion_set, name='realizar_actualizacion_set'),
    path('borrar-set/<int:set_id>/', views.borrar_set, name='borrar_set'),
    
    # URLs para Cartas
    path('agregar-carta/', views.agregar_carta, name='agregar_carta'),
    path('ver-carta/', views.ver_carta, name='ver_carta'),
    path('actualizar-carta/<int:carta_id>/', views.actualizar_carta, name='actualizar_carta'),
    path('realizar-actualizacion-carta/<int:carta_id>/', views.realizar_actualizacion_carta, name='realizar_actualizacion_carta'),
    path('borrar-carta/<int:carta_id>/', views.borrar_carta, name='borrar_carta'),
    
    # URLs para Detalle Producto
    path('agregar-detalle/', views.agregar_detalle, name='agregar_detalle'),
    path('ver-detalle/', views.ver_detalle, name='ver_detalle'),
    path('actualizar-detalle/<int:detalle_id>/', views.actualizar_detalle, name='actualizar_detalle'),
    path('realizar-actualizacion-detalle/<int:detalle_id>/', views.realizar_actualizacion_detalle, name='realizar_actualizacion_detalle'),
    path('borrar-detalle/<int:detalle_id>/', views.borrar_detalle, name='borrar_detalle'),
]