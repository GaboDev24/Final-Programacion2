h# Instituto Nuevo Cuyo (INCUYO)
## Práctica Profesional 2 / Programación 2 — Examen Final
### Sistema de Gestión de Ventas y Control de Stock (TPV)

**Estudiante:** Gabriel Reina — 2do año  
**Institución:** Instituto Nuevo Cuyo (INCUYO)  
**Tecnologías:** Python 3, CustomTkinter, SQLite3, hashlib  
**Patrón de Diseño:** Modelo-Vista-Controlador (MVC)  

---

## 1. Descripción General del Proyecto

El presente proyecto consiste en el diseño, desarrollo e implementación de una aplicación de escritorio profesional orientada a la automatización integral de procesos comerciales, gestión de compras, facturación en tiempo real y control riguroso de inventario.

La aplicación ha sido construida bajo el paradigma de **Programación Orientada a Objetos (POO)** y la arquitectura de software **Modelo-Vista-Controlador (MVC)**, garantizando una alta modularidad, escalabilidad, robustez frente a errores y una interfaz gráfica moderna y responsiva.

---

## 2. Requisitos Técnicos Cumplidos

### 2.1 Requisitos Base (Obligatorios)
- **Arquitectura POO:** Clases y entidades modeladas de forma modular y desacoplada.
- **Persistencia en Base de Datos Relacional:** Base de datos SQLite (`sistema_ventas.db`) con soporte para claves foráneas (`PRAGMA foreign_keys = ON;`), transacciones atómicas (`BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`) y relaciones de integridad referencial.
- **Interfaz Gráfica de Usuario (GUI):** Desarrollada con CustomTkinter con colores personalizados, libre de errores visuales y con componentes reutilizables.
- **Módulo de Inventario (CRUD):**
  - Altas, bajas, modificaciones y búsquedas en tiempo real de artículos.
  - Control de existencias (Stock), alertas automáticas de stock crítico/mínimo y cálculo de margen de ganancia.
- **Módulo de Facturación y Ventas:**
  - Terminal de Punto de Venta (TPV) con procesamiento de pedidos en tiempo real.
  - Carrito de compras dinámico con verificación de stock disponible en línea.
  - Descuento automático de existencias tras cada operación exitosa.
  - Emisión de comprobantes: visualización de ticket térmico y exportación automática a archivo `.txt` en el directorio `tickets/`.

### 2.2 Módulos y Características Opcionales Incorporadas
- **Patrón Modelo-Vista-Controlador (MVC):** Separación estricta entre capas de persistencia (`database`), entidades de dominio (`models`), lógica de negocio (`controllers`), validadores/utilidades (`utils`) e interfaz gráfica (`views`).
- **Módulo de Gestión de Clientes (CRUD):** Registro de clientes (DNI/CUIT, nombre, contacto, dirección) y visualización del historial de compras previas.
- **Módulo de Proveedores (CRUD):** Padrón de distribuidores y empresas mayoristas con asociación directa al catálogo de productos.
- **Módulo de Abastecimiento (Compras):** Registro formal de ingresos de mercadería, actualización de precios de costo e incremento automático de stock.
- **Control de Acceso y Roles (Login):**
  - Sistema de autenticación con contraseñas encriptadas mediante algoritmo criptográfico SHA-256.
  - Roles definidos: **Administrador** (control total de la plataforma) y **Vendedor** (acceso operativo a TPV, inventario y clientes).
- **Validación y Robustez:**
  - Verificación estricta de tipos de datos en capa de controladores y utilidades (prevención de textos en precios/cantidades, campos obligatorios, formatos de identificación).
  - Manejo integral de excepciones para impedir cierres inesperados de la aplicación.

---

## 3. Estructura del Proyecto

```
FINAL Programacion 2/
├── database/
│   └── gestor_bd.py                # Inicializacion de SQLite, tablas y datos semilla
├── models/
│   ├── usuario.py                  # Entidad de Usuario y roles
│   ├── producto.py                 # Entidad de Producto, precios y stock
│   ├── cliente.py                  # Entidad de Cliente
│   ├── proveedor.py                # Entidad de Proveedor
│   ├── venta.py                    # Entidades Venta y DetalleVenta
│   └── compra.py                   # Entidades Compra y DetalleCompra
├── controllers/
│   ├── controlador_autenticacion.py# Logica de inicio y cierre de sesion
│   ├── controlador_inventario.py   # CRUD y consultas de articulos
│   ├── controlador_ventas.py       # Procesamiento transaccional de ventas y stock
│   ├── controlador_clientes.py     # CRUD de clientes e historial
│   ├── controlador_proveedores.py  # CRUD de proveedores
│   ├── controlador_compras.py      # Registro de compras e incremento de stock
│   ├── controlador_reportes.py     # Metricas financieras, resumen y caja
│   └── controlador_usuarios.py     # Gestion de usuarios del sistema
├── utils/
│   ├── validadores.py              # Validaciones de tipos y consistencia
│   └── generador_ticket.py         # Formateo y guardado de tickets termicos
├── views/
│   ├── tema.py                     # Tokens de diseno, paleta roja y fuentes
│   ├── componentes.py              # Widgets personalizados (tablas, botones, tarjetas)
│   ├── vista_login.py              # Pantalla de acceso
│   ├── vista_principal.py          # Dashboard contenedor con navegacion lateral
│   ├── vista_ventas.py             # Terminal de punto de venta (TPV)
│   ├── vista_inventario.py         # Gestion de productos y categorias
│   ├── vista_clientes.py           # Gestion de clientes
│   ├── vista_proveedores.py        # Gestion de distribuidores
│   ├── vista_compras.py            # Modulo de abastecimiento
│   ├── vista_reportes.py           # Metricas y reimpresion de comprobantes
│   ├── vista_usuarios.py           # Administracion de cuentas y roles
│   └── main.py                     # Punto de entrada alternativo desde subdirectorio
├── tickets/                        # Directorio autogenerado con comprobantes emitidos
├── DESIGN.md                       # Especificacion del sistema de diseno
├── README.md                       # Documentacion tecnica para defensa de examen
└── main.py                         # Punto de entrada principal de la aplicacion
```

---

## 4. Guía de Instalación y Ejecución

### 4.1 Requisitos Previos
- Python 3.10 o superior instalado.
- Biblioteca `customtkinter`.

### 4.2 Instalación de Dependencias
Ejecutar en la terminal:
```bash
pip install customtkinter
```

### 4.3 Ejecución de la Aplicación
Iniciar la aplicación desde la raíz del proyecto:
```bash
python main.py
```
O de forma alternativa:
```bash
python views/main.py
```

---

## 5. Credenciales de Acceso Iniciales (Seed Data)

El sistema inicializa automáticamente la base de datos con los siguientes usuarios de demostración:

| Rol | Usuario | Contraseña | Permisos |
|---|---|---|---|
| Administrador | `admin` | `admin123` | Acceso irrestricto: TPV, Inventario, Clientes, Proveedores, Compras, Reportes, Usuarios. |
| Vendedor | `vendedor` | `1234` | Acceso operativo: TPV, Consulta de Inventario y Clientes. |

---

## 6. Flujo Operativo y Defensa de la Lógica

### 6.1 Flujo de Venta Exitosa (Demostración Paso a Paso)
1. El usuario se autentica en la pantalla de Login con sus credenciales.
2. Ingresa a la sección **Punto de Venta (TPV)**.
3. Utiliza la barra de búsqueda en tiempo real para localizar el producto por código o descripción.
4. Indica la cantidad deseada y presiona `+ Agregar al Carrito`. El sistema valida que la cantidad no sea menor o igual a cero y que no supere el stock físico disponible en la base de datos.
5. Selecciona el cliente receptor (por defecto `Consumidor Final` o un cliente registrado).
6. Selecciona el método de pago (Efectivo, Débito, Crédito, Transferencia, Cuenta Corriente) y opcionalmente un monto de descuento.
7. Presiona `FINALIZAR VENTA Y EMITIR TICKET`:
   - El controlador inicia una transacción SQLite (`BEGIN TRANSACTION`).
   - Se genera el número correlativo de comprobante (`VTA-AAAA-XXXXX`).
   - Se crea el registro de la venta en la tabla `ventas`.
   - Se inserta cada línea en `detalle_ventas`.
   - Se descuenta atómicamente el stock en la tabla `productos`.
   - Se ejecuta el `COMMIT` de la transacción.
   - El generador de tickets formatea el comprobante de impresión y lo almacena físicamente en `tickets/ticket_VTA-AAAA-XXXXX.txt`.
   - Se abre el modal con la vista previa del ticket térmico para entrega al comprador.

### 6.2 Flujo de Abastecimiento (Compras)
1. El administrador ingresa a **Abastecimiento**.
2. Selecciona un proveedor y el producto a ingresar.
3. Especifica el costo unitario de adquisición y las unidades recibidas.
4. Presiona `CONFIRMAR INGRESO DE STOCK`:
   - Se registra la orden en `compras` y `detalle_compras`.
   - Se incrementa el stock del artículo y se actualiza su precio de costo para recalcular márgenes.

### 6.3 Consulta de Reportes y Reimpresión
1. En la sección **Reportes y Caja**, el administrador visualiza métricas consolidadas: total facturado, ganancia bruta estimada, cantidad de comprobantes y alertas de artículos con stock bajo.
2. Puede filtrar por número de factura o medio de pago, y seleccionar cualquier venta previa para visualizar o exportar nuevamente el ticket en archivo de texto.

---

## 7. Información Institucional

- **Institución:** Instituto Nuevo Cuyo (INCUYO)
- **Materia:** Práctica Profesional 2 / Programación 2
- **Alumno:** Gabriel Reina (2do año)
- **Año Académico:** 2026
