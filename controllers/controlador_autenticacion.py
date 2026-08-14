import hashlib
from models.usuario import Usuario

class ControladorAutenticacion:
    def __init__(self, gestor_bd):
        self.bd = gestor_bd
        self.usuario_actual = None

    def iniciar_sesion(self, nombre_usuario, clave):
        if not nombre_usuario or not clave:
            raise ValueError("Debe ingresar el nombre de usuario y la contraseña.")
        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        conexion = self.bd.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = ? AND activo = 1", (nombre_usuario.strip(),))
        fila = cursor.fetchone()
        conexion.close()

        if not fila:
            raise ValueError("Usuario o contraseña incorrectos.")
        if fila["clave_hash"] != clave_hash:
            raise ValueError("Usuario o contraseña incorrectos.")

        self.usuario_actual = Usuario.desde_fila(fila)
        return self.usuario_actual

    def cerrar_sesion(self):
        self.usuario_actual = None

    def obtener_usuario_actual(self):
        return self.usuario_actual
