from datetime import datetime
from models.compra import Compra, DetalleCompra
from utils.validadores import Validador

class ControladorCompras:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd

    def generar_numero_comprobante(self):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM compras ORDER BY id DESC LIMIT 1")
        fila = cursor.fetchone()
        conexion.close()
        siguiente_id = (fila["id"] + 1) if fila else 1
        anio = datetime.now().year
        return f"CMP-{anio}-{siguiente_id:05d}"

    def registrar_compra(self, proveedor_id, usuario_id, items_compra):
        if not items_compra:
            raise ValueError("No se han agregado productos al ingreso de mercadería.")
        if not proveedor_id:
            raise ValueError("Debe seleccionar un proveedor.")

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()

        try:
            conexion.execute("BEGIN TRANSACTION")

            total_compra = 0.0
            items_procesados = []

            for item in items_compra:
                prod_id = item["producto_id"]
                cant = Validador.entero_positivo(item["cantidad"], "Cantidad a ingresar")
                costo = Validador.flotante_positivo(item["costo_unitario"], "Costo unitario")

                if cant <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0.")

                cursor.execute("SELECT id, codigo, nombre, stock FROM productos WHERE id = ? AND activo = 1", (prod_id,))
                prod = cursor.fetchone()
                if not prod:
                    raise ValueError(f"El producto con ID {prod_id} no existe.")

                subtot = round(costo * cant, 2)
                total_compra += subtot

                items_procesados.append({
                    "producto_id": prod["id"],
                    "codigo_producto": prod["codigo"],
                    "nombre_producto": prod["nombre"],
                    "costo_unitario": costo,
                    "cantidad": cant,
                    "subtotal": subtot,
                    "nuevo_stock": prod["stock"] + cant
                })

            total_compra = round(total_compra, 2)
            num_comp = self.generar_numero_comprobante()

            cursor.execute("""
                INSERT INTO compras (numero_comprobante, proveedor_id, usuario_id, total)
                VALUES (?, ?, ?, ?)
            """, (num_comp, proveedor_id, usuario_id, total_compra))
            compra_id = cursor.lastrowid

            for it in items_procesados:
                cursor.execute("""
                    INSERT INTO detalle_compras (compra_id, producto_id, costo_unitario, cantidad, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (compra_id, it["producto_id"], it["costo_unitario"], it["cantidad"], it["subtotal"]))

                cursor.execute("""
                    UPDATE productos 
                    SET stock = ?, precio_costo = ?
                    WHERE id = ?
                """, (it["nuevo_stock"], it["costo_unitario"], it["producto_id"]))

            conexion.commit()
            conexion.close()
            return compra_id

        except Exception as e:
            conexion.rollback()
            conexion.close()
            raise e

    def obtener_compras(self, busqueda=None):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            SELECT c.*, p.razon_social as razon_social_proveedor, u.nombre_completo as nombre_usuario
            FROM compras c
            LEFT JOIN proveedores p ON c.proveedor_id = p.id
            LEFT JOIN usuarios u ON c.usuario_id = u.id
        """
        parametros = []
        if busqueda:
            sql += " WHERE c.numero_comprobante LIKE ? OR p.razon_social LIKE ?"
            term = f"%{busqueda.strip()}%"
            parametros.extend([term, term])
        sql += " ORDER BY c.fecha DESC"

        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        conexion.close()
        return [Compra.desde_fila(f) for f in filas]

    def obtener_compra_por_id(self, compra_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT c.*, p.razon_social as razon_social_proveedor, u.nombre_completo as nombre_usuario
            FROM compras c
            LEFT JOIN proveedores p ON c.proveedor_id = p.id
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.id = ?
        """, (compra_id,))
        fila = cursor.fetchone()
        if not fila:
            conexion.close()
            return None

        cursor.execute("""
            SELECT dc.*, pr.nombre as nombre_producto, pr.codigo as codigo_producto
            FROM detalle_compras dc
            LEFT JOIN productos pr ON dc.producto_id = pr.id
            WHERE dc.compra_id = ?
        """, (compra_id,))
        filas_items = cursor.fetchall()
        conexion.close()

        compra = Compra.desde_fila(fila)
        compra.items = [DetalleCompra.desde_fila(f) for f in filas_items]
        return compra
