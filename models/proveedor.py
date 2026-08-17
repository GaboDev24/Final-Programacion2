class Proveedor:
    def __init__(self, id=None, cuit="", razon_social="", contacto="", telefono="", email="", direccion="", fecha_creacion=None):
        self.id = id
        self.cuit = cuit
        self.razon_social = razon_social
        self.contacto = contacto
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_creacion = fecha_creacion

    @property
    def company_name(self):
        return self.razon_social

    @property
    def contact_name(self):
        return self.contacto

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
            cuit=fila["cuit"],
            razon_social=fila["razon_social"],
            contacto=fila["contacto"],
            telefono=fila["telefono"],
            email=fila["email"],
            direccion=fila["direccion"],
            fecha_creacion=fila["fecha_creacion"]
        )
