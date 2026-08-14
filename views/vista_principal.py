import customtkinter as ctk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_INPUT, BG_SIDEBAR,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, TEXTO_MUTED, ACENTO_ROJO,
    ACENTO_VERDE, BORDE_COLOR,
    FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_NORMAL_BOLD,
    FUENTE_PEQUENA
)
from views.vista_ventas import VistaVentas
from views.vista_inventario import VistaInventario
from views.vista_clientes import VistaClientes
from views.vista_proveedores import VistaProveedores
from views.vista_compras import VistaCompras
from views.vista_reportes import VistaReportes
from views.vista_usuarios import VistaUsuarios

class VistaPrincipal(ctk.CTkFrame):
    def __init__(self, master, usuario_actual, controladores, al_cerrar_sesion):
        super().__init__(master, fg_color=BG_PRINCIPAL)
        self.usuario_actual = usuario_actual
        self.controladores = controladores
        self.al_cerrar_sesion = al_cerrar_sesion

        self.es_admin = self.usuario_actual.es_admin() if hasattr(self.usuario_actual, "es_admin") else (self.usuario_actual.rol == "Administrador")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.botones_nav = {}
        self.vista_activa = None

        self._crear_sidebar()
        self._crear_contenedor_vistas()
        self._navegar("ventas")

    def _crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(2, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        f_logo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        f_logo.grid(row=0, column=0, sticky="ew", padx=20, pady=(24, 16))

        lbl_logo = ctk.CTkLabel(f_logo, text="SISTEMA POS", font=("Segoe UI", 18, "bold"), text_color=ACENTO_ROJO)
        lbl_logo.pack(anchor="w")

        lbl_sublogo = ctk.CTkLabel(f_logo, text="Ventas y Control de Stock", font=FUENTE_PEQUENA, text_color=TEXTO_MUTED)
        lbl_sublogo.pack(anchor="w")

        lbl_autor = ctk.CTkLabel(f_logo, text="Gabriel Reina - 2do ano", font=("Segoe UI", 10, "bold"), text_color=TEXTO_SECUNDARIO)
        lbl_autor.pack(anchor="w", pady=(2, 0))

        sep1 = ctk.CTkFrame(self.sidebar, fg_color=BORDE_COLOR, height=1)
        sep1.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))

        f_menu = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        f_menu.grid(row=2, column=0, sticky="nsew", padx=10, pady=0)
        f_menu.grid_columnconfigure(0, weight=1)

        modulos = [
            ("ventas", "Punto de Venta (TPV)", True),
            ("inventario", "Inventario y Stock", True),
            ("clientes", "Clientes", True),
            ("proveedores", "Proveedores", self.es_admin),
            ("compras", "Abastecimiento", self.es_admin),
            ("reportes", "Reportes y Caja", self.es_admin),
            ("usuarios", "Control de Acceso", self.es_admin)
        ]

        for clave, etiqueta, visible in modulos:
            if visible:
                btn = ctk.CTkButton(
                    f_menu, text=etiqueta, anchor="w",
                    fg_color="transparent", text_color=TEXTO_SECUNDARIO,
                    hover_color=BG_TARJETA, font=FUENTE_NORMAL,
                    height=40, corner_radius=8,
                    command=lambda k=clave: self._navegar(k)
                )
                btn.pack(fill="x", pady=2)
                self.botones_nav[clave] = btn

        f_usuario = ctk.CTkFrame(self.sidebar, fg_color=BG_SECUNDARIO, corner_radius=10, border_color=BORDE_COLOR, border_width=1)
        f_usuario.grid(row=3, column=0, sticky="ew", padx=14, pady=16)

        nombre_usr = self.usuario_actual.full_name if hasattr(self.usuario_actual, "full_name") else self.usuario_actual.nombre_completo
        lbl_unom = ctk.CTkLabel(f_usuario, text=nombre_usr, font=FUENTE_NORMAL_BOLD, text_color=TEXTO_PRINCIPAL, anchor="w")
        lbl_unom.pack(fill="x", padx=12, pady=(10, 0))

        color_rol = ACENTO_ROJO if self.es_admin else TEXTO_SECUNDARIO
        lbl_urol = ctk.CTkLabel(f_usuario, text=f"{self.usuario_actual.rol}", font=FUENTE_PEQUENA, text_color=color_rol, anchor="w")
        lbl_urol.pack(fill="x", padx=12, pady=(0, 8))

        btn_salir = ctk.CTkButton(
            f_usuario, text="Cerrar Sesion", fg_color=BG_INPUT,
            text_color=ACENTO_ROJO, hover_color="#2c1418",
            font=FUENTE_PEQUENA, height=30, corner_radius=6,
            command=self._ejecutar_cierre_sesion
        )
        btn_salir.pack(fill="x", padx=12, pady=(0, 10))

    def _crear_contenedor_vistas(self):
        self.contenedor_vistas = ctk.CTkFrame(self, fg_color=BG_PRINCIPAL)
        self.contenedor_vistas.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.contenedor_vistas.grid_rowconfigure(0, weight=1)
        self.contenedor_vistas.grid_columnconfigure(0, weight=1)

    def _navegar(self, clave_modulo):
        for k, btn in self.botones_nav.items():
            if k == clave_modulo:
                btn.configure(fg_color=BG_TARJETA, text_color=ACENTO_ROJO, font=FUENTE_NORMAL_BOLD)
            else:
                btn.configure(fg_color="transparent", text_color=TEXTO_SECUNDARIO, font=FUENTE_NORMAL)

        if self.vista_activa:
            self.vista_activa.destroy()

        if clave_modulo == "ventas":
            self.vista_activa = VistaVentas(
                self.contenedor_vistas,
                self.controladores["ventas"],
                self.controladores["inventario"],
                self.controladores["clientes"],
                self.usuario_actual
            )
        elif clave_modulo == "inventario":
            self.vista_activa = VistaInventario(
                self.contenedor_vistas,
                self.controladores["inventario"],
                self.controladores["proveedores"],
                self.es_admin
            )
        elif clave_modulo == "clientes":
            self.vista_activa = VistaClientes(
                self.contenedor_vistas,
                self.controladores["clientes"],
                self.es_admin
            )
        elif clave_modulo == "proveedores":
            self.vista_activa = VistaProveedores(
                self.contenedor_vistas,
                self.controladores["proveedores"],
                self.es_admin
            )
        elif clave_modulo == "compras":
            self.vista_activa = VistaCompras(
                self.contenedor_vistas,
                self.controladores["compras"],
                self.controladores["inventario"],
                self.controladores["proveedores"],
                self.usuario_actual
            )
        elif clave_modulo == "reportes":
            self.vista_activa = VistaReportes(
                self.contenedor_vistas,
                self.controladores["reportes"],
                self.controladores["ventas"],
                self.controladores["clientes"],
                self.controladores["auth"]
            )
        elif clave_modulo == "usuarios":
            self.vista_activa = VistaUsuarios(
                self.contenedor_vistas,
                self.controladores["usuarios"]
            )

        if self.vista_activa:
            self.vista_activa.grid(row=0, column=0, sticky="nsew")

    def _ejecutar_cierre_sesion(self):
        if self.al_cerrar_sesion:
            self.al_cerrar_sesion()
