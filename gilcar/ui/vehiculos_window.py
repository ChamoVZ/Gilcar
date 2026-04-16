import tkinter as tk
from tkinter import ttk, messagebox
from gilcar.repositories import VehiculosRepo

class VehiculosWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.repo = VehiculosRepo()
        self.id_seleccionado = None

        self.title("Gestión de Vehículos")
        self.geometry("980x520")

        tk.Label(self, text="Gestión de Vehículos", font=("Arial", 16, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=8)

        self._campo(form, "Marca", 0, 0);        self.marca = tk.Entry(form); self.marca.grid(row=0, column=1)
        self._campo(form, "Modelo", 0, 2);       self.modelo = tk.Entry(form); self.modelo.grid(row=0, column=3)
        self._campo(form, "Año", 1, 0);          self.anio = tk.Entry(form); self.anio.grid(row=1, column=1)
        self._campo(form, "Tipo", 1, 2);         self.tipo = tk.Entry(form); self.tipo.grid(row=1, column=3)
        self._campo(form, "KM", 2, 0);           self.km = tk.Entry(form); self.km.grid(row=2, column=1)
        self._campo(form, "Combustible", 2, 2);  self.comb = tk.Entry(form); self.comb.grid(row=2, column=3)
        self._campo(form, "Color", 3, 0);        self.color = tk.Entry(form); self.color.grid(row=3, column=1)
        self._campo(form, "Precio", 3, 2);       self.precio = tk.Entry(form); self.precio.grid(row=3, column=3)

        botones = tk.Frame(self)
        botones.pack(pady=10)
        tk.Button(botones, text="Guardar", width=12, command=self.guardar).grid(row=0, column=0, padx=6)
        tk.Button(botones, text="Actualizar", width=12, command=self.actualizar).grid(row=0, column=1, padx=6)
        tk.Button(botones, text="Inactivar", width=12, command=self.inactivar).grid(row=0, column=2, padx=6)
        tk.Button(botones, text="Limpiar", width=12, command=self.limpiar).grid(row=0, column=3, padx=6)

        cols = ("ID", "Marca", "Modelo", "Año", "Tipo", "KM", "Combustible", "Color", "Precio")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=100)
        self.tabla.pack(pady=10, fill="x", padx=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

        self.cargar_tabla()

    def _campo(self, parent, texto, r, c):
        tk.Label(parent, text=texto).grid(row=r, column=c, padx=8, pady=5, sticky="e")

    def validar(self):
        try:
            data = {
                "marca": self.marca.get().strip(),
                "modelo": self.modelo.get().strip(),
                "anio": int(self.anio.get().strip()),
                "tipo": self.tipo.get().strip(),
                "km": int(self.km.get().strip()),
                "combustible": self.comb.get().strip(),
                "color": self.color.get().strip(),
                "precio": float(self.precio.get().strip()),
            }
        except Exception:
            messagebox.showwarning("Validación", "Revisá Año/KM/Precio: deben ser numéricos.")
            return None

        if not data["marca"] or not data["modelo"]:
            messagebox.showwarning("Validación", "Marca y Modelo son obligatorios.")
            return None

        return data

    def cargar_tabla(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        for v in self.repo.listar_disponibles():
            self.tabla.insert("", "end", values=(
                v["id_vehiculo"], v["marca"], v["modelo"], v["anio"],
                v["tipo"], v["km"], v["combustible"], v["color"], v["precio"]
            ))

    def guardar(self):
        data = self.validar()
        if not data:
            return
        try:
            new_id = self.repo.insertar(data)
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("OK", f"Vehículo insertado con ID {new_id}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar.\n\nDetalle: {e}")

    def actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccioná un vehículo.")
            return
        data = self.validar()
        if not data:
            return
        try:
            self.repo.actualizar(self.id_seleccionado, data)
            self.cargar_tabla()
            messagebox.showinfo("OK", "Vehículo actualizado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar.\n\nDetalle: {e}")

    def inactivar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccioná un vehículo.")
            return
        try:
            self.repo.inactivar(self.id_seleccionado)
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("OK", "Vehículo inactivado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo inactivar.\n\nDetalle: {e}")

    def seleccionar(self, _event):
        sel = self.tabla.selection()
        if not sel:
            return
        values = self.tabla.item(sel[0], "values")
        self.id_seleccionado = int(values[0])

        self.limpiar(keep_id=True)
        self.marca.insert(0, values[1])
        self.modelo.insert(0, values[2])
        self.anio.insert(0, values[3])
        self.tipo.insert(0, values[4])
        self.km.insert(0, values[5])
        self.comb.insert(0, values[6])
        self.color.insert(0, values[7])
        self.precio.insert(0, values[8])

    def limpiar(self, keep_id=False):
        if not keep_id:
            self.id_seleccionado = None
        for e in (self.marca, self.modelo, self.anio, self.tipo, self.km, self.comb, self.color, self.precio):
            e.delete(0, tk.END)
