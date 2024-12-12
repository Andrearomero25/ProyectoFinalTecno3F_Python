import tkinter as tk
from tkinter import ttk
from database import Database
import os
from tkinter import messagebox  # Importamos messagebox para mostrar mensajes de error
import re  # Importamos re para validar el formato de correo electrónico


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NIKE: Indumentaria y Zapatillas")
        self.geometry("825x525")
        self.resizable(0, 0)

        # Establecer el ícono de la ventana
        self.iconbitmap(os.path.join(os.getcwd(), "logo.ico"))  # Usa el archivo .ico que tienes en el directorio raíz

        # Configuración del estilo de la interfaz
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Cambia el tema para un diseño más moderno
        self.style.configure("TButton", padding=5, relief="flat", foreground="white", background="#0078D7")
        self.style.map("TButton", background=[("active", "#005A9E")])
        self.style.configure("TLabel", foreground="black", background="#F0F0F0", font=("Arial", 10))
        self.style.configure("TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF")
        self.style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", foreground="black")
        self.style.configure("Treeview.Heading", background="#0078D7", foreground="white", font=("Arial", 10, "bold"))

        # Crear instancia de la base de datos y reiniciarla con datos iniciales
        self.db = Database()
        self.db.reset_database()  # Reiniciar la base de datos
        self.db.insert_initial_data()  # Insertar datos iniciales

        # Crear un diseño alternativo sin usar logo.png
        self.create_header()
        self.create_widgets()

    def create_header(self):
        """Crea un encabezado alternativo sin usar logo.png."""
        header_frame = ttk.Frame(self, style="TLabel")
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = ttk.Label(header_frame, text="NIKE: Indumentaria y Zapatillas", font=("Arial", 16, "bold"), foreground="#0078D7", background="#F0F0F0")
        title_label.pack(side="left", padx=10)

    def create_widgets(self):
        """Crea los widgets de la interfaz."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_categorias = ttk.Frame(self.notebook)
        self.tab_productos = ttk.Frame(self.notebook)
        self.tab_clientes = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_categorias, text="Categorías")
        self.notebook.add(self.tab_productos, text="Productos")
        self.notebook.add(self.tab_clientes, text="Clientes")

        self.create_categoria_widgets()
        self.create_producto_widgets()
        self.create_cliente_widgets()

    def create_categoria_widgets(self):
        """Crea los widgets para la pestaña de Categorías."""
        self.label_nombre_categoria = ttk.Label(self.tab_categorias, text="Nombre de la Categoría:")
        self.label_nombre_categoria.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_nombre_categoria = ttk.Entry(self.tab_categorias)
        self.entry_nombre_categoria.grid(row=0, column=1, padx=10, pady=10)

        self.btn_agregar_categoria = ttk.Button(self.tab_categorias, text="Agregar", command=self.agregar_categoria)
        self.btn_agregar_categoria.grid(row=1, column=0, padx=10, pady=10)

        self.btn_actualizar_categoria = ttk.Button(self.tab_categorias, text="Actualizar", command=self.actualizar_categoria)
        self.btn_actualizar_categoria.grid(row=1, column=1, padx=10, pady=10)

        self.btn_eliminar_categoria = ttk.Button(self.tab_categorias, text="Eliminar", command=self.eliminar_categoria)
        self.btn_eliminar_categoria.grid(row=1, column=2, padx=10, pady=10)

        self.tree_categorias = ttk.Treeview(self.tab_categorias, columns=("ID", "Nombre"), show="headings")
        self.tree_categorias.heading("ID", text="ID")
        self.tree_categorias.heading("Nombre", text="Nombre")
        self.tree_categorias.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.populate_categorias()

    def create_producto_widgets(self):
        """Crea los widgets para la pestaña de Productos."""
        self.label_nombre_producto = ttk.Label(self.tab_productos, text="Nombre del Producto:")
        self.label_nombre_producto.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_nombre_producto = ttk.Entry(self.tab_productos)
        self.entry_nombre_producto.grid(row=0, column=1, padx=10, pady=10)

        self.label_precio_producto = ttk.Label(self.tab_productos, text="Precio:")
        self.label_precio_producto.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_precio_producto = ttk.Entry(self.tab_productos)
        self.entry_precio_producto.grid(row=1, column=1, padx=10, pady=10)

        self.label_categoria_producto = ttk.Label(self.tab_productos, text="Categoría:")
        self.label_categoria_producto.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.combo_categoria_producto = ttk.Combobox(self.tab_productos)
        self.combo_categoria_producto.grid(row=2, column=1, padx=10, pady=10)
        self.populate_categorias_combo()

        self.btn_agregar_producto = ttk.Button(self.tab_productos, text="Agregar", command=self.agregar_producto)
        self.btn_agregar_producto.grid(row=3, column=0, padx=10, pady=10)

        self.btn_actualizar_producto = ttk.Button(self.tab_productos, text="Actualizar", command=self.actualizar_producto)
        self.btn_actualizar_producto.grid(row=3, column=1, padx=10, pady=10)

        self.btn_eliminar_producto = ttk.Button(self.tab_productos, text="Eliminar", command=self.eliminar_producto)
        self.btn_eliminar_producto.grid(row=3, column=2, padx=10, pady=10)

        self.tree_productos = ttk.Treeview(self.tab_productos, columns=("ID", "Nombre", "Precio", "Categoría"), show="headings")
        self.tree_productos.heading("ID", text="ID")
        self.tree_productos.heading("Nombre", text="Nombre")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Categoría", text="Categoría")
        self.tree_productos.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.populate_productos()

    def create_cliente_widgets(self):
        """Crea los widgets para la pestaña de Clientes."""
        self.label_nombre_cliente = ttk.Label(self.tab_clientes, text="Nombre del Cliente:")
        self.label_nombre_cliente.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_nombre_cliente = ttk.Entry(self.tab_clientes)
        self.entry_nombre_cliente.grid(row=0, column=1, padx=10, pady=10)

        self.label_email_cliente = ttk.Label(self.tab_clientes, text="Email:")
        self.label_email_cliente.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_email_cliente = ttk.Entry(self.tab_clientes)
        self.entry_email_cliente.grid(row=1, column=1, padx=10, pady=10)

        self.label_producto_cliente = ttk.Label(self.tab_clientes, text="Producto:")
        self.label_producto_cliente.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.combo_producto_cliente = ttk.Combobox(self.tab_clientes)
        self.combo_producto_cliente.grid(row=2, column=1, padx=10, pady=10)
        self.populate_productos_combo()

        self.btn_agregar_cliente = ttk.Button(self.tab_clientes, text="Agregar", command=self.agregar_cliente)
        self.btn_agregar_cliente.grid(row=3, column=0, padx=10, pady=10)

        self.btn_actualizar_cliente = ttk.Button(self.tab_clientes, text="Actualizar", command=self.actualizar_cliente)
        self.btn_actualizar_cliente.grid(row=3, column=1, padx=10, pady=10)

        self.btn_eliminar_cliente = ttk.Button(self.tab_clientes, text="Eliminar", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=3, column=2, padx=10, pady=10)

        self.tree_clientes = ttk.Treeview(self.tab_clientes, columns=("ID", "Nombre", "Email", "Producto"), show="headings")
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.heading("Producto", text="Producto")
        self.tree_clientes.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.populate_clientes()

    def populate_categorias(self):
        """Llena la tabla de Categorías con los datos de la base de datos."""
        categorias = self.db.get_categorias()
        self.tree_categorias.delete(*self.tree_categorias.get_children())
        for categoria in categorias:
            self.tree_categorias.insert("", "end", values=categoria)

    def populate_productos(self):
        """Llena la tabla de Productos con los datos de la base de datos."""
        productos = self.db.get_productos()
        self.tree_productos.delete(*self.tree_productos.get_children())
        for producto in productos:
            self.tree_productos.insert("", "end", values=producto)

    def populate_clientes(self):
        """Llena la tabla de Clientes con los datos de la base de datos."""
        clientes = self.db.get_clientes()
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        for cliente in clientes:
            self.tree_clientes.insert("", "end", values=cliente)

    def populate_categorias_combo(self):
        """Llena el Combobox de Categorías."""
        categorias = self.db.get_categorias()
        categorias_list = [f"{cat[0]} - {cat[1]}" for cat in categorias]
        self.combo_categoria_producto["values"] = categorias_list

    def populate_productos_combo(self):
        """Llena el Combobox de Productos."""
        productos = self.db.get_productos()
        productos_list = [f"{prod[0]} - {prod[1]}" for prod in productos]
        self.combo_producto_cliente["values"] = productos_list

    def agregar_categoria(self):
        """Agrega una nueva categoría."""
        nombre = self.entry_nombre_categoria.get()

        # Validación: Asegurarse de que el campo no esté vacío
        if not nombre:
            messagebox.showerror("Error", "El nombre de la categoría no puede estar vacío.")
            return

        self.db.insert_categoria(nombre)
        self.populate_categorias()
        self.entry_nombre_categoria.delete(0, tk.END)

    def actualizar_categoria(self):
        """Actualiza una categoría existente."""
        selected_item = self.tree_categorias.selection()
        if selected_item:
            id = self.tree_categorias.item(selected_item)["values"][0]
            nombre = self.entry_nombre_categoria.get()

            # Validación: Asegurarse de que el campo no esté vacío
            if not nombre:
                messagebox.showerror("Error", "El nombre de la categoría no puede estar vacío.")
                return

            self.db.update_categoria(id, nombre)
            self.populate_categorias()
            self.entry_nombre_categoria.delete(0, tk.END)

    def eliminar_categoria(self):
        """Elimina una categoría."""
        selected_item = self.tree_categorias.selection()
        if selected_item:
            id = self.tree_categorias.item(selected_item)["values"][0]
            self.db.delete_categoria(id)
            self.populate_categorias()

    def agregar_producto(self):
        """Agrega un nuevo producto."""
        nombre = self.entry_nombre_producto.get()
        precio = self.entry_precio_producto.get()
        categoria = self.combo_categoria_producto.get()

        # Validación: Asegurarse de que el precio sea un número
        if not precio.replace(".", "", 1).isdigit():
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        if nombre and precio and categoria:
            categoria_id = int(categoria.split(" - ")[0])
            self.db.insert_producto(nombre, float(precio), categoria_id)
            self.populate_productos()
            self.entry_nombre_producto.delete(0, tk.END)
            self.entry_precio_producto.delete(0, tk.END)
            self.combo_categoria_producto.set("")

    def actualizar_producto(self):
        """Actualiza un producto existente."""
        selected_item = self.tree_productos.selection()
        if selected_item:
            id = self.tree_productos.item(selected_item)["values"][0]
            nombre = self.entry_nombre_producto.get()
            precio = self.entry_precio_producto.get()
            categoria = self.combo_categoria_producto.get()

            # Validación: Asegurarse de que el precio sea un número
            if not precio.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "El precio debe ser un número válido.")
                return

            if nombre and precio and categoria:
                categoria_id = int(categoria.split(" - ")[0])
                self.db.update_producto(id, nombre, float(precio), categoria_id)
                self.populate_productos()
                self.entry_nombre_producto.delete(0, tk.END)
                self.entry_precio_producto.delete(0, tk.END)
                self.combo_categoria_producto.set("")

    def eliminar_producto(self):
        """Elimina un producto."""
        selected_item = self.tree_productos.selection()
        if selected_item:
            id = self.tree_productos.item(selected_item)["values"][0]
            self.db.delete_producto(id)
            self.populate_productos()

    def agregar_cliente(self):
        """Agrega un nuevo cliente."""
        nombre = self.entry_nombre_cliente.get()
        email = self.entry_email_cliente.get()
        producto = self.combo_producto_cliente.get()

        # Validación: Asegurarse de que el correo electrónico tenga un formato válido
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "El correo electrónico no tiene un formato válido.")
            return

        if not producto:
            messagebox.showerror("Error", "Debes seleccionar un producto.")
            return

        if nombre and email and producto:
            producto_id = int(producto.split(" - ")[0])
            self.db.insert_cliente(nombre, email, producto_id)
            self.populate_clientes()
            self.entry_nombre_cliente.delete(0, tk.END)
            self.entry_email_cliente.delete(0, tk.END)
            self.combo_producto_cliente.set("")

    def actualizar_cliente(self):
        """Actualiza un cliente existente."""
        selected_item = self.tree_clientes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar un cliente para actualizar.")
            return

        id = self.tree_clientes.item(selected_item)["values"][0]
        nombre = self.entry_nombre_cliente.get()
        email = self.entry_email_cliente.get()
        producto = self.combo_producto_cliente.get()

        # Validación: Asegurarse de que el correo electrónico tenga un formato válido
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "El correo electrónico no tiene un formato válido.")
            return

        if not producto:
            messagebox.showerror("Error", "Debes seleccionar un producto.")
            return

        if nombre and email and producto:
            producto_id = int(producto.split(" - ")[0])
            self.db.update_cliente(id, nombre, email, producto_id)
            self.populate_clientes()
            self.entry_nombre_cliente.delete(0, tk.END)
            self.entry_email_cliente.delete(0, tk.END)
            self.combo_producto_cliente.set("")

    def eliminar_cliente(self):
        """Elimina un cliente."""
        selected_item = self.tree_clientes.selection()
        if selected_item:
            id = self.tree_clientes.item(selected_item)["values"][0]
            self.db.delete_cliente(id)
            self.populate_clientes()


if __name__ == "__main__":
    app = App()
    app.mainloop()