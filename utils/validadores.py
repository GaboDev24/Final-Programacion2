import re

class Validador:
    @staticmethod
    def no_vacio(valor, nombre_campo="Campo"):
        if not valor or str(valor).strip() == "":
            raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
        return str(valor).strip()

    @staticmethod
    def flotante_positivo(valor, nombre_campo="Monto"):
        try:
            val = float(valor)
            if val < 0:
                raise ValueError(f"El campo '{nombre_campo}' debe ser mayor o igual a 0.")
            return val
        except (ValueError, TypeError):
            raise ValueError(f"El campo '{nombre_campo}' debe ser un número decimal válido.")

    @staticmethod
    def entero_positivo(valor, nombre_campo="Cantidad"):
        try:
            val = int(valor)
            if val < 0:
                raise ValueError(f"El campo '{nombre_campo}' debe ser un entero mayor o igual a 0.")
            return val
        except (ValueError, TypeError):
            raise ValueError(f"El campo '{nombre_campo}' debe ser un número entero válido.")

    @staticmethod
    def email_valido(valor, obligatorio=False):
        if not valor and not obligatorio:
            return ""
        val = str(valor).strip()
        if not val and not obligatorio:
            return ""
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, val):
            raise ValueError("El correo electrónico no tiene un formato válido.")
        return val

    @staticmethod
    def dni_cuit_valido(valor, nombre_campo="DNI/CUIT"):
        val = str(valor).strip()
        if not val:
            raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
        limpio = val.replace("-", "").replace(".", "").replace(" ", "")
        if not limpio.isalnum() and not limpio.isdigit():
            raise ValueError(f"El campo '{nombre_campo}' contiene caracteres no válidos.")
        return val
