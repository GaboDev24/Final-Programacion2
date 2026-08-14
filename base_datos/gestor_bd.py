import sqlite3
import hashlib

class GestorBD:
    def __init__(self, ruta_bd="sistema_ventas.db"):
        self.ruta_bd = ruta_bd
        self.inicializar_bd()

    def obtener_conexion(self):
        conexion = sqlite3.connect(self.ruta_bd)
        conexion.row_factory = sqlite3.Row
        return conexion

    def inicializar_bd(self):
        conexion = self.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                clave_hash TEXT NOT NULL,
                nombre_completo TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('Administrador', 'Vendedor')),
                activo INTEGER DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cuit TEXT UNIQUE NOT NULL,
                razon_social TEXT NOT NULL,
                contacto TEXT,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni_cuit TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio_costo REAL NOT NULL DEFAULT 0.0,
                precio_venta REAL NOT NULL DEFAULT 0.0,
                stock INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER NOT NULL DEFAULT 5,
                proveedor_id INTEGER,
                activo INTEGER DEFAULT 1,
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                cliente_id INTEGER,
                usuario_id INTEGER NOT NULL,
                metodo_pago TEXT NOT NULL,
                subtotal REAL NOT NULL,
                descuento REAL DEFAULT 0.0,
                total REAL NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                codigo_producto TEXT NOT NULL,
                nombre_producto TEXT NOT NULL,
                precio_unitario REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_comprobante TEXT UNIQUE NOT NULL,
                proveedor_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                total REAL NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                costo_unitario REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        self._poblar_datos_iniciales(cursor)
        conexion.commit()
        conexion.close()

    def _poblar_datos_iniciales(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            clave_admin = hashlib.sha256("admin123".encode()).hexdigest()
            clave_vendedor = hashlib.sha256("1234".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (nombre_usuario, clave_hash, nombre_completo, rol)
                VALUES (?, ?, ?, ?)
            """, ("admin", clave_admin, "Gabriel Reina - Administrador", "Administrador"))
            cursor.execute("""
                INSERT INTO usuarios (nombre_usuario, clave_hash, nombre_completo, rol)
                VALUES (?, ?, ?, ?)
            """, ("vendedor", clave_vendedor, "Juan Pérez", "Vendedor"))

        cursor.execute("SELECT COUNT(*) FROM categorias")
        if cursor.fetchone()[0] == 0:
            categorias = ["Electrónica", "Computación", "Accesorios", "Audio y Video", "Servicios"]
            for cat in categorias:
                cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (cat,))

        cursor.execute("SELECT COUNT(*) FROM proveedores")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO proveedores (cuit, razon_social, contacto, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("30-71234567-9", "Tech Import SRL", "Carlos Gómez", "11-4567-8901", "ventas@techimport.com", "Av. Corrientes 1234, CABA"))
            cursor.execute("""
                INSERT INTO proveedores (cuit, razon_social, contacto, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("30-89654321-4", "Global Soluciones SA", "Mariana López", "11-9876-5432", "contacto@globalsoluciones.com", "Belgrano 450, Rosario"))

        cursor.execute("SELECT COUNT(*) FROM clientes")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO clientes (dni_cuit, nombre, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, ("0", "Consumidor Final", "-", "-", "-"))
            cursor.execute("""
                INSERT INTO clientes (dni_cuit, nombre, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, ("38456123", "Luciana Martínez", "11-2345-6789", "luciana@example.com", "San Martín 789"))

        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            productos_iniciales = [
                ("PRD-1001", "Teclado Mecánico RGB", "Accesorios", 18000.0, 32000.0, 15, 5, 1),
                ("PRD-1002", "Mouse Inalámbrico Gamer", "Accesorios", 12000.0, 22500.0, 8, 3, 1),
                ("PRD-1003", "Monitor 24' IPS 144Hz", "Computación", 85000.0, 145000.0, 4, 2, 1),
                ("PRD-1004", "Auriculares Bluetooth Pro", "Audio y Video", 25000.0, 48000.0, 2, 4, 2),
                ("PRD-1005", "SSD NVMe 1TB HighSpeed", "Computación", 35000.0, 62000.0, 12, 5, 1),
                ("PRD-1006", "Mantenimiento Preventivo PC", "Servicios", 5000.0, 15000.0, 999, 0, None)
            ]
            for p in productos_iniciales:
                cursor.execute("""
                    INSERT INTO productos (codigo, nombre, categoria, precio_costo, precio_venta, stock, stock_minimo, proveedor_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, p)
