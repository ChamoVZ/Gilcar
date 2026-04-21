import tkinter as tk
from gilcar.ui.vehiculos_window import VehiculosWindow
from gilcar.ui.usuarios_window import UsuariosWindow

class MenuWindow(tk.Tk):
    def __init__(self, session: dict):
        super().__init__()
        self.session = session

        self.title("Gilcar - Menú Principal")
        self.geometry("460x300")
        self.resizable(False, False)

        tk.Label(self, text="Menú Principal", font=("Arial", 16, "bold")).pack(pady=18)

        tk.Button(
            self,
            text="Gestionar Vehículos",
            width=25,
            height=2,
            command=self.abrir_vehiculos
        ).pack(pady=10)

        btn_usuarios = tk.Button(
            self,
            text="Gestionar Usuarios",
            width=25,
            height=2,
            command=self.abrir_usuarios
        )

        rol_raw = self.session.get("id_rol") or self.session.get("rol") or self.session.get("ID_ROL")
        try:
            rol = int(rol_raw)
        except (TypeError, ValueError):
            rol = 0

        if rol == 1:   # 1 = ADMIN
            btn_usuarios.config(state="normal")
        else:
            btn_usuarios.config(state="disabled")

        btn_usuarios.pack(pady=10)

        tk.Button(
            self,
            text="Salir",
            width=25,
            height=2,
            command=self.destroy
        ).pack(pady=10)

    def abrir_vehiculos(self):
        win = VehiculosWindow(self)
        win.grab_set()

    def abrir_usuarios(self):
        win = UsuariosWindow(self)
        win.grab_set()
