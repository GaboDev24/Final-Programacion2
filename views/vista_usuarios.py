import customtkinter as ctk
import tkinter as tk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_INPUT, TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO, TEXTO_MUTED, ACENTO_ROJO, ACENTO_VERDE,
    BORDE_COLOR, FUENTE_TITULO, FUENTE_SUBTITULO,
    FUENTE_NORMAL, FUENTE_NORMAL_BOLD, FUENTE_PEQUENA
)
from views.componentes import (
    Tarjeta, BotonPrimario, BotonSecundario, BotonPeligro,
    CampoEntrada, TablaEstilizada, DialogoAlerta, DialogoConfirmar
)

class VistaUsuarios(ctk.CTkFrame):
    def __init__(self, master, controlador_usuarios):
        super().__init__(master, fg_color="transparent")
        self.controlador_usr = controlador_usuarios

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_encabezado()
        self._crear_filtros()
        self._crear_tabla()
        self.cargar_datos()

    def _crear_encabezado(self):
        panel_sup = ctk.CTkFrame(self, fg_color="transparent")
        panel_sup.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        panel_sup.grid_columnconfigure(0, weight=1)

        tit_frame = ctk.CTkFrame(panel_sup, fg_color="transparent")
        tit_frame.pack(side="left")

        lbl_tit = ctk.CTkLabel(tit_frame, text="Control de Acceso y Usuarios", font=FUENTE_TITULO, text_color=TEXTO_PRINCIPAL)
        lbl_tit.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(tit_frame, text="Administracion de cuentas y asignacion de roles del sistema", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO)
        lbl_sub.pack(anchor="w")

        btn_nuevo = BotonPrimario(panel_sup, text="+ Nuevo Usuario", command=self._modal_crear_usuario, width=150)
        btn_nuevo.pack(side="right")

    def _crear_filtros(self):
        panel_filtros = Tarjeta(self)
        panel_filtros.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        fila = ctk.CTkFrame(panel_filtros, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=12)

        lbl = ctk.CTkLabel(fila, text="Buscar:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl.pack(side="left", padx=(0, 8))

        self.ent_busqueda = ctk.CTkEntry(fila, placeholder_text="Usuario o nombre completo...", fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, width=280, height=36)
        self.ent_busqueda.pack(side="left", padx=(0, 16))
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_datos())

        btn_limpiar = BotonSecundario(fila, text="Limpiar", command=self._limpiar_filtros, width=80, height=36)
        btn_limpiar.pack(side="right")

    def _crear_tabla(self):
        columnas = ("id", "usuario", "nombre", "rol", "fecha")
        encabezados = ("ID", "NOMBRE DE USUARIO", "NOMBRE COMPLETO", "ROL ASIGNADO", "FECHA DE ALTA")
        anchos = {"id": 40, "usuario": 140, "nombre": 220, "rol": 130, "fecha": 150}

        contenedor_tabla = ctk.CTkFrame(self, fg_color="transparent")
        contenedor_tabla.grid(row=2, column=0, sticky="nsew")
        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

        self.tabla = TablaEstilizada(contenedor_tabla, columnas, encabezados, anchos)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        panel_acciones = ctk.CTkFrame(contenedor_tabla, fg_color="transparent")
        panel_acciones.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        btn_editar = BotonSecundario(panel_acciones, text="Editar Usuario", command=self._modal_editar_usuario, width=140)
        btn_editar.pack(side="left", padx=(0, 10))

        btn_desactivar = BotonPeligro(panel_acciones, text="Desactivar Cuenta", command=self._confirmar_desactivar_usuario, width=150)
        btn_desactivar.pack(side="left")

    def _limpiar_filtros(self):
        self.ent_busqueda.delete(0, tk.END)
        self.cargar_datos()

    def cargar_datos(self):
        busqueda = self.ent_busqueda.get()
        usuarios = self.controlador_usr.obtener_usuarios(busqueda=busqueda)
        self.tabla.limpiar()
        for u in usuarios:
            usr = u.username if hasattr(u, "username") else u.nombre_usuario
            nom = u.full_name if hasattr(u, "full_name") else u.nombre_completo
            fch = u.created_at if hasattr(u, "created_at") else u.fecha_creacion
            valores = (u.id, usr, nom, u.rol, fch if fch else "-")
            self.tabla.insertar_fila(valores)

    def _modal_crear_usuario(self):
        self._abrir_formulario_usuario(usuario=None)

    def _modal_editar_usuario(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un usuario para editar.", tipo="advertencia")
            return
        usr_id = fila[0]
        usuarios = self.controlador_usr.obtener_usuarios()
        usuario_obj = next((u for u in usuarios if u.id == usr_id), None)
        if usuario_obj:
            self._abrir_formulario_usuario(usuario=usuario_obj)

    def _confirmar_desactivar_usuario(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un usuario para desactivar.", tipo="advertencia")
            return
        usr_id = fila[0]
        usr_nombre = fila[1]

        if usr_id == 1:
            DialogoAlerta(self.winfo_toplevel(), "Operacion no permitida", "No se puede desactivar la cuenta principal de Administrador.", tipo="error")
            return

        def desactivar():
            try:
                self.controlador_usr.desactivar_usuario(usr_id)
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", f"Usuario '{usr_nombre}' desactivado.", tipo="exito")
            except Exception as e:
                DialogoAlerta(self.winfo_toplevel(), "Error", str(e), tipo="error")

        DialogoConfirmar(self.winfo_toplevel(), "Desactivar Usuario", f"Desea desactivar la cuenta de '{usr_nombre}'?", desactivar)

    def _abrir_formulario_usuario(self, usuario=None):
        es_edicion = usuario is not None
        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title("Editar Usuario" if es_edicion else "Nuevo Usuario")
        modal.geometry("440x460")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text="Editar Cuenta" if es_edicion else "Alta de Usuario", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 12))

        cuerpo = ctk.CTkFrame(modal, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=24, pady=6)

        usr_val = (usuario.username if hasattr(usuario, "username") else usuario.nombre_usuario) if es_edicion else ""
        c_usuario = CampoEntrada(cuerpo, etiqueta="Nombre de Usuario", placeholder="Ej: jsmith", valor_inicial=usr_val)
        c_usuario.pack(fill="x", pady=4)

        c_clave = CampoEntrada(cuerpo, etiqueta="Contrasena" if not es_edicion else "Nueva Contrasena (dejar en blanco para mantener)", placeholder="••••••••", es_password=True)
        c_clave.pack(fill="x", pady=4)

        nom_val = (usuario.full_name if hasattr(usuario, "full_name") else usuario.nombre_completo) if es_edicion else ""
        c_nombre = CampoEntrada(cuerpo, etiqueta="Nombre Completo", placeholder="Ej: Juan Smith", valor_inicial=nom_val)
        c_nombre.pack(fill="x", pady=4)

        lbl_rol = ctk.CTkLabel(cuerpo, text="Rol del Sistema", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO, anchor="w")
        lbl_rol.pack(fill="x", pady=(6, 2))

        combo_rol = ctk.CTkComboBox(cuerpo, values=["Vendedor", "Administrador"], fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, height=36)
        if es_edicion:
            combo_rol.set(usuario.rol)
        combo_rol.pack(fill="x", pady=4)

        def guardar():
            try:
                usr = c_usuario.obtener()
                pwd = c_clave.obtener()
                nom = c_nombre.obtener()
                rol = combo_rol.get()

                if es_edicion:
                    self.controlador_usr.actualizar_usuario(usuario.id, usr, pwd, nom, rol)
                else:
                    self.controlador_usr.crear_usuario(usr, pwd, nom, rol)

                modal.destroy()
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", "Usuario guardado con exito.", tipo="exito")
            except Exception as e:
                DialogoAlerta(modal, "Error", str(e), tipo="error")

        btn_guardar = BotonPrimario(modal, text="Guardar Usuario", command=guardar, height=38)
        btn_guardar.pack(pady=(8, 16))
