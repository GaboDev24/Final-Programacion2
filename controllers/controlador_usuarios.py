import hashlib
from models.usuario import Usuario
from utils.validadores import Validador

class ControladorUsuarios:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd

    def obtener_usuarios(self, busqueda=None):
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        sql = "SELECT * FROM usuarios WHERE activo = 1"
        parametros = []
        if busqueda:
            sql += " AND (nombre_usuario LIKE ? OR nombre_completo LIKE ?)"
            term = f"%{busqueda.strip()}%"
            parametros.extend([term, term])
        sql += " ORDER BY nombre_usuario ASC"
        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        conexion.close()
        return [Usuario.desde_fila(f) for f in filas]

    def crear_usuario(self, nombre_usuario, clave, nombre_completo, rol):
        usr = Validador.no_vacio(nombre_usuario, "Nombre de usuario")
        pwd = Validador.no_vacio(clave, "Contraseña")
        nombre = Validador.no_vacio(nombre_completo, "Nombre completo")

        if rol not in ["Administrador", "Vendedor"]:
            rol = "Vendedor"

        clave_hash = hashlib.sha256(pwd.encode()).hexdigest()

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = ?", (usr,))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"El nombre de usuario '{usr}' ya está registrado.")

        cursor.execute("""
            INSERT INTO usuarios (nombre_usuario, clave_hash, nombre_completo, rol)
            VALUES (?, ?, ?, ?)
        """, (usr, clave_hash, nombre, rol))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def actualizar_usuario(self, usuario_id, nombre_usuario, nueva_clave, nombre_completo, rol):
        usr = Validador.no_vacio(nombre_usuario, "Nombre de usuario")
        nombre = Validador.no_vacio(nombre_completo, "Nombre completo")

        if rol not in ["Administrador", "Vendedor"]:
            rol = "Vendedor"

        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = ? AND id != ?", (usr, usuario_id))
        if cursor.fetchone():
            conexion.close()
            raise ValueError(f"El nombre de usuario '{usr}' ya está en uso.")

        if nueva_clave and nueva_clave.strip():
            clave_hash = hashlib.sha256(nueva_clave.strip().encode()).hexdigest()
            cursor.execute("""
                UPDATE usuarios
                SET nombre_usuario = ?, clave_hash = ?, nombre_completo = ?, rol = ?
                WHERE id = ?
            """, (usr, clave_hash, nombre, rol, usuario_id))
        else:
            cursor.execute("""
                UPDATE usuarios
                SET nombre_usuario = ?, nombre_completo = ?, rol = ?
                WHERE id = ?
            """, (usr, nombre, rol, usuario_id))

        conexion.commit()
        conexion.close()

    def desactivar_usuario(self, usuario_id):
        if usuario_id == 1:
            raise ValueError("No se puede desactivar el usuario administrador principal.")
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (usuario_id,))
        conexion.commit()
        conexion.close()
