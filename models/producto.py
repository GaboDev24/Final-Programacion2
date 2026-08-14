class Producto:
    def __init__(self, id=None, codigo="", nombre="", categoria="", precio_costo=0.0, precio_venta=0.0, stock=0, stock_minimo=5, proveedor_id=None, activo=1, nombre_proveedor=""):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio_costo = float(precio_costo)
        self.precio_venta = float(precio_venta)
        self.stock = int(stock)
        self.stock_minimo = int(stock_minimo)
        self.proveedor_id = proveedor_id
        self.activo = activo
        self.nombre_proveedor = nombre_proveedor

    @property
    def margen_ganancia(self):
        if self.precio_costo > 0:
            return round(((self.precio_venta - self.precio_costo) / self.precio_costo) * 100, 2)
        return 0.0

    @property
    def tiene_stock_bajo(self):
        return self.stock <= self.stock_minimo

    @classmethod
    def desde_fila(cls, fila):
        if not fila:
            return None
        nombre_proveedor = fila["nombre_proveedor"] if "nombre_proveedor" in fila.keys() else ""
        return cls(
            id=fila["id"],
            codigo=fila["codigo"],
            nombre=fila["nombre"],
            categoria=fila["categoria"],
            precio_costo=fila["precio_costo"],
            precio_venta=fila["precio_venta"],
            stock=fila["stock"],
            stock_minimo=fila["stock_minimo"],
            proveedor_id=fila["proveedor_id"],
            activo=fila["activo"],
            nombre_proveedor=nombre_proveedor
        )
