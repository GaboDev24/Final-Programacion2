import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from views.tema import (
    BG_PRINCIPAL, BG_SECUNDARIO, BG_TARJETA, BG_TARJETA_HOVER, BG_INPUT,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, TEXTO_MUTED,
    ACENTO_ROJO, ACENTO_ROJO_HOVER, ACENTO_VERDE, ACENTO_AMARILLO,
    BORDE_COLOR, FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_NORMAL_BOLD, FUENTE_PEQUENA, FUENTE_MONO
)

class Tarjeta(ctk.CTkFrame):
    def __init__(self, master, fg_color=BG_TARJETA, border_color=BORDE_COLOR, border_width=1, corner_radius=12, **kwargs):
        super().__init__(master, fg_color=fg_color, border_color=border_color, border_width=border_width, corner_radius=corner_radius, **kwargs)

class TarjetaEstadistica(Tarjeta):
    def __init__(self, master, titulo, valor, subtitulo="", color_acento=ACENTO_ROJO, icono="", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        fila_sup = ctk.CTkFrame(self, fg_color="transparent")
        fila_sup.pack(fill="x", padx=16, pady=(14, 4))

        lbl_tit = ctk.CTkLabel(fila_sup, text=titulo.upper(), font=FUENTE_PEQUENA, text_color=TEXTO_MUTED)
        lbl_tit.pack(side="left")

        if icono:
            lbl_ico = ctk.CTkLabel(fila_sup, text=icono, font=("Segoe UI", 12, "bold"), text_color=color_acento)
            lbl_ico.pack(side="right")

        self.lbl_val = ctk.CTkLabel(self, text=str(valor), font=("Segoe UI", 22, "bold"), text_color=TEXTO_PRINCIPAL, anchor="w")
        self.lbl_val.pack(fill="x", padx=16, pady=(0, 4))

        if subtitulo:
            lbl_sub = ctk.CTkLabel(self, text=subtitulo, font=FUENTE_PEQUENA, text_color=color_acento, anchor="w")
            lbl_sub.pack(fill="x", padx=16, pady=(0, 12))
        else:
            ctk.CTkLabel(self, text="", height=4).pack()

    def actualizar(self, nuevo_valor):
        self.lbl_val.configure(text=str(nuevo_valor))

class BotonPrimario(ctk.CTkButton):
    def __init__(self, master, text, command=None, width=140, height=38, **kwargs):
        super().__init__(
            master, text=text, command=command, width=width, height=height,
            fg_color=ACENTO_ROJO, text_color="#ffffff", hover_color=ACENTO_ROJO_HOVER,
            font=FUENTE_NORMAL_BOLD, corner_radius=8, **kwargs
        )

class BotonSecundario(ctk.CTkButton):
    def __init__(self, master, text, command=None, width=140, height=38, **kwargs):
        super().__init__(
            master, text=text, command=command, width=width, height=height,
            fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, hover_color=BG_TARJETA_HOVER,
            border_color=BORDE_COLOR, border_width=1,
            font=FUENTE_NORMAL, corner_radius=8, **kwargs
        )

class BotonPeligro(ctk.CTkButton):
    def __init__(self, master, text, command=None, width=140, height=38, **kwargs):
        super().__init__(
            master, text=text, command=command, width=width, height=height,
            fg_color="#991b1b", text_color="#ffffff", hover_color=ACENTO_ROJO,
            font=FUENTE_NORMAL_BOLD, corner_radius=8, **kwargs
        )

class BotonExito(ctk.CTkButton):
    def __init__(self, master, text, command=None, width=140, height=38, **kwargs):
        super().__init__(
            master, text=text, command=command, width=width, height=height,
            fg_color=ACENTO_ROJO, text_color="#ffffff", hover_color=ACENTO_ROJO_HOVER,
            font=FUENTE_NORMAL_BOLD, corner_radius=8, **kwargs
        )

class CampoEntrada(ctk.CTkFrame):
    def __init__(self, master, etiqueta, placeholder="", es_password=False, valor_inicial="", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        lbl = ctk.CTkLabel(self, text=etiqueta, font=FUENTE_NORMAL_BOLD, text_color=TEXTO_SECUNDARIO, anchor="w")
        lbl.pack(fill="x", pady=(0, 4))

        self.entrada = ctk.CTkEntry(
            self, placeholder_text=placeholder, show="*" if es_password else "",
            fg_color=BG_INPUT, text_color=TEXTO_PRINCIPAL, placeholder_text_color=TEXTO_MUTED,
            border_color=BORDE_COLOR, border_width=1, corner_radius=8, height=38,
            font=FUENTE_NORMAL
        )
        if valor_inicial:
            self.entrada.insert(0, str(valor_inicial))
        self.entrada.pack(fill="x")

    def obtener(self):
        return self.entrada.get()

    def establecer(self, valor):
        self.entrada.delete(0, tk.END)
        if valor is not None:
            self.entrada.insert(0, str(valor))

    def limpiar(self):
        self.entrada.delete(0, tk.END)

class TablaEstilizada(ctk.CTkFrame):
    def __init__(self, master, columnas, encabezados, anchos=None, **kwargs):
        super().__init__(master, fg_color=BG_TARJETA, border_color=BORDE_COLOR, border_width=1, corner_radius=10, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Custom.Treeview",
            background=BG_TARJETA,
            foreground=TEXTO_PRINCIPAL,
            fieldbackground=BG_TARJETA,
            bordercolor=BORDE_COLOR,
            borderwidth=0,
            rowheight=32,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "Custom.Treeview.Heading",
            background=BG_SECUNDARIO,
            foreground=TEXTO_SECUNDARIO,
            relief="flat",
            borderwidth=1,
            bordercolor=BORDE_COLOR,
            font=("Segoe UI", 10, "bold")
        )
        estilo.map(
            "Custom.Treeview",
            background=[("selected", "#381216")],
            foreground=[("selected", "#ff6b6b")]
        )
        estilo.map(
            "Custom.Treeview.Heading",
            background=[("active", BG_TARJETA_HOVER)]
        )

        self.arbol = ttk.Treeview(self, columns=columnas, show="headings", style="Custom.Treeview", selectmode="browse")

        for col, enc in zip(columnas, encabezados):
            self.arbol.heading(col, text=enc)
            ancho = 120
            if anchos and col in anchos:
                ancho = anchos[col]
            self.arbol.column(col, width=ancho, anchor="center")

        scroll_y = ctk.CTkScrollbar(self, orientation="vertical", command=self.arbol.yview, fg_color=BG_TARJETA, button_color=BG_INPUT, button_hover_color=BORDE_COLOR)
        self.arbol.configure(yscrollcommand=scroll_y.set)

        self.arbol.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=2)
        scroll_y.grid(row=0, column=1, sticky="ns", padx=(0, 2), pady=2)

    def limpiar(self):
        for item in self.arbol.get_children():
            self.arbol.delete(item)

    def insertar_fila(self, valores, tags=()):
        return self.arbol.insert("", "end", values=valores, tags=tags)

    def obtener_seleccionado(self):
        seleccion = self.arbol.selection()
        if seleccion:
            return self.arbol.item(seleccion[0])["values"]
        return None

class DialogoAlerta(ctk.CTkToplevel):
    def __init__(self, master, titulo, mensaje, tipo="info"):
        super().__init__(master)
        self.title(titulo)
        self.geometry("420x220")
        self.resizable(False, False)
        self.configure(fg_color=BG_SECUNDARIO)
        self.transient(master)
        self.grab_set()

        colores = {
            "exito": (ACENTO_ROJO, "EXITO"),
            "error": (ACENTO_ROJO, "ERROR"),
            "advertencia": (ACENTO_AMARILLO, "ADVERTENCIA"),
            "info": (ACENTO_ROJO, "INFORMACION")
        }
        color, cabecera = colores.get(tipo, (ACENTO_ROJO, "INFORMACION"))

        self.grid_columnconfigure(0, weight=1)

        barra = ctk.CTkFrame(self, fg_color=color, height=4, corner_radius=0)
        barra.pack(fill="x")

        lbl_cab = ctk.CTkLabel(self, text=cabecera, font=FUENTE_SUBTITULO, text_color=color)
        lbl_cab.pack(pady=(16, 6))

        lbl_msg = ctk.CTkLabel(self, text=mensaje, font=FUENTE_NORMAL, text_color=TEXTO_PRINCIPAL, wraplength=360, justify="center")
        lbl_msg.pack(pady=8, padx=20)

        btn = BotonPrimario(self, text="Aceptar", command=self.destroy, width=120)
        btn.pack(pady=(12, 16))

        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (420 // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (220 // 2)
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

class DialogoConfirmar(ctk.CTkToplevel):
    def __init__(self, master, titulo, mensaje, callback_confirmar):
        super().__init__(master)
        self.title(titulo)
        self.geometry("420x220")
        self.resizable(False, False)
        self.configure(fg_color=BG_SECUNDARIO)
        self.transient(master)
        self.grab_set()
        self.callback_confirmar = callback_confirmar

        self.grid_columnconfigure(0, weight=1)

        barra = ctk.CTkFrame(self, fg_color=ACENTO_ROJO, height=4, corner_radius=0)
        barra.pack(fill="x")

        lbl_cab = ctk.CTkLabel(self, text="CONFIRMAR ACCION", font=FUENTE_SUBTITULO, text_color=ACENTO_ROJO)
        lbl_cab.pack(pady=(16, 6))

        lbl_msg = ctk.CTkLabel(self, text=mensaje, font=FUENTE_NORMAL, text_color=TEXTO_PRINCIPAL, wraplength=360, justify="center")
        lbl_msg.pack(pady=8, padx=20)

        fila_btn = ctk.CTkFrame(self, fg_color="transparent")
        fila_btn.pack(pady=(12, 16))

        btn_cancel = BotonSecundario(fila_btn, text="Cancelar", command=self.destroy, width=110)
        btn_cancel.pack(side="left", padx=8)

        btn_ok = BotonPeligro(fila_btn, text="Confirmar", command=self._confirmar, width=110)
        btn_ok.pack(side="left", padx=8)

        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (420 // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (220 // 2)
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    def _confirmar(self):
        self.destroy()
        if self.callback_confirmar:
            self.callback_confirmar()
