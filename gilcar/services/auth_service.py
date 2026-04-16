from gilcar.repositories import UsuariosRepo

class AuthService:
    def __init__(self):
        self.repo = UsuariosRepo()

    def login(self, correo: str, password: str) -> dict:
        ok, id_usuario, id_rol = self.repo.validar_login(correo, password)
        if ok != 1:
            return {"ok": False, "message": "Credenciales inválidas"}
        return {"ok": True, "id_usuario": id_usuario, "id_rol": id_rol}
