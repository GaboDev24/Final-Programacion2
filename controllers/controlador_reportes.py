from models.venta import Venta, DetalleVenta

class ControladorReportes:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd

    def obtener_resumen_dashboard(self):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas")
        total_ventas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ventas")
        cantidad_ventas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 1")
        total_productos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM productos WHERE stock <= stock_minimo AND activo = 1")
        productos_stock_bajo = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(dv.cantidad * (dv.precio_unitario - p.precio_costo)), 0)
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
        """)
        ganancia_estimada = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM compras")
        total_compras = cursor.fetchone()[0]

        conexion.close()

        return {
            "total_ventas": round(total_ventas, 2),
            "cantidad_ventas": cantidad_ventas,
            "total_productos": total_productos,
            "productos_stock_bajo": productos_stock_bajo,
            "total_clientes": total_clientes,
            "ganancia_estimada": round(ganancia_estimada, 2),
            "total_compras": round(total_compras, 2)
        }

    def obtener_historial_ventas(self, busqueda=None, metodo_pago=None, fecha_inicio=None, fecha_fin=None):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
            SELECT v.*, c.nombre as nombre_cliente, u.nombre_completo as nombre_usuario
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE 1=1
        """
        parametros = []

        if busqueda:
            sql += " AND (v.numero_factura LIKE ? OR c.nombre LIKE ? OR u.nombre_completo LIKE ?)"
            term = f"%{busqueda.strip()}%"
            parametros.extend([term, term, term])

        if metodo_pago and metodo_pago != "Todos":
            sql += " AND v.metodo_pago = ?"
            parametros.append(metodo_pago)

        if fecha_inicio:
            sql += " AND date(v.fecha) >= date(?)"
            parametros.append(fecha_inicio)

        if fecha_fin:
            sql += " AND date(v.fecha) <= date(?)"
            parametros.append(fecha_fin)

        sql += " ORDER BY v.fecha DESC"

        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        conexion.close()
        return [Venta.desde_fila(f) for f in filas]

    def obtener_productos_mas_vendidos(self, limite=5):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.nombre, p.categoria, SUM(dv.cantidad) as total_unidades, SUM(dv.subtotal) as total_recaudado
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            GROUP BY p.id
            ORDER BY total_unidades DESC
            LIMIT ?
        """, (limite,))
        filas = cursor.fetchall()
        conexion.close()
        return filas
