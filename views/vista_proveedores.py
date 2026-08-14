import customtkinter as ctk
import tkinter as tk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_INPUT, TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO, TEXTO_MUTED, ACENTO_ROJO, ACENTO_VERDE,
    BORDE_COLOR, FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL,
    FUENTE_NORMAL_BOLD, FUENTE_PEQUENA
)
from views.componentes import (
    Tarjeta, BotonPrimario, BotonSecundario, BotonPeligro,
    CampoEntrada, TablaEstilizada, DialogoAlerta, DialogoConfirmar
)

class VistaProveedores(ctk.CTkFrame):
    def __init__(self, master, controlador_proveedores, es_admin=True):
        super().__init__(master, fg_color="transparent")
        self.controlador_prov = controlador_proveedores
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

        lbl_tit = ctk.CTkLabel(tit_frame, text="Gestion de Proveedores", font=FUENTE_TITULO, text_color=TEXTO_PRINCIPAL)
        lbl_tit.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(tit_frame, text="Registro y administracion de distribuidores y empresas asociadas", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO)
        lbl_sub.pack(anchor="w")

        if self.es_admin:
            btn_nuevo = BotonPrimario(panel_sup, text="+ Nuevo Proveedor", command=self._modal_crear_proveedor, width=150)
            btn_nuevo.pack(side="right")

    def _crear_filtros(self):
        panel_filtros = Tarjeta(self)
        panel_filtros.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        fila = ctk.CTkFrame(panel_filtros, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=12)

        lbl = ctk.CTkLabel(fila, text="Buscar:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl.pack(side="left", padx=(0, 8))

        self.ent_busqueda = ctk.CTkEntry(fila, placeholder_text="CUIT, razon social o contacto...", fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, width=280, height=36)
        self.ent_busqueda.pack(side="left", padx=(0, 16))
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_datos())

        btn_limpiar = BotonSecundario(fila, text="Limpiar", command=self._limpiar_filtros, width=80, height=36)
        btn_limpiar.pack(side="right")

    def _crear_tabla(self):
        columnas = ("id", "cuit", "razon_social", "contacto", "telefono", "email", "direccion")
        encabezados = ("ID", "CUIT", "RAZON SOCIAL", "CONTACTO", "TELEFONO", "EMAIL", "DIRECCION")
        anchos = {"id": 40, "cuit": 110, "razon_social": 180, "contacto": 130, "telefono": 110, "email": 160, "direccion": 170}

        contenedor_tabla = ctk.CTkFrame(self, fg_color="transparent")
        contenedor_tabla.grid(row=2, column=0, sticky="nsew")
        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

        self.tabla = TablaEstilizada(contenedor_tabla, columnas, encabezados, anchos)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        if self.es_admin:
            panel_acciones = ctk.CTkFrame(contenedor_tabla, fg_color="transparent")
            panel_acciones.grid(row=1, column=0, sticky="ew", pady=(10, 0))

            btn_editar = BotonSecundario(panel_acciones, text="Editar Proveedor", command=self._modal_editar_proveedor, width=140)
            btn_editar.pack(side="left", padx=(0, 10))

            btn_eliminar = BotonPeligro(panel_acciones, text="Eliminar Proveedor", command=self._confirmar_eliminar_proveedor, width=140)
            btn_eliminar.pack(side="left")

    def _limpiar_filtros(self):
        self.ent_busqueda.delete(0, tk.END)
        self.cargar_datos()

    def cargar_datos(self):
        busqueda = self.ent_busqueda.get()
        proveedores = self.controlador_prov.obtener_proveedores(busqueda=busqueda)
        self.tabla.limpiar()
        for p in proveedores:
            rz = p.company_name if hasattr(p, "company_name") else p.razon_social
            ct = p.contact_name if hasattr(p, "contact_name") else p.contacto
            tl = p.phone if hasattr(p, "phone") else p.telefono
            dr = p.address if hasattr(p, "address") else p.direccion
            valores = (p.id, p.cuit, rz, ct, tl, p.email, dr)
            self.tabla.insertar_fila(valores)

    def _modal_crear_proveedor(self):
        self._abrir_formulario_proveedor(proveedor=None)

    def _modal_editar_proveedor(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un proveedor para editar.", tipo="advertencia")
            return
        prov_id = fila[0]
        prov = self.controlador_prov.obtener_proveedor_por_id(prov_id)
        if prov:
            self._abrir_formulario_proveedor(proveedor=prov)

    def _confirmar_eliminar_proveedor(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un proveedor para eliminar.", tipo="advertencia")
            return
        prov_id = fila[0]
        prov_rz = fila[2]

        def eliminar():
            try:
                self.controlador_prov.eliminar_proveedor(prov_id)
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", f"Proveedor '{prov_rz}' eliminado correctamente.", tipo="exito")
            except Exception as e:
                DialogoAlerta(self.winfo_toplevel(), "Error", str(e), tipo="error")

        DialogoConfirmar(self.winfo_toplevel(), "Eliminar Proveedor", f"Desea eliminar el proveedor '{prov_rz}'?", eliminar)

    def _abrir_formulario_proveedor(self, proveedor=None):
        es_edicion = proveedor is not None
        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title("Editar Proveedor" if es_edicion else "Nuevo Proveedor")
        modal.geometry("460x510")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text="Editar Proveedor" if es_edicion else "Alta de Proveedor", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 12))

        cuerpo = ctk.CTkFrame(modal, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=24, pady=6)

        c_cuit = CampoEntrada(cuerpo, etiqueta="CUIT", placeholder="Ej: 30-12345678-9", valor_inicial=proveedor.cuit if es_edicion else "")
        c_cuit.pack(fill="x", pady=4)

        rz_val = (proveedor.company_name if hasattr(proveedor, "company_name") else proveedor.razon_social) if es_edicion else ""
        c_razon = CampoEntrada(cuerpo, etiqueta="Razon Social", placeholder="Nombre de la empresa", valor_inicial=rz_val)
        c_razon.pack(fill="x", pady=4)

        ct_val = (proveedor.contact_name if hasattr(proveedor, "contact_name") else proveedor.contacto) if es_edicion else ""
        c_contacto = CampoEntrada(cuerpo, etiqueta="Persona de Contacto", placeholder="Nombre del representante", valor_inicial=ct_val)
        c_contacto.pack(fill="x", pady=4)

        tl_val = (proveedor.phone if hasattr(proveedor, "phone") else proveedor.telefono) if es_edicion else ""
        c_tel = CampoEntrada(cuerpo, etiqueta="Telefono", placeholder="Ej: 11-4567-8900", valor_inicial=tl_val)
        c_tel.pack(fill="x", pady=4)

        c_email = CampoEntrada(cuerpo, etiqueta="Email", placeholder="ventas@proveedor.com", valor_inicial=proveedor.email if es_edicion else "")
        c_email.pack(fill="x", pady=4)

        dr_val = (proveedor.address if hasattr(proveedor, "address") else proveedor.direccion) if es_edicion else ""
        c_dir = CampoEntrada(cuerpo, etiqueta="Direccion", placeholder="Calle, Numero, Ciudad", valor_inicial=dr_val)
        c_dir.pack(fill="x", pady=4)

        def guardar():
            try:
                cuit = c_cuit.obtener()
                razon = c_razon.obtener()
                contacto = c_contacto.obtener()
                tel = c_tel.obtener()
                email = c_email.obtener()
                direc = c_dir.obtener()

                if es_edicion:
                    self.controlador_prov.actualizar_proveedor(proveedor.id, cuit, razon, contacto, tel, email, direc)
                else:
                    self.controlador_prov.crear_proveedor(cuit, razon, contacto, tel, email, direc)

                modal.destroy()
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", "Proveedor guardado con exito.", tipo="exito")
            except Exception as e:
                DialogoAlerta(modal, "Error", str(e), tipo="error")

        btn_guardar = BotonPrimario(modal, text="Guardar Proveedor", command=guardar, height=38)
        btn_guardar.pack(pady=(8, 16))
