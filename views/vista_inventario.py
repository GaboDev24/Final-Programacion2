import customtkinter as ctk
import tkinter as tk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_INPUT, TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO, TEXTO_MUTED, ACENTO_ROJO, ACENTO_VERDE,
    ACENTO_AMARILLO, BORDE_COLOR, FUENTE_TITULO, FUENTE_SUBTITULO,
    FUENTE_NORMAL, FUENTE_NORMAL_BOLD, FUENTE_PEQUENA
)
from views.componentes import (
    Tarjeta, TarjetaEstadistica, BotonPrimario, BotonSecundario, BotonPeligro,
    BotonExito, CampoEntrada, TablaEstilizada, DialogoAlerta, DialogoConfirmar
)

class VistaInventario(ctk.CTkFrame):
    def __init__(self, master, controlador_inventario, controlador_proveedores, es_admin=True):
        super().__init__(master, fg_color="transparent")
        self.controlador_inv = controlador_inventario
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

        lbl_tit = ctk.CTkLabel(tit_frame, text="Inventario y Control de Stock", font=FUENTE_TITULO, text_color=TEXTO_PRINCIPAL)
        lbl_tit.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(tit_frame, text="Gestion integral de productos, existencias y precios", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO)
        lbl_sub.pack(anchor="w")

        if self.es_admin:
            btn_frame = ctk.CTkFrame(panel_sup, fg_color="transparent")
            btn_frame.pack(side="right")

            btn_cat = BotonSecundario(btn_frame, text="+ Categoria", command=self._modal_agregar_categoria, width=120)
            btn_cat.pack(side="left", padx=(0, 10))

            btn_nuevo = BotonPrimario(btn_frame, text="+ Nuevo Producto", command=self._modal_crear_producto, width=150)
            btn_nuevo.pack(side="left")

    def _crear_filtros(self):
        panel_filtros = Tarjeta(self)
        panel_filtros.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        fila = ctk.CTkFrame(panel_filtros, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=12)

        lbl_busc = ctk.CTkLabel(fila, text="Buscar:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_busc.pack(side="left", padx=(0, 8))

        self.ent_busqueda = ctk.CTkEntry(fila, placeholder_text="Codigo o nombre...", fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, width=220, height=36)
        self.ent_busqueda.pack(side="left", padx=(0, 16))
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_datos())

        lbl_cat = ctk.CTkLabel(fila, text="Categoria:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_cat.pack(side="left", padx=(0, 8))

        self.combo_categoria = ctk.CTkComboBox(fila, values=["Todas"], command=lambda v: self.cargar_datos(), fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, width=160, height=36)
        self.combo_categoria.pack(side="left", padx=(0, 16))

        self.var_stock_bajo = ctk.BooleanVar(value=False)
        self.chk_stock_bajo = ctk.CTkCheckBox(fila, text="Solo stock bajo o critico", variable=self.var_stock_bajo, command=self.cargar_datos, text_color=ACENTO_AMARILLO, fg_color=ACENTO_ROJO, checkmark_color="#ffffff")
        self.chk_stock_bajo.pack(side="left", padx=(0, 16))

        btn_limpiar = BotonSecundario(fila, text="Limpiar", command=self._limpiar_filtros, width=80, height=36)
        btn_limpiar.pack(side="right")

    def _crear_tabla(self):
        columnas = ("id", "codigo", "nombre", "categoria", "costo", "venta", "margen", "stock", "stock_min", "estado", "proveedor")
        encabezados = ("ID", "CODIGO", "NOMBRE", "CATEGORIA", "COSTO", "VENTA", "MARGEN", "STOCK", "MINIMO", "ESTADO", "PROVEEDOR")
        anchos = {
            "id": 40, "codigo": 90, "nombre": 180, "categoria": 110,
            "costo": 85, "venta": 85, "margen": 75, "stock": 65,
            "stock_min": 65, "estado": 100, "proveedor": 140
        }

        contenedor_tabla = ctk.CTkFrame(self, fg_color="transparent")
        contenedor_tabla.grid(row=2, column=0, sticky="nsew")
        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

        self.tabla = TablaEstilizada(contenedor_tabla, columnas, encabezados, anchos)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        if self.es_admin:
            panel_acciones = ctk.CTkFrame(contenedor_tabla, fg_color="transparent")
            panel_acciones.grid(row=1, column=0, sticky="ew", pady=(10, 0))

            btn_editar = BotonSecundario(panel_acciones, text="Editar Seleccionado", command=self._modal_editar_producto, width=160)
            btn_editar.pack(side="left", padx=(0, 10))

            btn_eliminar = BotonPeligro(panel_acciones, text="Eliminar Producto", command=self._confirmar_eliminar_producto, width=160)
            btn_eliminar.pack(side="left")

    def _limpiar_filtros(self):
        self.ent_busqueda.delete(0, tk.END)
        self.combo_categoria.set("Todas")
        self.var_stock_bajo.set(False)
        self.cargar_datos()

    def actualizar_categorias_combo(self):
        categorias = ["Todas"] + self.controlador_inv.obtener_categorias()
        self.combo_categoria.configure(values=categorias)

    def cargar_datos(self):
        self.actualizar_categorias_combo()
        busqueda = self.ent_busqueda.get()
        cat = self.combo_categoria.get()
        stock_bajo = self.var_stock_bajo.get()

        productos = self.controlador_inv.obtener_productos(
            busqueda=busqueda,
            categoria=cat,
            solo_stock_bajo=stock_bajo
        )

        self.tabla.limpiar()
        for p in productos:
            if p.stock <= 0:
                estado = "AGOTADO"
            elif p.tiene_stock_bajo:
                estado = "BAJO STOCK"
            else:
                estado = "NORMAL"

            prov = p.nombre_proveedor if p.nombre_proveedor else "-"
            valores = (
                p.id, p.codigo, p.nombre, p.categoria,
                f"${p.precio_costo:.2f}", f"${p.precio_venta:.2f}",
                f"{p.margen_ganancia:.1f}%", p.stock, p.stock_minimo,
                estado, prov
            )
            self.tabla.insertar_fila(valores)

    def _modal_crear_producto(self):
        self._abrir_formulario_producto(producto=None)

    def _modal_editar_producto(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Debe seleccionar un producto de la tabla para editar.", tipo="advertencia")
            return
        prod_id = fila[0]
        producto = self.controlador_inv.obtener_producto_por_id(prod_id)
        if producto:
            self._abrir_formulario_producto(producto=producto)

    def _confirmar_eliminar_producto(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Debe seleccionar un producto para eliminar.", tipo="advertencia")
            return
        prod_id = fila[0]
        prod_nom = fila[2]

        def eliminar():
            try:
                self.controlador_inv.eliminar_producto(prod_id)
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", f"Producto '{prod_nom}' eliminado correctamente.", tipo="exito")
            except Exception as e:
                DialogoAlerta(self.winfo_toplevel(), "Error", str(e), tipo="error")

        DialogoConfirmar(self.winfo_toplevel(), "Eliminar Producto", f"Desea eliminar el producto '{prod_nom}'?", eliminar)

    def _modal_agregar_categoria(self):
        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title("Nueva Categoria")
        modal.geometry("380x200")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text="Agregar Nueva Categoria", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 8))

        campo = CampoEntrada(modal, etiqueta="Nombre de Categoria", placeholder="Ej: Hardware")
        campo.pack(fill="x", padx=24, pady=8)

        def guardar():
            try:
                self.controlador_inv.agregar_categoria(campo.obtener())
                modal.destroy()
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", "Categoria agregada con exito.", tipo="exito")
            except Exception as e:
                DialogoAlerta(modal, "Error", str(e), tipo="error")

        btn = BotonPrimario(modal, text="Guardar Categoria", command=guardar, height=36)
        btn.pack(pady=(12, 16))

    def _abrir_formulario_producto(self, producto=None):
        es_edicion = producto is not None
        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title("Editar Producto" if es_edicion else "Nuevo Producto")
        modal.geometry("540x600")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text="Editar Producto" if es_edicion else "Alta de Producto", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 12))

        cuerpo = ctk.CTkScrollableFrame(modal, fg_color="transparent", width=480, height=440)
        cuerpo.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        c_codigo = CampoEntrada(cuerpo, etiqueta="Codigo", placeholder="PRD-XXXX", valor_inicial=producto.codigo if es_edicion else "")
        c_codigo.pack(fill="x", pady=4)

        c_nombre = CampoEntrada(cuerpo, etiqueta="Nombre del Producto", placeholder="Nombre descriptivo", valor_inicial=producto.nombre if es_edicion else "")
        c_nombre.pack(fill="x", pady=4)

        lbl_cat = ctk.CTkLabel(cuerpo, text="Categoria", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO, anchor="w")
        lbl_cat.pack(fill="x", pady=(6, 2))
        categorias = self.controlador_inv.obtener_categorias()
        combo_cat = ctk.CTkComboBox(cuerpo, values=categorias if categorias else ["General"], fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, height=36)
        if es_edicion and producto.category in categorias:
            combo_cat.set(producto.category)
        combo_cat.pack(fill="x", pady=4)

        f_precios = ctk.CTkFrame(cuerpo, fg_color="transparent")
        f_precios.pack(fill="x", pady=4)
        f_precios.grid_columnconfigure((0, 1), weight=1)

        c_costo = CampoEntrada(f_precios, etiqueta="Precio de Costo ($)", placeholder="0.00", valor_inicial=str(producto.cost_price) if es_edicion else "0.0")
        c_costo.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        c_venta = CampoEntrada(f_precios, etiqueta="Precio de Venta ($)", placeholder="0.00", valor_inicial=str(producto.sale_price) if es_edicion else "0.0")
        c_venta.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        f_stock = ctk.CTkFrame(cuerpo, fg_color="transparent")
        f_stock.pack(fill="x", pady=4)
        f_stock.grid_columnconfigure((0, 1), weight=1)

        c_stock = CampoEntrada(f_stock, etiqueta="Stock Actual", placeholder="0", valor_inicial=str(producto.stock) if es_edicion else "0")
        c_stock.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        c_stock_min = CampoEntrada(f_stock, etiqueta="Stock Minimo de Alerta", placeholder="5", valor_inicial=str(producto.min_stock) if es_edicion else "5")
        c_stock_min.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        lbl_prov = ctk.CTkLabel(cuerpo, text="Proveedor Asociado", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO, anchor="w")
        lbl_prov.pack(fill="x", pady=(6, 2))
        proveedores = self.controlador_prov.obtener_proveedores()
        opciones_prov = ["(Ninguno)"] + [f"{p.id} - {p.company_name if hasattr(p, 'company_name') else p.razon_social}" for p in proveedores]
        combo_prov = ctk.CTkComboBox(cuerpo, values=opciones_prov, fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, height=36)
        if es_edicion and producto.supplier_id:
            for op in opciones_prov:
                if op.startswith(f"{producto.supplier_id} -"):
                    combo_prov.set(op)
                    break
        combo_prov.pack(fill="x", pady=4)

        def guardar_producto():
            try:
                cod = c_codigo.obtener()
                nom = c_nombre.obtener()
                cat = combo_cat.get()
                cost = c_costo.obtener()
                vent = c_venta.obtener()
                stk = c_stock.obtener()
                stk_min = c_stock_min.obtener()

                prov_sel = combo_prov.get()
                prov_id = None
                if prov_sel and not prov_sel.startswith("(Ninguno)"):
                    prov_id = int(prov_sel.split(" - ")[0])

                if es_edicion:
                    self.controlador_inv.actualizar_producto(producto.id, cod, nom, cat, cost, vent, stk, stk_min, prov_id)
                else:
                    self.controlador_inv.crear_producto(cod, nom, cat, cost, vent, stk, stk_min, prov_id)

                modal.destroy()
                self.cargar_datos()
                DialogoAlerta(self.winfo_toplevel(), "Exito", "Producto guardado correctamente.", tipo="exito")
            except Exception as e:
                DialogoAlerta(modal, "Error al Guardar", str(e), tipo="error")

        btn_guardar = BotonPrimario(modal, text="Guardar Producto", command=guardar_producto, height=40)
        btn_guardar.pack(pady=(6, 16))
