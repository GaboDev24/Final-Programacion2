from models.producto import Producto
from utils.validadores import Validador

class ControladorInventario:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd

    def obtener_productos(self, busqueda=None, categoria=None, solo_stock_bajo=False):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            SELECT p.*, s.razon_social as nombre_proveedor 
            FROM productos p
            LEFT JOIN proveedores s ON p.proveedor_id = s.id
            WHERE p.activo = 1
        """
        parametros = []
        if busqueda:
            sql += " AND (p.codigo LIKE ? OR p.nombre LIKE ?)"
            termino = f"%{busqueda.strip()}%"
            parametros.extend([termino, termino])
        if categoria and categoria != "Todas":
            sql += " AND p.categoria = ?"
            parametros.append(categoria)
        if solo_stock_bajo:
            sql += " AND p.stock <= p.stock_minimo"
        sql += " ORDER BY p.nombre ASC"

        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        conexion.close()
        return [Producto.desde_fila(f) for f in filas]

    def obtener_producto_por_id(self, producto_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.*, s.razon_social as nombre_proveedor 
            FROM productos p
            LEFT JOIN proveedores s ON p.proveedor_id = s.id
            WHERE p.id = ? AND p.activo = 1
        """, (producto_id,))
        fila = cursor.fetchone()
        conexion.close()
        return Producto.desde_fila(fila)

    def obtener_producto_por_codigo(self, codigo):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.*, s.razon_social as nombre_proveedor 
            FROM productos p
            LEFT JOIN proveedores s ON p.proveedor_id = s.id
            WHERE p.codigo = ? AND p.activo = 1
        """, (codigo.strip(),))
        fila = cursor.fetchone()
        conexion.close()
        return Producto.desde_fila(fila)

    def crear_producto(self, codigo, nombre, categoria, precio_costo, precio_venta, stock, stock_minimo, proveedor_id):
        codigo = Validador.no_vacio(codigo, "Código")
        nombre = Validador.no_vacio(nombre, "Nombre")
        categoria = Validador.no_vacio(categoria, "Categoría")
        costo = Validador.flotante_positivo(precio_costo, "Precio de costo")
        venta = Validador.flotante_positivo(precio_venta, "Precio de venta")
        stk = Validador.entero_positivo(stock, "Stock actual")
        min_stk = Validador.entero_positivo(stock_minimo, "Stock mínimo")

        if venta < costo:
            raise ValueError("El precio de venta no puede ser inferior al precio de costo.")

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM productos WHERE codigo = ? AND activo = 1", (codigo,))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"Ya existe un producto con el código '{codigo}'.")

        cursor.execute("""
            INSERT INTO productos (codigo, nombre, categoria, precio_costo, precio_venta, stock, stock_minimo, proveedor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, nombre, categoria, costo, venta, stk, min_stk, proveedor_id if proveedor_id else None))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def actualizar_producto(self, producto_id, codigo, nombre, categoria, precio_costo, precio_venta, stock, stock_minimo, proveedor_id):
        codigo = Validador.no_vacio(codigo, "Código")
        nombre = Validador.no_vacio(nombre, "Nombre")
        categoria = Validador.no_vacio(categoria, "Categoría")
        costo = Validador.flotante_positivo(precio_costo, "Precio de costo")
        venta = Validador.flotante_positivo(precio_venta, "Precio de venta")
        stk = Validador.entero_positivo(stock, "Stock actual")
        min_stk = Validador.entero_positivo(stock_minimo, "Stock mínimo")

        if venta < costo:
            raise ValueError("El precio de venta no puede ser inferior al precio de costo.")

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM productos WHERE codigo = ? AND id != ? AND activo = 1", (codigo, producto_id))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"Ya existe otro producto con el código '{codigo}'.")

        cursor.execute("""
            UPDATE productos
            SET codigo = ?, nombre = ?, categoria = ?, precio_costo = ?, precio_venta = ?, stock = ?, stock_minimo = ?, proveedor_id = ?
            WHERE id = ?
        """, (codigo, nombre, categoria, costo, venta, stk, min_stk, proveedor_id if proveedor_id else None, producto_id))
        conexion.commit()
        conexion.close()

    def eliminar_producto(self, producto_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET activo = 0 WHERE id = ?", (producto_id,))
        conexion.commit()
        conexion.close()

    def obtener_categorias(self):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM categorias ORDER BY nombre ASC")
        filas = cursor.fetchall()
        conexion.close()
        return [f["nombre"] for f in filas]

    def agregar_categoria(self, nombre):
        nombre_cat = Validador.no_vacio(nombre, "Nombre de categoría")
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre_cat,))
            conexion.commit()
        except Exception:
            conexion.close()
            raise ValueError(f"La categoría '{nombre_cat}' ya existe.")
        conexion.close()
