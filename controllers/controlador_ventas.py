from datetime import datetime
from models.venta import Venta, DetalleVenta
from models.cliente import Cliente
from models.usuario import Usuario
from utils.validadores import Validador
from utils.generador_ticket import GeneradorTicket

class ControladorVentas:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd

    def generar_numero_factura(self):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM ventas ORDER BY id DESC LIMIT 1")
        fila = cursor.fetchone()
        conexion.close()
        siguiente_id = (fila["id"] + 1) if fila else 1
        anio = datetime.now().year
        return f"VTA-{anio}-{siguiente_id:05d}"

    def procesar_venta(self, cliente_id, usuario_id, metodo_pago, items_carrito, descuento=0.0):
        if not items_carrito:
            raise ValueError("El carrito de compras está vacío.")
        if not usuario_id:
            raise ValueError("No hay un usuario autenticado para registrar la venta.")

        metodos_validos = ["Efectivo", "Tarjeta de Débito", "Tarjeta de Crédito", "Transferencia", "Cuenta Corriente"]
        if metodo_pago not in metodos_validos:
            metodo_pago = "Efectivo"

        descuento = Validador.flotante_positivo(descuento, "Descuento")

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()

        try:
            conexion.execute("BEGIN TRANSACTION")

            subtotal = 0.0
            items_validados = []

            for item in items_carrito:
                producto_id = item["producto_id"]
                cantidad = item["cantidad"]

                if cantidad <= 0:
                    raise ValueError(f"La cantidad para '{item['nombre_producto']}' debe ser mayor a 0.")

                cursor.execute("SELECT id, codigo, nombre, precio_venta, stock FROM productos WHERE id = ? AND activo = 1", (producto_id,))
                prod = cursor.fetchone()
                if not prod:
                    raise ValueError(f"El producto con ID {producto_id} no existe o fue desactivado.")

                if prod["stock"] < cantidad:
                    raise ValueError(f"Stock insuficiente para '{prod['nombre']}'. Disponible: {prod['stock']}, Solicitado: {cantidad}.")

                subtotal_item = round(prod["precio_venta"] * cantidad, 2)
                subtotal += subtotal_item

                items_validados.append({
                    "producto_id": prod["id"],
                    "codigo_producto": prod["codigo"],
                    "nombre_producto": prod["nombre"],
                    "precio_unitario": prod["precio_venta"],
                    "cantidad": cantidad,
                    "subtotal": subtotal_item,
                    "nuevo_stock": prod["stock"] - cantidad
                })

            subtotal = round(subtotal, 2)
            if descuento > subtotal:
                raise ValueError("El descuento no puede superar el subtotal de la venta.")

            total = round(subtotal - descuento, 2)
            num_factura = self.generar_numero_factura()

            cursor.execute("""
                INSERT INTO ventas (numero_factura, cliente_id, usuario_id, metodo_pago, subtotal, descuento, total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (num_factura, cliente_id if cliente_id else None, usuario_id, metodo_pago, subtotal, descuento, total))
            venta_id = cursor.lastrowid

            objetos_items = []
            for it in items_validados:
                cursor.execute("""
                    INSERT INTO detalle_ventas (venta_id, producto_id, codigo_producto, nombre_producto, precio_unitario, cantidad, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (venta_id, it["producto_id"], it["codigo_producto"], it["nombre_producto"], it["precio_unitario"], it["cantidad"], it["subtotal"]))

                cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (it["nuevo_stock"], it["producto_id"]))

                objetos_items.append(DetalleVenta(
                    venta_id=venta_id,
                    producto_id=it["producto_id"],
                    codigo_producto=it["codigo_producto"],
                    nombre_producto=it["nombre_producto"],
                    precio_unitario=it["precio_unitario"],
                    cantidad=it["cantidad"],
                    subtotal=it["subtotal"]
                ))

            conexion.commit()

            cursor.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,))
            fila_venta = cursor.fetchone()

            cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
            fila_cliente = cursor.fetchone()

            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
            fila_usuario = cursor.fetchone()

            obj_venta = Venta.desde_fila(fila_venta)
            obj_venta.items = objetos_items
            obj_cliente = Cliente.desde_fila(fila_cliente) if fila_cliente else None
            obj_usuario = Usuario.desde_fila(fila_usuario) if fila_usuario else None

            texto_ticket = GeneradorTicket.generar_texto_ticket(obj_venta, obj_cliente, obj_usuario, objetos_items)
            archivo_ticket = GeneradorTicket.guardar_ticket_archivo(texto_ticket, obj_venta.numero_factura)

            conexion.close()
            return obj_venta, texto_ticket, archivo_ticket

        except Exception as e:
            conexion.rollback()
            conexion.close()
            raise e

    def obtener_venta_por_id(self, venta_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT v.*, c.nombre as nombre_cliente, u.nombre_completo as nombre_usuario
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.id = ?
        """, (venta_id,))
        fila = cursor.fetchone()
        if not fila:
            conexion.close()
            return None

        cursor.execute("SELECT * FROM detalle_ventas WHERE venta_id = ?", (venta_id,))
        filas_items = cursor.fetchall()
        conexion.close()

        venta = Venta.desde_fila(fila)
        venta.items = [DetalleVenta.desde_fila(f) for f in filas_items]
        return venta
