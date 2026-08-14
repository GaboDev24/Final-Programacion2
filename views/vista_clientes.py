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

class VistaClientes(ctk.CTkFrame):
    def __init__(self, master, controlador_clientes, es_admin=True):
        super().__init__(master, fg_color="transparent")
        self.controlador_cli = controlador_clientes
        self.es_admin = es_admin

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

        lbl_tit = ctk.CTkLabel(tit_frame, text="Gestion de Clientes", font=FUENTE_TITULO, text_color=TEXTO_PRINCIPAL)
        lbl_tit.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(tit_frame, text="Padron de clientes, contactos e historial de compras", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO)
        lbl_sub.pack(anchor="w")

        btn_nuevo = BotonPrimario(panel_sup, text="+ Nuevo Cliente", command=self._modal_crear_cliente, width=140)
        btn_nuevo.pack(side="right")

    def _crear_filtros(self):
        panel_filtros = Tarjeta(self)
        panel_filtros.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        fila = ctk.CTkFrame(panel_filtros, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=12)

        lbl = ctk.CTkLabel(fila, text="Buscar:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl.pack(side="left", padx=(0, 8))

        self.ent_busqueda = ctk.CTkEntry(fila, placeholder_text="DNI, CUIT, nombre o telefono...", fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, width=280, height=36)
        self.ent_busqueda.pack(side="left", padx=(0, 16))
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_datos())

        btn_limpiar = BotonSecundario(fila, text="Limpiar", command=self._limpiar_filtros, width=80, height=36)
        btn_limpiar.pack(side="right")

    def _crear_tabla(self):
        columnas = ("id", "dni", "nombre", "telefono", "email", "direccion")
        encabezados = ("ID", "DNI / CUIT", "NOMBRE O RAZON SOCIAL", "TELEFONO", "EMAIL", "DIRECCION")
        anchos = {"id": 40, "dni": 110, "nombre": 180, "telefono": 120, "email": 160, "direccion": 180}

        contenedor_tabla = ctk.CTkFrame(self, fg_color="transparent")
        contenedor_tabla.grid(row=2, column=0, sticky="nsew")
        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

        self.tabla = TablaEstilizada(contenedor_tabla, columnas, encabezados, anchos)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        panel_acciones = ctk.CTkFrame(contenedor_tabla, fg_color="transparent")
        panel_acciones.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        btn_editar = BotonSecundario(panel_acciones, text="Editar Cliente", command=self._modal_editar_cliente, width=130)
        btn_editar.pack(side="left", padx=(0, 10))

        btn_historial = BotonSecundario(panel_acciones, text="Historial de Compras", command=self._ver_historial_cliente, width=160)
        btn_historial.pack(side="left", padx=(0, 10))

        if self.es_admin:
            btn_eliminar = BotonPeligro(panel_acciones, text="Eliminar Cliente", command=self._confirmar_eliminar_cliente, width=130)
            btn_eliminar.pack(side="left")

    def _limpiar_filtros(self):
        self.ent_busqueda.delete(0, tk.END)
        self.cargar_datos()

    def cargar_datos(self):
        busqueda = self.ent_busqueda.get()
        clientes = self.controlador_cli.obtener_clientes(busqueda=busqueda)
        self.tabla.limpiar()
        for c in clientes:
            valores = (c.id, c.dni_cuit, c.name if hasattr(c, "name") else c.nombre, c.phone if hasattr(c, "phone") else c.telefono, c.email, c.address if hasattr(c, "address") else c.direccion)
            self.tabla.insertar_fila(valores)

    def _modal_crear_cliente(self):
        self._abrir_formulario_cliente(cliente=None)

    def _modal_editar_cliente(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un cliente para editar.", tipo="advertencia")
            return
        cli_id = fila[0]
        cliente = self.controlador_cli.obtener_cliente_por_id(cli_id)
        if cliente:
            self._abrir_formulario_cliente(cliente=cliente)

    def _confirmar_eliminar_cliente(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un cliente para eliminar.", tipo="advertencia")
            return
        cli_id = fila[0]
        cli_nom = fila[2]

        if cli_id == 1:
            DialogoAlerta(self.winfo_toplevel(), "Operacion no permitida", "No se puede eliminar el cliente 'Consumidor Final'.", tipo="error")
            return

        def eliminar():
            try:
                self.controlador_cli.eliminar_cliente(cli_id)
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", f"Cliente '{cli_nom}' eliminado correctamente.", tipo="exito")
            except Exception as e:
                DialogoAlerta(self.winfo_toplevel(), "Error", str(e), tipo="error")

        DialogoConfirmar(self.winfo_toplevel(), "Eliminar Cliente", f"Desea eliminar al cliente '{cli_nom}'?", eliminar)

    def _abrir_formulario_cliente(self, cliente=None):
        es_edicion = cliente is not None
        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title("Editar Cliente" if es_edicion else "Nuevo Cliente")
        modal.geometry("460x480")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text="Editar Cliente" if es_edicion else "Alta de Cliente", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 12))

        cuerpo = ctk.CTkFrame(modal, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=24, pady=6)

        c_dni = CampoEntrada(cuerpo, etiqueta="DNI / CUIT", placeholder="Sin puntos ni guiones", valor_inicial=cliente.dni_cuit if es_edicion else "")
        c_dni.pack(fill="x", pady=4)

        nom_val = (cliente.name if hasattr(cliente, "name") else cliente.nombre) if es_edicion else ""
        c_nombre = CampoEntrada(cuerpo, etiqueta="Nombre Completo o Razon Social", placeholder="Nombre del cliente", valor_inicial=nom_val)
        c_nombre.pack(fill="x", pady=4)

        tel_val = (cliente.phone if hasattr(cliente, "phone") else cliente.telefono) if es_edicion else ""
        c_tel = CampoEntrada(cuerpo, etiqueta="Telefono", placeholder="Ej: 11-1234-5678", valor_inicial=tel_val)
        c_tel.pack(fill="x", pady=4)

        c_email = CampoEntrada(cuerpo, etiqueta="Email", placeholder="cliente@correo.com", valor_inicial=cliente.email if es_edicion else "")
        c_email.pack(fill="x", pady=4)

        dir_val = (cliente.address if hasattr(cliente, "address") else cliente.direccion) if es_edicion else ""
        c_dir = CampoEntrada(cuerpo, etiqueta="Direccion", placeholder="Calle, Numero, Localidad", valor_inicial=dir_val)
        c_dir.pack(fill="x", pady=4)

        def guardar():
            try:
                dni = c_dni.obtener()
                nom = c_nombre.obtener()
                tel = c_tel.obtener()
                email = c_email.obtener()
                direc = c_dir.obtener()

                if es_edicion:
                    self.controlador_cli.actualizar_cliente(cliente.id, dni, nom, tel, email, direc)
                else:
                    self.controlador_cli.crear_cliente(dni, nom, tel, email, direc)

                modal.destroy()
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", "Cliente guardado con exito.", tipo="exito")
            except Exception as e:
                DialogoAlerta(modal, "Error", str(e), tipo="error")

        btn_guardar = BotonPrimario(modal, text="Guardar Cliente", command=guardar, height=38)
        btn_guardar.pack(pady=(8, 16))

    def _ver_historial_cliente(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un cliente para ver su historial.", tipo="advertencia")
            return

        cli_id = fila[0]
        cli_nom = fila[2]
        ventas = self.controlador_cli.obtener_historial_compras_cliente(cli_id)

        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title(f"Historial de Compras - {cli_nom}")
        modal.geometry("640x460")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text=f"Historial de Compras: {cli_nom}", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 10))

        cols = ("factura", "fecha", "pago", "total", "atendido")
        encs = ("N FACTURA", "FECHA", "METODO PAGO", "TOTAL", "VENDEDOR")
        anchos = {"factura": 120, "fecha": 140, "pago": 110, "total": 90, "atendido": 130}

        tabla_hist = TablaEstilizada(modal, cols, encs, anchos)
        tabla_hist.pack(fill="both", expand=True, padx=20, pady=10)

        for v in ventas:
            tabla_hist.insertar_fila((v["numero_factura"], v["fecha"], v["metodo_pago"], f"${v['total']:.2f}", v["nombre_usuario"]))

        btn_cerrar = BotonSecundario(modal, text="Cerrar", command=modal.destroy, width=120)
        btn_cerrar.pack(pady=(4, 14))
