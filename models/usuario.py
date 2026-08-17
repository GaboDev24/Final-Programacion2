class Usuario:
    def __init__(self, id=None, nombre_usuario="", clave_hash="", nombre_completo="", rol="Vendedor", activo=1, fecha_creacion=None):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.clave_hash = clave_hash
        self.nombre_completo = nombre_completo
        self.rol = rol
        self.activo = activo
        self.fecha_creacion = fecha_creacion

    @property
    def username(self):
        return self.nombre_usuario

    @property
    def full_name(self):
        return self.nombre_completo

    @property
    def is_active(self):
        return self.activo

    @property
    def created_at(self):
        return self.fecha_creacion

    @classmethod
    def desde_fila(cls, fila):
        if not fila:
            return None
        return cls(
            id=fila["id"],
            nombre_usuario=fila["nombre_usuario"],
            clave_hash=fila["clave_hash"],
            nombre_completo=fila["nombre_completo"],
            rol=fila["rol"],
            activo=fila["activo"],
            fecha_creacion=fila["fecha_creacion"]
        )

    def es_admin(self):
        return self.rol == "Administrador"

    def is_admin(self):
        return self.rol == "Administrador"
