import customtkinter as ctk
import tkinter as tk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_INPUT, TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO, TEXTO_MUTED, ACENTO_ROJO, ACENTO_VERDE,
    ACENTO_AMARILLO, BORDE_COLOR, FUENTE_TITULO, FUENTE_SUBTITULO,
    FUENTE_NORMAL, FUENTE_NORMAL_BOLD, FUENTE_PEQUENA, FUENTE_MONO, FUENTE_MONO_BOLD
)
from views.componentes import (
    Tarjeta, BotonPrimario, BotonSecundario, BotonPeligro, BotonExito,
    CampoEntrada, TablaEstilizada, DialogoAlerta, DialogoConfirmar
)

class VistaVentas(ctk.CTkFrame):
    def __init__(self, master, controlador_ventas, controlador_inventario, controlador_clientes, usuario_actual):
        super().__init__(master, fg_color="transparent")
        self.controlador_ventas = controlador_ventas
        self.controlador_inv = controlador_inventario
        self.controlador_cli = controlador_clientes
        self.usuario_actual = usuario_actual

        self.carrito = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        self._crear_encabezado()
        self._crear_panel_catalogo()
        self._crear_panel_carrito()
        self.cargar_catalogo()
        self.cargar_clientes()

    def _crear_encabezado(self):
        panel_sup = ctk.CTkFrame(self, fg_color="transparent")
        panel_sup.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        lbl_tit = ctk.CTkLabel(panel_sup, text="Terminal de Punto de Venta (TPV)", font=FUENTE_TITULO, text_color=TEXTO_PRINCIPAL)
        lbl_tit.pack(side="left")

        nom_op = self.usuario_actual.full_name if hasattr(self.usuario_actual, 'full_name') else self.usuario_actual.nombre_completo
        lbl_user = ctk.CTkLabel(panel_sup, text=f"Operador: {nom_op}", font=FUENTE_NORMAL_BOLD, text_color=ACENTO_ROJO)
        lbl_user.pack(side="right")

    def _crear_panel_catalogo(self):
        panel_izq = Tarjeta(self)
        panel_izq.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        panel_izq.grid_rowconfigure(2, weight=1)
        panel_izq.grid_columnconfigure(0, weight=1)

        fila_busc = ctk.CTkFrame(panel_izq, fg_color="transparent")
        fila_busc.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        lbl = ctk.CTkLabel(fila_busc, text="Buscar Producto:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl.pack(side="left", padx=(0, 8))

        self.ent_busqueda = ctk.CTkEntry(fila_busc, placeholder_text="Codigo o nombre...", fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, width=220, height=36)
        self.ent_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_catalogo())

        btn_act = BotonSecundario(fila_busc, text="Actualizar", command=self.cargar_catalogo, width=90, height=36)
        btn_act.pack(side="right")

        cols = ("id", "codigo", "nombre", "categoria", "precio", "stock")
        encs = ("ID", "CODIGO", "DESCRIPCION", "CATEGORIA", "PRECIO", "STOCK")
        anchos = {"id": 35, "codigo": 85, "nombre": 160, "categoria": 100, "precio": 80, "stock": 60}

        self.tabla_catalogo = TablaEstilizada(panel_izq, cols, encs, anchos)
        self.tabla_catalogo.grid(row=2, column=0, sticky="nsew", padx=16, pady=6)

        fila_agregar = ctk.CTkFrame(panel_izq, fg_color="transparent")
        fila_agregar.grid(row=3, column=0, sticky="ew", padx=16, pady=(8, 14))

        lbl_cant = ctk.CTkLabel(fila_agregar, text="Cantidad:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_cant.pack(side="left", padx=(0, 8))

        self.ent_cantidad = ctk.CTkEntry(fila_agregar, width=70, height=36, fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, justify="center")
        self.ent_cantidad.insert(0, "1")
        self.ent_cantidad.pack(side="left", padx=(0, 14))

        btn_add = BotonPrimario(fila_agregar, text="+ Agregar al Carrito", command=self._agregar_al_carrito, width=160, height=36)
        btn_add.pack(side="left")

    def _crear_panel_carrito(self):
        panel_der = Tarjeta(self)
        panel_der.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        panel_der.grid_rowconfigure(2, weight=1)
        panel_der.grid_columnconfigure(0, weight=1)

        fila_cli = ctk.CTkFrame(panel_der, fg_color="transparent")
        fila_cli.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        lbl_cli = ctk.CTkLabel(fila_cli, text="Cliente:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_cli.pack(side="left", padx=(0, 8))

        self.combo_clientes = ctk.CTkComboBox(fila_cli, values=["1 - Consumidor Final"], fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, height=36)
        self.combo_clientes.pack(side="left", fill="x", expand=True)

        lbl_cart_tit = ctk.CTkLabel(panel_der, text="Detalle de Venta", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_cart_tit.grid(row=1, column=0, sticky="w", padx=16, pady=(4, 6))

        cols = ("idx", "nombre", "precio", "cant", "subtotal")
        encs = ("#", "PRODUCTO", "P.UNIT", "CANT", "SUBTOTAL")
        anchos = {"idx": 30, "nombre": 130, "precio": 70, "cant": 50, "subtotal": 80}

        self.tabla_carrito = TablaEstilizada(panel_der, cols, encs, anchos)
        self.tabla_carrito.grid(row=2, column=0, sticky="nsew", padx=16, pady=4)

        fila_quitar = ctk.CTkFrame(panel_der, fg_color="transparent")
        fila_quitar.grid(row=3, column=0, sticky="ew", padx=16, pady=(4, 8))

        btn_quitar = BotonPeligro(fila_quitar, text="Quitar Item", command=self._quitar_del_carrito, width=110, height=32)
        btn_quitar.pack(side="left")

        btn_vaciar = BotonSecundario(fila_quitar, text="Vaciar Carrito", command=self._vaciar_carrito, width=110, height=32)
        btn_vaciar.pack(side="right")

        tarjeta_totales = Tarjeta(panel_der, fg_color=BG_SECUNDARIO)
        tarjeta_totales.grid(row=4, column=0, sticky="ew", padx=16, pady=(6, 14))

        f_pago = ctk.CTkFrame(tarjeta_totales, fg_color="transparent")
        f_pago.pack(fill="x", padx=14, pady=(10, 4))
        f_pago.grid_columnconfigure(1, weight=1)

        lbl_mp = ctk.CTkLabel(f_pago, text="Metodo de Pago:", font=FUENTE_PEQUENA, text_color=TEXTO_SECUNDARIO)
        lbl_mp.grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.combo_pago = ctk.CTkComboBox(
            f_pago, values=["Efectivo", "Tarjeta de Debito", "Tarjeta de Credito", "Transferencia", "Cuenta Corriente"],
            fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, height=32
        )
        self.combo_pago.grid(row=0, column=1, sticky="ew")

        f_calc = ctk.CTkFrame(tarjeta_totales, fg_color="transparent")
        f_calc.pack(fill="x", padx=14, pady=4)

        f_sub = ctk.CTkFrame(f_calc, fg_color="transparent")
        f_sub.pack(fill="x", pady=2)
        ctk.CTkLabel(f_sub, text="Subtotal:", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.lbl_subtotal = ctk.CTkLabel(f_sub, text="$0.00", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_PRINCIPAL)
        self.lbl_subtotal.pack(side="right")

        f_desc = ctk.CTkFrame(f_calc, fg_color="transparent")
        f_desc.pack(fill="x", pady=2)
        ctk.CTkLabel(f_desc, text="Descuento ($):", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.ent_descuento = ctk.CTkEntry(f_desc, width=80, height=28, fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, justify="right")
        self.ent_descuento.insert(0, "0.00")
        self.ent_descuento.pack(side="right")
        self.ent_descuento.bind("<KeyRelease>", lambda e: self._actualizar_totales())

        f_tot = ctk.CTkFrame(f_calc, fg_color="transparent")
        f_tot.pack(fill="x", pady=(6, 2))
        ctk.CTkLabel(f_tot, text="TOTAL:", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO).pack(side="left")
        self.lbl_total = ctk.CTkLabel(f_tot, text="$0.00", font=("Segoe UI", 16, "bold"), text_color=ACENTO_ROJO)
        self.lbl_total.pack(side="right")

        self.btn_cobrar = BotonExito(tarjeta_totales, text="FINALIZAR VENTA Y EMITIR TICKET", command=self._procesar_venta_cobro, height=42)
        self.btn_cobrar.pack(fill="x", padx=14, pady=(8, 12))

    def cargar_catalogo(self):
        busq = self.ent_busqueda.get()
        productos = self.controlador_inv.obtener_productos(busqueda=busq)
        self.tabla_catalogo.limpiar()
        for p in productos:
            valores = (p.id, p.codigo, p.nombre, p.categoria, f"${p.precio_venta:.2f}", p.stock)
            self.tabla_catalogo.insertar_fila(valores)

    def cargar_clientes(self):
        clientes = self.controlador_cli.obtener_clientes()
        opciones = [f"{c.id} - {c.name if hasattr(c, 'name') else c.nombre} ({c.dni_cuit})" for c in clientes]
        self.combo_clientes.configure(values=opciones)
        if opciones:
            self.combo_clientes.set(opciones[0])

    def _agregar_al_carrito(self):
        fila = self.tabla_catalogo.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un producto del catalogo para agregar.", tipo="advertencia")
            return

        prod_id = fila[0]
        prod = self.controlador_inv.obtener_producto_por_id(prod_id)
        if not prod:
            return

        try:
            cant = int(self.ent_cantidad.get())
            if cant <= 0:
                raise ValueError()
        except ValueError:
            DialogoAlerta(self.winfo_toplevel(), "Error", "Ingrese una cantidad valida mayor a 0.", tipo="error")
            return

        cant_en_carrito = sum(item["cantidad"] for item in self.carrito if item["product_id"] == prod.id)
        if (cant_en_carrito + cant) > prod.stock:
            DialogoAlerta(self.winfo_toplevel(), "Stock Insuficiente", f"Stock disponible: {prod.stock}. Ya tiene {cant_en_carrito} en el carrito.", tipo="advertencia")
            return

        encontrado = False
        for item in self.carrito:
            if item["product_id"] == prod.id:
                item["cantidad"] += cant
                item["subtotal"] = round(item["cantidad"] * item["precio_unitario"], 2)
                encontrado = True
                break

        if not encontrado:
            self.carrito.append({
                "product_id": prod.id,
                "codigo": prod.codigo,
                "nombre_producto": prod.nombre,
                "precio_unitario": prod.precio_venta,
                "cantidad": cant,
                "subtotal": round(cant * prod.precio_venta, 2)
            })

        self.ent_cantidad.delete(0, tk.END)
        self.ent_cantidad.insert(0, "1")
        self._refrescar_tabla_carrito()

    def _quitar_del_carrito(self):
        fila = self.tabla_carrito.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un item del carrito para quitar.", tipo="advertencia")
            return
        idx = int(fila[0]) - 1
        if 0 <= idx < len(self.carrito):
            self.carrito.pop(idx)
            self._refrescar_tabla_carrito()

    def _vaciar_carrito(self):
        self.carrito.clear()
        self._refrescar_tabla_carrito()

    def _refrescar_tabla_carrito(self):
        self.tabla_carrito.limpiar()
        for i, item in enumerate(self.carrito, 1):
            valores = (i, item["nombre_producto"], f"${item['precio_unitario']:.2f}", item["cantidad"], f"${item['subtotal']:.2f}")
            self.tabla_carrito.insertar_fila(valores)
        self._actualizar_totales()

    def _actualizar_totales(self):
        subtotal = sum(item["subtotal"] for item in self.carrito)
        self.lbl_subtotal.configure(text=f"${subtotal:.2f}")

        try:
            desc = float(self.ent_descuento.get()) if self.ent_descuento.get() else 0.0
            if desc < 0:
                desc = 0.0
        except ValueError:
            desc = 0.0

        total = max(0.0, subtotal - desc)
        self.lbl_total.configure(text=f"${total:.2f}")

    def _procesar_venta_cobro(self):
        if not self.carrito:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "El carrito de ventas esta vacio.", tipo="advertencia")
            return

        cli_sel = self.combo_clientes.get()
        cli_id = 1
        if cli_sel:
            try:
                cli_id = int(cli_sel.split(" - ")[0])
            except Exception:
                cli_id = 1

        metodo_pago = self.combo_pago.get()

        try:
            desc = float(self.ent_descuento.get()) if self.ent_descuento.get() else 0.0
        except ValueError:
            DialogoAlerta(self.winfo_toplevel(), "Error", "El descuento ingresado es invalido.", tipo="error")
            return

        usr_id = self.usuario_actual.id

        try:
            venta, ticket_texto, ticket_archivo = self.controlador_ventas.procesar_venta(
                cliente_id=cli_id,
                usuario_id=usr_id,
                metodo_pago=metodo_pago,
                items_carrito=self.carrito,
                descuento=desc
            )

            self.carrito.clear()
            self._refrescar_tabla_carrito()
            self.cargar_catalogo()
            self.ent_descuento.delete(0, tk.END)
            self.ent_descuento.insert(0, "0.00")

            self._mostrar_modal_ticket(venta, ticket_texto, ticket_archivo)

        except Exception as e:
            DialogoAlerta(self.winfo_toplevel(), "Error al Procesar Venta", str(e), tipo="error")

    def _mostrar_modal_ticket(self, venta, ticket_texto, ticket_archivo):
        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title(f"Comprobante de Venta - {venta.numero_factura}")
        modal.geometry("480x620")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text="VENTA REGISTRADA CON EXITO", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 6))

        txt_ticket = ctk.CTkTextbox(modal, font=FUENTE_MONO, fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, border_width=1, corner_radius=8, width=420, height=440)
        txt_ticket.pack(padx=20, pady=10)
        txt_ticket.insert("1.0", ticket_texto)
        txt_ticket.configure(state="disabled")

        f_btn = ctk.CTkFrame(modal, fg_color="transparent")
        f_btn.pack(pady=(6, 16))

        lbl_guardado = ctk.CTkLabel(modal, text=f"Ticket guardado en: {ticket_archivo}", font=FUENTE_PEQUENA, text_color=TEXTO_MUTED)
        lbl_guardado.pack(pady=(0, 8))

        btn_cerrar = BotonPrimario(f_btn, text="Aceptar y Continuar", command=modal.destroy, width=180)
        btn_cerrar.pack()
