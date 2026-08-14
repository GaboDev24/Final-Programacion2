import os
from datetime import datetime

class GeneradorTicket:
    @staticmethod
    def generar_texto_ticket(venta, cliente, usuario, items):
        fecha_str = venta.fecha if venta.fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ancho = 44
        sep = "=" * ancho
        sub_sep = "-" * ancho

        lineas = [
            sep,
            "         SISTEMA DE GESTION DE VENTAS       ".center(ancho),
            "             CONTROL DE STOCK Y TPV         ".center(ancho),
            "          Desarrollado por: Gabriel Reina   ".center(ancho),
            "                     2do año                ".center(ancho),
            sep,
            f" COMPROBANTE: {venta.numero_factura}",
            f" FECHA: {fecha_str}",
            f" ATENDIDO POR: {usuario.nombre_completo if usuario else 'Vendedor'}",
            sub_sep,
            f" CLIENTE: {cliente.nombre if cliente else 'Consumidor Final'}",
            f" DOC/CUIT: {cliente.dni_cuit if cliente else '-'}",
            f" FORMA DE PAGO: {venta.metodo_pago}",
            sep,
            f"{'CANT':<5}{'DESCRIPCION':<20}{'P.UNIT':>9}{'SUBTOT':>10}",
            sub_sep
        ]

        for it in items:
            nombre_corto = (it.nombre_producto[:18] + "..") if len(it.nombre_producto) > 18 else it.nombre_producto
            lineas.append(f"{it.cantidad:<5}{nombre_corto:<20}${it.precio_unitario:>8.2f}${it.subtotal:>9.2f}")

        lineas.extend([
            sub_sep,
            f"{'SUBTOTAL:':<30}${venta.subtotal:>12.2f}",
            f"{'DESCUENTO:':<30}${venta.descuento:>12.2f}",
            f"{'TOTAL A PAGAR:':<30}${venta.total:>12.2f}",
            sep,
            "     GRACIAS POR SU COMPRA VUELVA PRONTO    ".center(ancho),
            sep
        ])

        return "\n".join(lineas)

    @staticmethod
    def guardar_ticket_archivo(texto_ticket, numero_factura, carpeta_salida="tickets"):
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)
        nombre_archivo = os.path.join(carpeta_salida, f"ticket_{numero_factura}.txt")
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(texto_ticket)
        return nombre_archivo
