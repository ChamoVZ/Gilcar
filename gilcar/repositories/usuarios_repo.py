class UsuariosRepo:
    def validar_login(self, correo: str, password: str):
        """
        Devuelve: (ok:int, id_usuario:int|None, id_rol:int|None)
        """
        import oracledb
        from gilcar.data import get_connection

        with get_connection() as cn:
            with cn.cursor() as cur:
                p_ok = cur.var(int)
                p_id_usuario = cur.var(int)
                p_id_rol = cur.var(int)

                cur.callproc("PKG_USUARIOS.SP_VALIDAR_LOGIN", [
                    correo,
                    password,
                    p_ok,
                    p_id_usuario,
                    p_id_rol
                ])

                ok = int(p_ok.getvalue())
                id_usuario = p_id_usuario.getvalue()
                id_rol = p_id_rol.getvalue()
                return ok, id_usuario, id_rol
