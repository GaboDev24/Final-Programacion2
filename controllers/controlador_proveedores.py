from models.proveedor import Proveedor
from utils.validadores import Validador

class ControladorProveedores:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd

    def obtener_proveedores(self, busqueda=None):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        sql = "SELECT * FROM proveedores"
        parametros = []
        if busqueda:
            sql += " WHERE cuit LIKE ? OR razon_social LIKE ? OR contacto LIKE ?"
            termino = f"%{busqueda.strip()}%"
            parametros.extend([termino, termino, termino])
        sql += " ORDER BY razon_social ASC"
        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        conexion.close()
        return [Proveedor.desde_fila(f) for f in filas]

    def obtener_proveedor_por_id(self, proveedor_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE id = ?", (proveedor_id,))
        fila = cursor.fetchone()
        conexion.close()
        return Proveedor.desde_fila(fila)

    def crear_proveedor(self, cuit, razon_social, contacto, telefono, email, direccion):
        cuit_val = Validador.dni_cuit_valido(cuit, "CUIT")
        razon = Validador.no_vacio(razon_social, "Razón Social")
        correo = Validador.email_valido(email, obligatorio=False)

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM proveedores WHERE cuit = ?", (cuit_val,))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"Ya existe un proveedor con CUIT '{cuit_val}'.")

        cursor.execute("""
            INSERT INTO proveedores (cuit, razon_social, contacto, telefono, email, direccion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cuit_val, razon, contacto.strip() if contacto else "", telefono.strip() if telefono else "", correo, direccion.strip() if direccion else ""))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def actualizar_proveedor(self, proveedor_id, cuit, razon_social, contacto, telefono, email, direccion):
        cuit_val = Validador.dni_cuit_valido(cuit, "CUIT")
        razon = Validador.no_vacio(razon_social, "Razón Social")
        correo = Validador.email_valido(email, obligatorio=False)

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM proveedores WHERE cuit = ? AND id != ?", (cuit_val, proveedor_id))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"Ya existe otro proveedor con CUIT '{cuit_val}'.")

        cursor.execute("""
            UPDATE proveedores
            SET cuit = ?, razon_social = ?, contacto = ?, telefono = ?, email = ?, direccion = ?
            WHERE id = ?
        """, (cuit_val, razon, contacto.strip() if contacto else "", telefono.strip() if telefono else "", correo, direccion.strip() if direccion else "", proveedor_id))
        conexion.commit()
        conexion.close()

    def eliminar_proveedor(self, proveedor_id):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM proveedores WHERE id = ?", (proveedor_id,))
        conexion.commit()
        conexion.close()
