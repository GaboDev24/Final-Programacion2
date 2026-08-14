import customtkinter as ctk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, TEXTO_PRINCIPAL, TEXTO_SECUNDARIO,
    TEXTO_MUTED, ACENTO_ROJO, BORDE_COLOR, FUENTE_TITULO,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_NORMAL_BOLD, FUENTE_PEQUENA
)
from views.componentes import BotonPrimario, BotonSecundario, CampoEntrada, DialogoAlerta

class VistaLogin(ctk.CTkFrame):
    def __init__(self, master, controlador_auth, al_iniciar_sesion):
        super().__init__(master, fg_color=BG_PRINCIPAL)
        self.controlador_auth = controlador_auth
        self.al_iniciar_sesion = al_iniciar_sesion

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        contenedor = ctk.CTkFrame(self, fg_color=BG_TARJETA, border_color=BORDE_COLOR, border_width=1, corner_radius=16, width=440)
        contenedor.grid(row=0, column=0, padx=20, pady=20)
        contenedor.grid_propagate(False)

        barra_decorativa = ctk.CTkFrame(contenedor, fg_color=ACENTO_ROJO, height=4, corner_radius=0)
        barra_decorativa.pack(fill="x")

        encabezado = ctk.CTkFrame(contenedor, fg_color="transparent")
        encabezado.pack(fill="x", padx=32, pady=(28, 16))

        lbl_marca = ctk.CTkLabel(encabezado, text="SISTEMA DE GESTION", font=FUENTE_TITULO, text_color=ACENTO_ROJO)
        lbl_marca.pack()

        lbl_sub = ctk.CTkLabel(encabezado, text="Control de Ventas y Stock", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO)
        lbl_sub.pack(pady=(2, 4))

        lbl_autor = ctk.CTkLabel(encabezado, text="Gabriel Reina - 2do ano", font=FUENTE_PEQUENA, text_color=TEXTO_MUTED)
        lbl_autor.pack()

        cuerpo = ctk.CTkFrame(contenedor, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=32, pady=10)

        self.campo_usuario = CampoEntrada(cuerpo, etiqueta="USUARIO", placeholder="Ej: admin o vendedor", valor_inicial="admin")
        self.campo_usuario.pack(fill="x", pady=(0, 14))

        self.campo_clave = CampoEntrada(cuerpo, etiqueta="CONTRASENA", placeholder="••••••••", es_password=True, valor_inicial="admin123")
        self.campo_clave.pack(fill="x", pady=(0, 20))

        self.btn_ingresar = BotonPrimario(cuerpo, text="INICIAR SESION", command=self._ejecutar_login, height=42)
        self.btn_ingresar.pack(fill="x", pady=(0, 12))

        self.campo_clave.entrada.bind("<Return>", lambda e: self._ejecutar_login())
        self.campo_usuario.entrada.bind("<Return>", lambda e: self._ejecutar_login())

        pie = ctk.CTkFrame(cuerpo, fg_color="transparent")
        pie.pack(fill="x", pady=(8, 0))

        lbl_demo = ctk.CTkLabel(pie, text="Accesos demo: admin/admin123 | vendedor/1234", font=FUENTE_PEQUENA, text_color=TEXTO_MUTED)
        lbl_demo.pack()

    def _ejecutar_login(self):
        usuario = self.campo_usuario.obtener()
        clave = self.campo_clave.obtener()

        try:
            usuario_autenticado = self.controlador_auth.iniciar_sesion(usuario, clave)
            if self.al_iniciar_sesion:
                self.al_iniciar_sesion(usuario_autenticado)
        except ValueError as e:
            DialogoAlerta(self.winfo_toplevel(), "Error de Autenticacion", str(e), tipo="error")
        except Exception as e:
            DialogoAlerta(self.winfo_toplevel(), "Error Inesperado", f"Ocurrio un error: {str(e)}", tipo="error")
