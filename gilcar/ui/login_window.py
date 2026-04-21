import tkinter as tk
from tkinter import messagebox
from gilcar.services.auth_service import AuthService
from gilcar.ui.menu_window import MenuWindow

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.auth = AuthService()

        self.title("Gilcar - Login")
        self.geometry("420x260")
        self.resizable(False, False)

        tk.Label(self, text="Sistema Gilcar", font=("Arial", 16, "bold")).pack(pady=14)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Correo").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        self.entry_correo = tk.Entry(frame, width=28)
        self.entry_correo.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(frame, text="Contraseña").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.entry_password = tk.Entry(frame, width=28, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=8)

        tk.Button(self, text="Ingresar", width=18, command=self.on_login).pack(pady=14)

       
        self.bind("<Return>", lambda _e: self.on_login())

    def on_login(self):
        correo = self.entry_correo.get().strip()
        password = self.entry_password.get().strip()

        if not correo or not password:
            messagebox.showwarning("Validación", "Ingrese correo y contraseña.")
            return

        try:
            result = self.auth.login(correo, password)
            if not result["ok"]:
                messagebox.showerror("Acceso denegado", result["message"])
                return

            self.destroy()
            menu = MenuWindow(session=result)
            menu.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar sesión.\n\nDetalle: {e}")
