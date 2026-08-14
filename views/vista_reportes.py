import customtkinter as ctk
import tkinter as tk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_INPUT, TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO, TEXTO_MUTED, ACENTO_ROJO, ACENTO_VERDE,
    ACENTO_AMARILLO, BORDE_COLOR, FUENTE_TITULO, FUENTE_SUBTITULO,
    FUENTE_NORMAL, FUENTE_NORMAL_BOLD, FUENTE_PEQUENA, FUENTE_MONO
)
from views.componentes import (
    Tarjeta, TarjetaEstadistica, BotonPrimario, BotonSecundario,
    CampoEntrada, TablaEstilizada, DialogoAlerta
)
from utils.generador_ticket import GeneradorTicket

class VistaReportes(ctk.CTkFrame):
    def __init__(self, master, controlador_reportes, controlador_ventas, controlador_clientes, controlador_auth):
        super().__init__(master, fg_color="transparent")
        self.controlador_rep = controlador_reportes
        self.controlador_vta = controlador_ventas
        self.controlador_cli = controlador_clientes
        self.controlador_auth = controlador_auth

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_tarjetas_kpi()
        self._crear_filtros()
        self._crear_tabla_historial()
        self.actualizar_reportes()

    def _crear_tarjetas_kpi(self):
        contenedor_kpi = ctk.CTkFrame(self, fg_color="transparent")
        contenedor_kpi.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        contenedor_kpi.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.kpi_ventas = TarjetaEstadistica(contenedor_kpi, titulo="Total Recaudado", valor="$0.00", subtitulo="Ventas acumuladas", color_acento=ACENTO_ROJO)
        self.kpi_ventas.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.kpi_ganancia = TarjetaEstadistica(contenedor_kpi, titulo="Ganancia Bruta", valor="$0.00", subtitulo="Margen total", color_acento=ACENTO_ROJO)
        self.kpi_ganancia.grid(row=0, column=1, sticky="ew", padx=8)

        self.kpi_transacciones = TarjetaEstadistica(contenedor_kpi, titulo="Comprobantes", valor="0", subtitulo="Operaciones emitidas", color_acento=TEXTO_SECUNDARIO)
        self.kpi_transacciones.grid(row=0, column=2, sticky="ew", padx=8)

        self.kpi_alertas = TarjetaEstadistica(contenedor_kpi, titulo="Stock Critico", valor="0", subtitulo="Productos con alerta", color_acento=ACENTO_AMARILLO)
        self.kpi_alertas.grid(row=0, column=3, sticky="ew", padx=(8, 0))

    def _crear_filtros(self):
        panel_filtros = Tarjeta(self)
        panel_filtros.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        fila = ctk.CTkFrame(panel_filtros, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=12)

        lbl = ctk.CTkLabel(fila, text="Buscar:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl.pack(side="left", padx=(0, 8))

        self.ent_busqueda = ctk.CTkEntry(fila, placeholder_text="N factura, cliente o vendedor...", fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, width=240, height=36)
        self.ent_busqueda.pack(side="left", padx=(0, 16))
        self.ent_busqueda.bind("<KeyRelease>", lambda e: self.cargar_historial())

        lbl_mp = ctk.CTkLabel(fila, text="Forma de Pago:", font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO)
        lbl_mp.pack(side="left", padx=(0, 8))

        self.combo_mp = ctk.CTkComboBox(
            fila, values=["Todos", "Efectivo", "Tarjeta de Debito", "Tarjeta de Credito", "Transferencia", "Cuenta Corriente"],
            command=lambda v: self.cargar_historial(), fg_color=BG_INPUT, border_color=BORDE_COLOR, button_color=BG_TARJETA, text_color=TEXTO_PRINCIPAL, width=170, height=36
        )
        self.combo_mp.pack(side="left", padx=(0, 16))

        btn_act = BotonSecundario(fila, text="Actualizar", command=self.actualizar_reportes, width=100, height=36)
        btn_act.pack(side="right")

    def _crear_tabla_historial(self):
        columnas = ("id", "factura", "fecha", "cliente", "pago", "subtotal", "descuento", "total", "vendedor")
        encabezados = ("ID", "N FACTURA", "FECHA / HORA", "CLIENTE", "PAGO", "SUBTOTAL", "DESC.", "TOTAL", "VENDEDOR")
        anchos = {"id": 35, "factura": 115, "fecha": 135, "cliente": 160, "pago": 110, "subtotal": 80, "descuento": 65, "total": 85, "vendedor": 130}

        contenedor_tabla = ctk.CTkFrame(self, fg_color="transparent")
        contenedor_tabla.grid(row=2, column=0, sticky="nsew")
        contenedor_tabla.grid_rowconfigure(0, weight=1)
        contenedor_tabla.grid_columnconfigure(0, weight=1)

        self.tabla = TablaEstilizada(contenedor_tabla, columnas, encabezados, anchos)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        panel_acciones = ctk.CTkFrame(contenedor_tabla, fg_color="transparent")
        panel_acciones.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        btn_ticket = BotonPrimario(panel_acciones, text="Ver / Reimprimir Ticket", command=self._reimprimir_ticket, width=190)
        btn_ticket.pack(side="left", padx=(0, 10))

    def actualizar_reportes(self):
        resumen = self.controlador_rep.obtener_resumen_dashboard()
        self.kpi_ventas.actualizar(f"${resumen['total_ventas']:,.2f}")
        self.kpi_ganancia.actualizar(f"${resumen['ganancia_estimada']:,.2f}")
        self.kpi_transacciones.actualizar(str(resumen["cantidad_ventas"]))
        self.kpi_alertas.actualizar(str(resumen["productos_stock_bajo"]))
        self.cargar_historial()

    def cargar_historial(self):
        busq = self.ent_busqueda.get()
        mp = self.combo_mp.get()
        ventas = self.controlador_rep.obtener_historial_ventas(busqueda=busq, metodo_pago=mp)

        self.tabla.limpiar()
        for v in ventas:
            cli = v.nombre_cliente if v.nombre_cliente else "Consumidor Final"
            usr = v.nombre_usuario if v.nombre_usuario else "Vendedor"
            valores = (
                v.id, v.numero_factura, v.fecha, cli, v.metodo_pago,
                f"${v.subtotal:.2f}", f"${v.descuento:.2f}", f"${v.total:.2f}", usr
            )
            self.tabla.insertar_fila(valores)

    def _reimprimir_ticket(self):
        fila = self.tabla.obtener_seleccionado()
        if not fila:
            DialogoAlerta(self.winfo_toplevel(), "Atencion", "Seleccione una venta para visualizar o reimprimir su comprobante.", tipo="advertencia")
            return

        venta_id = fila[0]
        venta = self.controlador_vta.obtener_venta_por_id(venta_id)
        if not venta:
            return

        cliente = self.controlador_cli.obtener_cliente_por_id(venta.cliente_id) if venta.cliente_id else None

        texto_ticket = GeneradorTicket.generar_texto_ticket(
            venta=venta,
            cliente=cliente,
            usuario=type("UsuarioTemp", (), {"nombre_completo": venta.nombre_usuario})(),
            items=venta.items
        )

        modal = ctk.CTkToplevel(self.winfo_toplevel())
        modal.title(f"Reimpresion de Comprobante - {venta.numero_factura}")
        modal.geometry("480x600")
        modal.resizable(False, False)
        modal.configure(fg_color=BG_SECUNDARIO)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        lbl_tit = ctk.CTkLabel(modal, text=f"Comprobante: {venta.numero_factura}", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_tit.pack(pady=(16, 6))

        txt_ticket = ctk.CTkTextbox(modal, font=FUENTE_MONO, fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, border_color=BORDE_COLOR, border_width=1, corner_radius=8, width=420, height=440)
        txt_ticket.pack(padx=20, pady=10)
        txt_ticket.insert("1.0", texto_ticket)
        txt_ticket.configure(state="disabled")

        def guardar():
            archivo = GeneradorTicket.guardar_ticket_archivo(texto_ticket, venta.numero_factura)
            DialogoAlerta(modal, "Ticket Exportado", f"Ticket guardado exitosamente en:\n{archivo}", tipo="exito")

        f_btn = ctk.CTkFrame(modal, fg_color="transparent")
        f_btn.pack(pady=(6, 16))

        btn_exp = BotonPrimario(f_btn, text="Exportar / Guardar TXT", command=guardar, width=170)
        btn_exp.pack(side="left", padx=8)

        btn_cerrar = BotonSecundario(f_btn, text="Cerrar", command=modal.destroy, width=110)
        btn_cerrar.pack(side="left", padx=8)
