import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from database.gestor_bd import GestorBD
from controllers.controlador_autenticacion import ControladorAutenticacion
from controllers.controlador_inventario import ControladorInventario
from controllers.controlador_ventas import ControladorVentas
from controllers.controlador_clientes import ControladorClientes
from controllers.controlador_proveedores import ControladorProveedores
from controllers.controlador_compras import ControladorCompras
from controllers.controlador_reportes import ControladorReportes
from controllers.controlador_usuarios import ControladorUsuarios
from views.tema import BG_PRINCIPAL
from views.vista_login import VistaLogin
from views.vista_principal import VistaPrincipal

class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Sistema de Gestión de Ventas y Control de Stock — Gabriel Reina 2do año")
        self.geometry("1200x750")
        self.minsize(1050, 680)
        self.configure(fg_color=BG_PRINCIPAL)

        self.gestor_bd = GestorBD()

        self.controlador_auth = ControladorAutenticacion(self.gestor_bd)
        self.controlador_inv = ControladorInventario(self.gestor_bd)
        self.controlador_vta = ControladorVentas(self.gestor_bd)
        self.controlador_cli = ControladorClientes(self.gestor_bd)
        self.controlador_prov = ControladorProveedores(self.gestor_bd)
        self.controlador_cmp = ControladorCompras(self.gestor_bd)
        self.controlador_rep = ControladorReportes(self.gestor_bd)
        self.controlador_usr = ControladorUsuarios(self.gestor_bd)

        self.controladores = {
            "auth": self.controlador_auth,
            "inventario": self.controlador_inv,
            "ventas": self.controlador_vta,
            "clientes": self.controlador_cli,
            "proveedores": self.controlador_prov,
            "compras": self.controlador_cmp,
            "reportes": self.controlador_rep,
            "usuarios": self.controlador_usr
        }

        self.vista_actual = None
        self.mostrar_login()

    def mostrar_login(self):
        if self.vista_actual:
            self.vista_actual.destroy()

        self.vista_actual = VistaLogin(
            self,
            controlador_auth=self.controlador_auth,
            al_iniciar_sesion=self.mostrar_dashboard
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_dashboard(self, usuario):
        if self.vista_actual:
            self.vista_actual.destroy()

        self.vista_actual = VistaPrincipal(
            self,
            usuario_actual=usuario,
            controladores=self.controladores,
            al_cerrar_sesion=self._al_cerrar_sesion
        )
        self.vista_actual.pack(fill="both", expand=True)

    def _al_cerrar_sesion(self):
        self.controlador_auth.cerrar_sesion()
        self.mostrar_login()

if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.mainloop()
