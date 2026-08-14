import customtkinter as ctk
import tkinter as tk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_INPUT, TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO, TEXTO_MUTED, ACENTO_ROJO, ACENTO_VERDE,
    BORDE_COLOR, FUENTE_TITULO, FUENTE_SUBTITULO,
    FUENTE_NORMAL, FUENTE_NORMAL_BOLD, FUENTE_PEQUENA
)
from views.componentes import (
    Tarjeta, BotonPrimario, BotonSecundario, BotonPeligro, BotonExito,
    CampoEntrada, TablaEstilizada, DialogoAlerta, DialogoConfirmar
)

class VistaCompras(ctk.CTkFrame):
    def __init__(self, master, controlador_compras, controlador_inventario, controlador_proveedores, usuario_actual):
        super().__init__(master, fg_color="transparent")
        self.controlador_compras = controlador_compras
        self.controlador_inv = controlador_inventario
        self.controlador_prov = controlador_proveedores
        self.usuario_actual = usuario_actual

        self.items_compra = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_interfaz()
        self.cargar_proveedores()
        self.cargar_productos_combo()
        self.cargar_historial_compras()

    def _crear_interfaz(self):
        panel_sup = ctk.CTkFrame(self, fg_color="transparent")
        panel_sup.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        lbl_tit = ctk.CTkLabel(panel_sup, text="Abastecimiento y Compras", font=FUENTE_TITULO, text_color=TEXTO_PRINCIPAL)
        lbl_tit.pack(side="left")

        lbl_sub = ctk.CTkLabel(panel_sup, text="Ingreso formal de mercaderia para incremento de stock y registro de costos", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO)
        lbl_sub.pack(side="left", padx=(16, 0), pady=(4, 0))

        contenedor_principal = ctk.CTkTabview(self, fg_color=BG_TARJETA, segmented_button_fg_color=BG_SECUNDARIO, segmented_button_selected_color=ACENTO_ROJO, segmented_button_selected_hover_color=ACENTO_ROJO, text_color="#ffffff")
        contenedor_principal.grid(row=1, column=0, sticky="nsew")

        tab_nueva = contenedor_principal.add("Nuevo Ingreso de Mercaderia")
        tab_historial = contenedor_principal.add("Historial de Compras")

        self._crear_tab_nueva_compra(tab_nueva)
        self._crear_tab_historial(tab_historial)

    def _crear_tab_nueva_compra(self, tab):
        tab.grid_rowconfigure(2, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        panel_cabecera = Tarjeta(tab, fg_color=BG_SECUNDARIO)
        panel_cabecera.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 10))

        fila1 = ctk.CTkFrame(panel_cabecera, fg_color="transparent")
        fila1.pack(fill="x", padx=14, pady=10)

        lbl_prov = ctk.CTkLabel(fila1, text="Proveedor:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_prov.pack(side="left", padx=(0, 8))

        self.combo_proveedor = ctk.CTkComboBox(fila1, values=[], fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, width=320, height=36)
        self.combo_proveedor.pack(side="left", padx=(0, 20))

        lbl_prod = ctk.CTkLabel(fila1, text="Producto:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_prod.pack(side="left", padx=(0, 8))

        self.combo_producto = ctk.CTkComboBox(fila1, values=[], command=self._al_seleccionar_producto, fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, width=280, height=36)
        self.combo_producto.pack(side="left")

        fila2 = ctk.CTkFrame(panel_cabecera, fg_color="transparent")
        fila2.pack(fill="x", padx=14, pady=(0, 10))

        lbl_costo = ctk.CTkLabel(fila2, text="Costo Unitario ($):", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_costo.pack(side="left", padx=(0, 8))

        self.ent_costo = ctk.CTkEntry(fila2, width=110, height=36, fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR)
        self.ent_costo.pack(side="left", padx=(0, 20))

        lbl_cant = ctk.CTkLabel(fila2, text="Cantidad:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_cant.pack(side="left", padx=(0, 8))

        self.ent_cant_compra = ctk.CTkEntry(fila2, width=90, height=36, fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR)
        self.ent_cant_compra.insert(0, "1")
        self.ent_cant_compra.pack(side="left", padx=(0, 20))

        btn_add = BotonPrimario(fila2, text="+ Agregar a la Orden", command=self._agregar_item_compra, width=170, height=36)
        btn_add.pack(side="left")

        cols = ("idx", "codigo", "nombre", "costo", "cant", "subtotal")
        encs = ("#", "CODIGO", "PRODUCTO", "COSTO UNITARIO", "CANTIDAD", "SUBTOTAL")
        anchos = {"idx": 30, "codigo": 90, "nombre": 220, "costo": 110, "cant": 80, "subtotal": 110}

        self.tabla_items = TablaEstilizada(tab, cols, encs, anchos)
        self.tabla_items.grid(row=2, column=0, sticky="nsew", padx=10, pady=6)

        panel_inferior = ctk.CTkFrame(tab, fg_color="transparent")
        panel_inferior.grid(row=3, column=0, sticky="ew", padx=10, pady=(8, 12))

        btn_quitar = BotonPeligro(panel_inferior, text="Quitar Seleccionado", command=self._quitar_item_compra, width=160, height=36)
        btn_quitar.pack(side="left")

        f_total = ctk.CTkFrame(panel_inferior, fg_color="transparent")
        f_total.pack(side="right")

        lbl_tot_tit = ctk.CTkLabel(f_total, text="TOTAL COMPRA:", font=FUENTE_SUBTITULO, text_color=TEXTO_SECUNDARIO)
        lbl_tot_tit.pack(side="left", padx=(0, 10))

        self.lbl_total_compra = ctk.CTkLabel(f_total, text="$0.00", font=("Segoe UI", 16, "bold"), text_color=ACENTO_ROJO)
        self.lbl_total_compra.pack(side="left", padx=(0, 20))

        btn_guardar = BotonExito(f_total, text="CONFIRMAR INGRESO DE STOCK", command=self._confirmar_guardar_compra, width=240, height=40)
        btn_guardar.pack(side="left")

    def _crear_tab_historial(self, tab):
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        fila_busc = ctk.CTkFrame(tab, fg_color="transparent")
        fila_busc.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 8))

        lbl = ctk.CTkLabel(fila_busc, text="Buscar Comprobante:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl.pack(side="left", padx=(0, 8))

        self.ent_busc_compra = ctk.CTkEntry(fila_busc, placeholder_text="N comprobante o proveedor...", fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, width=280, height=36)
        self.ent_busc_compra.pack(side="left", padx=(0, 12))
        self.ent_busc_compra.bind("<KeyRelease>", lambda e: self.cargar_historial_compras())

        btn_act = BotonSecundario(fila_busc, text="Actualizar", command=self.cargar_historial_compras, width=100, height=36)
        btn_act.pack(side="left")

        cols = ("id", "comprobante", "proveedor", "fecha", "total", "usuario")
        encs = ("ID", "N COMPROBANTE", "PROVEEDOR", "FECHA", "TOTAL", "REGISTRADO POR")
        anchos = {"id": 40, "comprobante": 130, "proveedor": 200, "fecha": 140, "total": 100, "usuario": 140}

        self.tabla_historial = TablaEstilizada(tab, cols, encs, anchos)
        self.tabla_historial.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)

        panel_pie = ctk.CTkFrame(tab, fg_color="transparent")
        panel_pie.grid(row=2, column=0, sticky="ew", padx=10, pady=(6, 12))

        btn_ver = BotonPrimario(panel_pie, text="Ver Detalle de Compra", command=self._ver_detalle_compra_modal, width=180, height=36)
        btn_ver.pack(side="left")

    def cargar_proveedores(self):
        proveedores = self.controlador_prov.obtener_proveedores()
        opciones = [f"{p.id} - {p.company_name if hasattr(p, 'company_name') else p.razon_social}" for p in proveedores]
        self.combo_proveedor.configure(values=opciones)
        if opciones:
            self.combo_proveedor.set(opciones[0])

    def cargar_productos_combo(self):
        productos = self.controlador_inv.obtener_productos()
        opciones = [f"{p.id} - {p.nombre} ({p.codigo})" for p in productos]
        self.combo_producto.configure(values=opciones)
        if opciones:
            self.combo_producto.set(opciones[0])
            self._al_seleccionar_producto(opciones[0])

    def _al_seleccionar_producto(self, seleccion):
        if seleccion:
            try:
                prod_id = int(seleccion.split(" - ")[0])
                prod = self.controlador_inv.obtener_producto_por_id(prod_id)
                if prod:
                    self.ent_costo.delete(0, tk.END)
                    self.ent_costo.insert(0, f"{prod.cost_price:.2f}")
            except Exception:
                pass

    def _agregar_item_compra(self):
        prod_sel = self.combo_producto.get()
        if not prod_sel:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Debe seleccionar un producto.", tipo="advertencia")
            return

        prod_id = int(prod_sel.split(" - ")[0])
        prod = self.controlador_inv.obtener_producto_por_id(prod_id)
        if not prod:
            return

        try:
            costo = float(self.ent_costo.get())
            cant = int(self.ent_cant_compra.get())
            if costo < 0 or cant <= 0:
                raise ValueError()
        except ValueError:
            DialogoAlerta(self.winfo_toplevel(), "Error", "Costo o cantidad ingresados invalidos.", tipo="error")
            return

        encontrado = False
        for item in self.items_compra:
            if item["producto_id"] == prod.id:
                item["cantidad"] += cant
                item["costo_unitario"] = costo
                item["subtotal"] = round(item["cantidad"] * costo, 2)
                encontrado = True
                break

        if not encontrado:
            self.items_compra.append({
                "producto_id": prod.id,
                "codigo_producto": prod.codigo,
                "nombre_producto": prod.nombre,
                "costo_unitario": costo,
                "cantidad": cant,
                "subtotal": round(costo * cant, 2)
            })

        self.ent_cant_compra.delete(0, tk.END)
        self.ent_cant_compra.insert(0, "1")
        self._refrescar_tabla_compra()

    def _quitar_item_compra(self):
        fila = self.tabla_items.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione un producto para quitar de la lista.", tipo="advertencia")
            return
        idx = int(fila[0]) - 1
        if 0 <= idx < len(self.items_compra):
            self.items_compra.pop(idx)
            self._refrescar_tabla_compra()

    def _refrescar_tabla_compra(self):
        self.tabla_items.limpiar()
        total = 0.0
        for i, item in enumerate(self.items_compra, 1):
            subtot = item["subtotal"]
            total += subtot
            valores = (i, item["codigo_producto"], item["nombre_producto"], f"${item['costo_unitario']:.2f}", item["cantidad"], f"${subtot:.2f}")
            self.tabla_items.insertar_fila(valores)

        self.lbl_total_compra.configure(text=f"${total:.2f}")

    def _confirmar_guardar_compra(self):
        if not self.items_compra:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "No hay productos agregados a la orden de compra.", tipo="advertencia")
            return

        prov_sel = self.combo_proveedor.get()
        if not prov_sel:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Debe seleccionar un proveedor.", tipo="advertencia")
            return

        prov_id = int(prov_sel.split(" - ")[0])
        usr_id = self.usuario_actual.id

        try:
            compra_id = self.controlador_compras.registrar_compra(prov_id, usr_id, self.items_compra)
            self.items_compra.clear()
            self._refrescar_tabla_compra()
            self.cargar_historial_compras()
            DialogoAlerta(self.winfo_toplevel(), "Exito", "Mercaderia ingresada y stock actualizado correctamente.", tipo="exito")
        except Exception as e:
            DialogoAlerta(self.winfo_toplevel(), "Error", str(e), tipo="error")

    def cargar_historial_compras(self):
        busq = self.ent_busc_compra.get()
        compras = self.controlador_compras.obtener_compras(busqueda=busq)
        self.tabla_historial.limpiar()
        for c in compras:
            rz = c.razon_social_proveedor if hasattr(c, "razon_social_proveedor") else ""
            usr = c.nombre_usuario if hasattr(c, "nombre_usuario") else ""
            valores = (c.id, c.numero_comprobante, rz, c.fecha, f"${c.total:.2f}", usr)
            self.tabla_historial.insertar_fila(valores)

    def _ver_detalle_compra_modal(self):
        fila = self.tabla_historial.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione una compra para ver su detalle.", tipo="advertencia")
            return

        compra_id = fila[0]
        compra = self.controlador_compras.obtener_compra_por_id(compra_id)
        if not compra:
            return

        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title(f"Detalle de Compra - {compra.numero_comprobante}")
        modal.geometry("620x460")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text=f"Comprobante: {compra.numero_comprobante}", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 4))

        lbl_info = ctk.CTkLabel(modal, text=f"Proveedor: {compra.razon_social_proveedor} | Fecha: {compra.fecha}", font=FUENTE_NORMAL, text_color=TEXTO_SECUNDARIO)
        lbl_info.pack(pady=(0, 10))

        cols = ("codigo", "nombre", "costo", "cant", "subtotal")
        encs = ("CODIGO", "PRODUCTO", "COSTO UNIT.", "CANTIDAD", "SUBTOTAL")
        anchos = {"codigo": 90, "nombre": 200, "costo": 100, "cant": 70, "subtotal": 100}

        tabla_det = TablaEstilizada(modal, cols, encs, anchos)
        tabla_det.pack(fill="both", expand=True, padx=20, pady=10)

        for item in compra.items:
            tabla_det.insertar_fila((item.codigo_producto, item.nombre_producto, f"${item.costo_unitario:.2f}", item.cantidad, f"${item.subtotal:.2f}"))

        lbl_tot = ctk.CTkLabel(modal, text=f"Total: ${compra.total:.2f}", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tot.pack(pady=(4, 6))

        btn_cerrar = BotonSecundario(modal, text="Cerrar", command=modal.destroy, width=120)
        btn_cerrar.pack(pady=(0, 14))
