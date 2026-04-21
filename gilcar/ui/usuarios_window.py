import tkinter as tk
from tkinter import ttk, messagebox
from gilcar.repositories.usuarios_repo import UsuariosRepo


class UsuariosWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.repo = UsuariosRepo()
        self.id_seleccionado = None
        self.roles_map = {}

        self.title("Gestión de Usuarios")
        self.geometry("1150x560")

        tk.Label(self, text="Gestión de Usuarios", font=("Arial", 16, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=8)

        self._campo(form, "Nombre", 0, 0)
        self.nombre = tk.Entry(form, width=28)
        self.nombre.grid(row=0, column=1, padx=5, pady=5)

        self._campo(form, "Apellidos", 0, 2)
        self.apellidos = tk.Entry(form, width=28)
        self.apellidos.grid(row=0, column=3, padx=5, pady=5)

        self._campo(form, "Correo", 1, 0)
        self.correo = tk.Entry(form, width=28)
        self.correo.grid(row=1, column=1, padx=5, pady=5)

        self._campo(form, "Teléfono", 1, 2)
        self.telefono = tk.Entry(form, width=28)
        self.telefono.grid(row=1, column=3, padx=5, pady=5)

        self._campo(form, "Contraseña", 2, 0)
        self.password = tk.Entry(form, width=28, show="*")
        self.password.grid(row=2, column=1, padx=5, pady=5)

        self._campo(form, "Rol", 2, 2)
        self.rol = ttk.Combobox(form, width=26, state="readonly")
        self.rol.grid(row=2, column=3, padx=5, pady=5)

        self._campo(form, "Estado", 3, 0)
        self.estado = ttk.Combobox(
            form,
            width=26,
            state="readonly",
            values=["ACTIVO", "INACTIVO", "BLOQUEADO"]
        )
        self.estado.grid(row=3, column=1, padx=5, pady=5)
        self.estado.set("ACTIVO")

        botones = tk.Frame(self)
        botones.pack(pady=10)

        tk.Button(botones, text="Guardar", width=12, command=self.guardar).grid(row=0, column=0, padx=6)
        tk.Button(botones, text="Actualizar", width=12, command=self.actualizar).grid(row=0, column=1, padx=6)
        tk.Button(botones, text="Inactivar", width=12, command=self.inactivar).grid(row=0, column=2, padx=6)
        tk.Button(botones, text="Limpiar", width=12, command=self.limpiar).grid(row=0, column=3, padx=6)

        cols = ("ID", "Nombre", "Apellidos", "Correo", "Teléfono", "Rol", "Estado", "Fecha Registro")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=14)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=130)

        self.tabla.pack(pady=10, fill="both", expand=True, padx=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

        
        self.cargar_roles()
        self.cargar_tabla()

    def _campo(self, parent, texto, r, c):
        tk.Label(parent, text=texto).grid(row=r, column=c, padx=8, pady=5, sticky="e")

    def cargar_roles(self):
        roles = self.repo.listar_roles()
        # roles: lista de dicts: {"id_rol":..., "nombre":...}
        self.roles_map = {r["nombre"]: r["id_rol"] for r in roles}
        self.rol["values"] = list(self.roles_map.keys())

        if roles:
            self.rol.set(roles[0]["nombre"])

    def validar(self, es_nuevo=False):
        nombre = self.nombre.get().strip()
        apellidos = self.apellidos.get().strip()
        correo = self.correo.get().strip().lower()
        telefono = self.telefono.get().strip()
        password = self.password.get().strip()
        rol_nombre = self.rol.get().strip()
        estado = self.estado.get().strip()

        if not nombre or not apellidos or not correo or not rol_nombre or not estado:
            messagebox.showwarning("Validación", "Complete los campos obligatorios.")
            return None

        if es_nuevo and not password:
            messagebox.showwarning("Validación", "La contraseña es obligatoria para nuevos usuarios.")
            return None

        return {
            "nombre": nombre,
            "apellidos": apellidos,
            "correo": correo,
            "telefono": telefono or None,
            "password": password or None,
            "id_rol": self.roles_map[rol_nombre],
            "estado_cuenta": estado
        }

    def cargar_tabla(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)

        for u in self.repo.listar():
            self.tabla.insert("", "end", values=(
                u["id_usuario"],
                u["nombre"],
                u["apellidos"],
                u["correo"],
                u["telefono"],
                u["rol"],
                u["estado_cuenta"],
                u["fecha_registro"]
            ))

    def guardar(self):
        data = self.validar(es_nuevo=True)
        if not data:
            return
        try:
            new_id = self.repo.insertar(data)
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("OK", f"Usuario insertado con ID {new_id}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar.\n\nDetalle: {e}")

    def actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccione un usuario.")
            return

        data = self.validar(es_nuevo=False)
        if not data:
            return

        try:
            self.repo.actualizar(self.id_seleccionado, data)
            self.cargar_tabla()
            messagebox.showinfo("OK", "Usuario actualizado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar.\n\nDetalle: {e}")

    def inactivar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccione un usuario.")
            return

        try:
            self.repo.inactivar(self.id_seleccionado)
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("OK", "Usuario inactivado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo inactivar.\n\nDetalle: {e}")

    def seleccionar(self, _event):
        sel = self.tabla.selection()
        if not sel:
            return

        values = self.tabla.item(sel[0], "values")
        self.id_seleccionado = int(values[0])

        detalle = self.repo.obtener_por_id(self.id_seleccionado)
        if not detalle:
            return

        self.limpiar(keep_id=True)
        self.nombre.insert(0, detalle["nombre"])
        self.apellidos.insert(0, detalle["apellidos"])
        self.correo.insert(0, detalle["correo"])

        if detalle.get("telefono"):
            self.telefono.insert(0, detalle["telefono"])

        
        for nombre_rol, id_rol in self.roles_map.items():
            if id_rol == detalle["id_rol"]:
                self.rol.set(nombre_rol)
                break

        self.estado.set(detalle["estado_cuenta"])

    def limpiar(self, keep_id=False):
        if not keep_id:
            self.id_seleccionado = None

        for e in (self.nombre, self.apellidos, self.correo, self.telefono, self.password):
            e.delete(0, tk.END)

        if self.rol["values"]:
            self.rol.set(self.rol["values"][0])

        self.estado.set("ACTIVO")
