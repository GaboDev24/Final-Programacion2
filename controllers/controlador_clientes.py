from models.cliente import Cliente
from utils.validadores import Validador

class ControladorClientes:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd

    def obtener_clientes(self, busqueda=None):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        sql = "SELECT * FROM clientes"
        parametros = []
        if busqueda:
            sql += " WHERE dni_cuit LIKE ? OR nombre LIKE ? OR telefono LIKE ?"
            termino = f"%{busqueda.strip()}%"
            parametros.extend([termino, termino, termino])
        sql += " ORDER BY nombre ASC"
        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        conexion.close()
        return [Cliente.desde_fila(f) for f in filas]

    def obtener_cliente_por_id(self, cliente_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        fila = cursor.fetchone()
        conexion.close()
        return Cliente.desde_fila(fila)

    def crear_cliente(self, dni_cuit, nombre, telefono, email, direccion):
        dni = Validador.dni_cuit_valido(dni_cuit, "DNI/CUIT")
        nom = Validador.no_vacio(nombre, "Nombre o Razón Social")
        correo = Validador.email_valido(email, obligatorio=False)

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM clientes WHERE dni_cuit = ?", (dni,))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"Ya existe un cliente con DNI/CUIT '{dni}'.")

        cursor.execute("""
            INSERT INTO clientes (dni_cuit, nombre, telefono, email, direccion)
            VALUES (?, ?, ?, ?, ?)
        """, (dni, nom, telefono.strip() if telefono else "", correo, direccion.strip() if direccion else ""))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def actualizar_cliente(self, cliente_id, dni_cuit, nombre, telefono, email, direccion):
        dni = Validador.dni_cuit_valido(dni_cuit, "DNI/CUIT")
        nom = Validador.no_vacio(nombre, "Nombre o Razón Social")
        correo = Validador.email_valido(email, obligatorio=False)

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM clientes WHERE dni_cuit = ? AND id != ?", (dni, cliente_id))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"Ya existe otro cliente con DNI/CUIT '{dni}'.")

        cursor.execute("""
            UPDATE clientes
            SET dni_cuit = ?, nombre = ?, telefono = ?, email = ?, direccion = ?
            WHERE id = ?
        """, (dni, nom, telefono.strip() if telefono else "", correo, direccion.strip() if direccion else "", cliente_id))
        conexion.commit()
        conexion.close()

    def eliminar_cliente(self, cliente_id):
        if cliente_id == 1:
            raise ValueError("No se puede eliminar el cliente 'Consumidor Final'.")
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conexion.commit()
        conexion.close()

    def obtener_historial_compras_cliente(self, cliente_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT v.*, u.nombre_completo as nombre_usuario
            FROM ventas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.cliente_id = ?
            ORDER BY v.fecha DESC
        """, (cliente_id,))
        filas = cursor.fetchall()
        conexion.close()
        return filas
