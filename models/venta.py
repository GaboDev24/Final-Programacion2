class DetalleVenta:
    def __init__(self, id=None, venta_id=None, producto_id=None, codigo_producto="", nombre_producto="", precio_unitario=0.0, cantidad=1, subtotal=0.0):
        self.id = id
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.codigo_producto = codigo_producto
        self.nombre_producto = nombre_producto
        self.precio_unitario = float(precio_unitario)
        self.cantidad = int(cantidad)
        self.subtotal = float(subtotal) if subtotal else round(self.precio_unitario * self.cantidad, 2)

    @classmethod
    def desde_fila(cls, fila):
        if not fila:
            return None
        return cls(
            id=fila["id"],
            venta_id=fila["venta_id"],
            producto_id=fila["producto_id"],
            codigo_producto=fila["codigo_producto"],
            nombre_producto=fila["nombre_producto"],
            precio_unitario=fila["precio_unitario"],
            cantidad=fila["cantidad"],
            subtotal=fila["subtotal"]
        )

class Venta:
    def __init__(self, id=None, numero_factura="", cliente_id=None, usuario_id=None, metodo_pago="Efectivo", subtotal=0.0, descuento=0.0, total=0.0, fecha=None, nombre_cliente="", nombre_usuario="", items=None):
        self.id = id
        self.numero_factura = numero_factura
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.metodo_pago = metodo_pago
        self.subtotal = float(subtotal)
        self.descuento = float(descuento)
        self.total = float(total)
        self.fecha = fecha
        self.nombre_cliente = nombre_cliente
        self.nombre_usuario = nombre_usuario
        self.items = items if items is not None else []

    @classmethod
    def desde_fila(cls, fila):
        if not fila:
            return None
        nombre_cliente = fila["nombre_cliente"] if "nombre_cliente" in fila.keys() else ""
        nombre_usuario = fila["nombre_usuario"] if "nombre_usuario" in fila.keys() else ""
        return cls(
            id=fila["id"],
            numero_factura=fila["numero_factura"],
            cliente_id=fila["cliente_id"],
            usuario_id=fila["usuario_id"],
            metodo_pago=fila["metodo_pago"],
            subtotal=fila["subtotal"],
            descuento=fila["descuento"],
            total=fila["total"],
            fecha=fila["fecha"],
            nombre_cliente=nombre_cliente,
            nombre_usuario=nombre_usuario
        )
