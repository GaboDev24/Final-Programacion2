class DetalleCompra:
    def __init__(self, id=None, compra_id=None, producto_id=None, costo_unitario=0.0, cantidad=1, subtotal=0.0, nombre_producto="", codigo_producto=""):
        self.id = id
        self.compra_id = compra_id
        self.producto_id = producto_id
        self.costo_unitario = float(costo_unitario)
        self.cantidad = int(cantidad)
        self.subtotal = float(subtotal) if subtotal else round(self.costo_unitario * self.cantidad, 2)
        self.nombre_producto = nombre_producto
        self.codigo_producto = codigo_producto

    @property
    def product_id(self):
        return self.producto_id

    @property
    def unit_cost(self):
        return self.costo_unitario

    @property
    def quantity(self):
        return self.cantidad

    @property
    def product_name(self):
        return self.nombre_producto

    @property
    def product_code(self):
        return self.codigo_producto

    @classmethod
    def desde_fila(cls, fila):
        if not fila:
            return None
        nombre_producto = fila["nombre_producto"] if "nombre_producto" in fila.keys() else ""
        codigo_producto = fila["codigo_producto"] if "codigo_producto" in fila.keys() else ""
        return cls(
            id=fila["id"],
            compra_id=fila["compra_id"],
            producto_id=fila["producto_id"],
            costo_unitario=fila["costo_unitario"],
            cantidad=fila["cantidad"],
            subtotal=fila["subtotal"],
            nombre_producto=nombre_producto,
            codigo_producto=codigo_producto
        )

class Compra:
    def __init__(self, id=None, numero_comprobante="", proveedor_id=None, usuario_id=None, total=0.0, fecha=None, razon_social_proveedor="", nombre_usuario="", items=None):
        self.id = id
        self.numero_comprobante = numero_comprobante
        self.proveedor_id = proveedor_id
        self.usuario_id = usuario_id
        self.total = float(total)
        self.fecha = fecha
        self.razon_social_proveedor = razon_social_proveedor
        self.nombre_usuario = nombre_usuario
        self.items = items if items is not None else []

    @property
    def receipt_number(self):
        return self.numero_comprobante

    @property
    def supplier_id(self):
        return self.proveedor_id

    @property
    def user_id(self):
        return self.usuario_id

    @classmethod
    def desde_fila(cls, fila):
        if not fila:
            return None
        razon_social = fila["razon_social"] if "razon_social" in fila.keys() else ""
        nombre_usuario = fila["nombre_usuario"] if "nombre_usuario" in fila.keys() else ""
        return cls(
            id=fila["id"],
            numero_comprobante=fila["numero_comprobante"],
            proveedor_id=fila["proveedor_id"],
            usuario_id=fila["usuario_id"],
            total=fila["total"],
            fecha=fila["fecha"],
            razon_social_proveedor=razon_social,
            nombre_usuario=nombre_usuario
        )
