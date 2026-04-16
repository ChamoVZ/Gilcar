import tkinter as tk
from gilcar.ui.vehiculos_window import VehiculosWindow

class MenuWindow(tk.Tk):
    def __init__(self, session: dict):
        super().__init__()
        self.session = session

        self.title("Gilcar - Menú Principal")
        self.geometry("460x300")
        self.resizable(False, False)

        tk.Label(self, text="Menú Principal", font=("Arial", 16, "bold")).pack(pady=18)

        tk.Button(self, text="Gestionar Vehículos", width=25, height=2,
                  command=self.abrir_vehiculos).pack(pady=10)

        # Deja esto listo para futuro
        tk.Button(self, text="Gestionar Usuarios", width=25, height=2,
                  state="disabled").pack(pady=10)

        tk.Button(self, text="Salir", width=25, height=2, command=self.destroy).pack(pady=10)

    def abrir_vehiculos(self):
        win = VehiculosWindow(self)
        win.grab_set()
