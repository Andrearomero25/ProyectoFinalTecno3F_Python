import sqlite3

class Database:
    def __init__(self, db_name="nike_factory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Crea las tablas en la base de datos si no existen."""
        # Tabla de Categorías
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
        """)

        # Tabla de Productos, con eliminación en cascada cuando se elimina una categoría
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
        )
        """)

        # Tabla de Clientes, con eliminación en cascada cuando se elimina un producto
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            producto_id INTEGER,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
        )
        """)

        self.conn.commit()

    def reset_database(self):
        """Elimina todas las tablas y las vuelve a crear."""
        self.cursor.execute("DROP TABLE IF EXISTS categorias")
        self.cursor.execute("DROP TABLE IF EXISTS productos")
        self.cursor.execute("DROP TABLE IF EXISTS clientes")
        self.conn.commit()
        self.create_tables()

    def insert_categoria(self, nombre):
        """Inserta una nueva categoría."""
        self.cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        self.conn.commit()

    def insert_producto(self, nombre, precio, categoria_id):
        """Inserta un nuevo producto."""
        self.cursor.execute("INSERT INTO productos (nombre, precio, categoria_id) VALUES (?, ?, ?)", (nombre, precio, categoria_id))
        self.conn.commit()

    def insert_cliente(self, nombre, email, producto_id):
        """Inserta un nuevo cliente."""
        self.cursor.execute("INSERT INTO clientes (nombre, email, producto_id) VALUES (?, ?, ?)", (nombre, email, producto_id))
        self.conn.commit()

    def get_categorias(self):
        """Obtiene todas las categorías."""
        self.cursor.execute("SELECT * FROM categorias")
        return self.cursor.fetchall()

    def get_productos(self):
        """Obtiene todos los productos."""
        self.cursor.execute("SELECT * FROM productos")
        return self.cursor.fetchall()

    def get_clientes(self):
        """Obtiene todos los clientes."""
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def update_categoria(self, id, nombre):
        """Actualiza una categoría existente."""
        self.cursor.execute("UPDATE categorias SET nombre = ? WHERE id = ?", (nombre, id))
        self.conn.commit()

    def update_producto(self, id, nombre, precio, categoria_id):
        """Actualiza un producto existente."""
        self.cursor.execute("UPDATE productos SET nombre = ?, precio = ?, categoria_id = ? WHERE id = ?", (nombre, precio, categoria_id, id))
        self.conn.commit()

    def update_cliente(self, id, nombre, email, producto_id):
        """Actualiza un cliente existente."""
        self.cursor.execute("UPDATE clientes SET nombre = ?, email = ?, producto_id = ? WHERE id = ?", (nombre, email, producto_id, id))
        self.conn.commit()

    def delete_categoria(self, id):
        """Elimina una categoría y sus productos relacionados."""
        self.cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
        self.conn.commit()

    def delete_producto(self, id):
        """Elimina un producto y sus clientes relacionados."""
        self.cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        self.conn.commit()

    def delete_cliente(self, id):
        """Elimina un cliente."""
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
        self.conn.commit()

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.conn.close()

    def insert_initial_data(self):
        """Inserta datos iniciales en la base de datos."""
        # Insertar categorías
        self.insert_categoria("Zapatillas")
        self.insert_categoria("Camisetas")
        self.insert_categoria("Pantalones")

        # Insertar productos
        self.insert_producto("Air Max 90", 120.50, 1)  # Categoría: Zapatillas (id=1)
        self.insert_producto("Jordan 1", 150.00, 1)   # Categoría: Zapatillas (id=1)
        self.insert_producto("Camiseta Estampada", 30.00, 2)  # Categoría: Camisetas (id=2)
        self.insert_producto("Pantalón Deportivo", 50.00, 3)  # Categoría: Pantalones (id=3)

        # Insertar clientes
        self.insert_cliente("Juan Pérez", "juan@example.com", 1)  # Producto: Air Max 90 (id=1)
        self.insert_cliente("María Gómez", "maria@example.com", 2)  # Producto: Jordan 1 (id=2)
        self.insert_cliente("Carlos López", "carlos@example.com", 3)  # Producto: Camiseta Estampada (id=3)
        self.insert_cliente("Ana Rodríguez", "ana@example.com", 4)  # Producto: Pantalón Deportivo (id=4)