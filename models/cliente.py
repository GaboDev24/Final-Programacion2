class Cliente:
    def __init__(self, id=None, dni_cuit="", nombre="", telefono="", email="", direccion="", fecha_creacion=None):
        self.id = id
        self.dni_cuit = dni_cuit
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_creacion = fecha_creacion

    @property
    def name(self):
        return self.nombre

    @property
    def phone(self):
        return self.telefono

    @property
    def address(self):
        return self.direccion

    @classmethod
    def desde_fila(cls, fila):
        if not fila:
            return None
        return cls(
            id=fila["id"],
            dni_cuit=fila["dni_cuit"],
            nombre=fila["nombre"],
            telefono=fila["telefono"],
            email=fila["email"],
            direccion=fila["direccion"],
            fecha_creacion=fila["fecha_creacion"]
        )
