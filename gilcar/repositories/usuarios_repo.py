import oracledb
from gilcar.data.db import get_connection


class UsuariosRepo:
   
    def validar_login(self, correo: str, password: str):
        """
        Retorna: (ok:int, id_usuario:int|None, id_rol:int|None)
        Llama: PKG_USUARIOS.SP_VALIDAR_LOGIN
        """
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

                ok = int(p_ok.getvalue() or 0)
                id_usuario = p_id_usuario.getvalue()
                id_rol = p_id_rol.getvalue()

                # Normalizar tipos (Oracle puede devolver Decimal)
                id_usuario = int(id_usuario) if id_usuario is not None else None
                id_rol = int(id_rol) if id_rol is not None else None

                return ok, id_usuario, id_rol

  
    def listar_roles(self):
        """
        Retorna lista de dicts: [{"id_rol": 1, "nombre": "ADMIN"}, ...]
        """
        with get_connection() as cn:
            with cn.cursor() as cur:
                cur.execute("""
                    SELECT ID_ROL, NOMBRE
                    FROM ROLES
                    ORDER BY ID_ROL
                """)
                rows = cur.fetchall()

        return [{"id_rol": int(r[0]), "nombre": r[1]} for r in rows]


    def listar(self):
        """
        Retorna lista de usuarios para la tabla (TreeView).
        """
        with get_connection() as cn:
            with cn.cursor() as cur:
                cur.execute("""
                    SELECT
                        U.ID_USUARIO,
                        U.NOMBRE,
                        U.APELLIDOS,
                        U.CORREO,
                        NVL(U.TELEFONO, ''),
                        R.NOMBRE AS ROL,
                        U.ESTADO_CUENTA,
                        TO_CHAR(U.FECHA_REGISTRO, 'YYYY-MM-DD HH24:MI')
                    FROM USUARIOS U
                    JOIN ROLES R ON R.ID_ROL = U.ID_ROL
                    ORDER BY U.ID_USUARIO
                """)
                rows = cur.fetchall()

        data = []
        for r in rows:
            data.append({
                "id_usuario": int(r[0]),
                "nombre": r[1],
                "apellidos": r[2],
                "correo": r[3],
                "telefono": r[4],
                "rol": r[5],
                "estado_cuenta": r[6],
                "fecha_registro": r[7]
            })
        return data

    def obtener_por_id(self, id_usuario: int):
        """
        Retorna dict con detalle para cargar formulario.
        """
        with get_connection() as cn:
            with cn.cursor() as cur:
                cur.execute("""
                    SELECT
                        ID_USUARIO,
                        NOMBRE,
                        APELLIDOS,
                        CORREO,
                        TELEFONO,
                        ID_ROL,
                        ESTADO_CUENTA
                    FROM USUARIOS
                    WHERE ID_USUARIO = :id
                """, {"id": int(id_usuario)})
                row = cur.fetchone()

        if not row:
            return None

        return {
            "id_usuario": int(row[0]),
            "nombre": row[1],
            "apellidos": row[2],
            "correo": row[3],
            "telefono": row[4],
            "id_rol": int(row[5]),
            "estado_cuenta": row[6]
        }

  
    def insertar(self, data: dict):
        """
        Inserta usuario usando PL/SQL:
        PKG_USUARIOS.SP_CREAR_USUARIO(nombre, apellidos, correo, telefono, password, nombre_rol, id_out)
        Para que tu UI no use SQL directo al crear.
        """
        # Convertir id_rol -> nombre_rol para el SP
        nombre_rol = self._rol_nombre_por_id(data["id_rol"])

        with get_connection() as cn:
            with cn.cursor() as cur:
                out_id = cur.var(int)

                cur.callproc("PKG_USUARIOS.SP_CREAR_USUARIO", [
                    data["nombre"],
                    data["apellidos"],
                    data["correo"],
                    data.get("telefono"),
                    data["password"],      
                    nombre_rol,
                    out_id
                ])

                try:
                    cn.commit()
                except Exception:
                    pass

                return int(out_id.getvalue())

    def _rol_nombre_por_id(self, id_rol: int) -> str:
        """
        Convierte ID_ROL a nombre de rol para SP_CREAR_USUARIO.
        """
        with get_connection() as cn:
            with cn.cursor() as cur:
                cur.execute("SELECT NOMBRE FROM ROLES WHERE ID_ROL = :id", {"id": int(id_rol)})
                row = cur.fetchone()
        if not row:
            raise Exception("Rol no encontrado en ROLES.")
        return row[0]


    def actualizar(self, id_usuario: int, data: dict):
        """
        Actualiza datos del usuario.
        - Si password viene None/vacío: no cambia contraseña.
        """
        pwd = data.get("password")
        with get_connection() as cn:
            with cn.cursor() as cur:
                if pwd is None or str(pwd).strip() == "":
                    cur.execute("""
                        UPDATE USUARIOS
                           SET NOMBRE = :nombre,
                               APELLIDOS = :apellidos,
                               CORREO = :correo,
                               TELEFONO = :telefono,
                               ID_ROL = :id_rol,
                               ESTADO_CUENTA = :estado
                         WHERE ID_USUARIO = :id
                    """, {
                        "nombre": data["nombre"],
                        "apellidos": data["apellidos"],
                        "correo": data["correo"],
                        "telefono": data.get("telefono"),
                        "id_rol": int(data["id_rol"]),
                        "estado": data["estado_cuenta"],
                        "id": int(id_usuario)
                    })
                else:
                    cur.execute("""
                        UPDATE USUARIOS
                           SET NOMBRE = :nombre,
                               APELLIDOS = :apellidos,
                               CORREO = :correo,
                               TELEFONO = :telefono,
                               CONTRASENA_ENCRIPTADA = :pwd,
                               ID_ROL = :id_rol,
                               ESTADO_CUENTA = :estado
                         WHERE ID_USUARIO = :id
                    """, {
                        "nombre": data["nombre"],
                        "apellidos": data["apellidos"],
                        "correo": data["correo"],
                        "telefono": data.get("telefono"),
                        "pwd": pwd,
                        "id_rol": int(data["id_rol"]),
                        "estado": data["estado_cuenta"],
                        "id": int(id_usuario)
                    })

                if cur.rowcount == 0:
                    raise Exception("Usuario no existe.")

                cn.commit()


    def inactivar(self, id_usuario: int):
        with get_connection() as cn:
            with cn.cursor() as cur:
                cur.execute("""
                    UPDATE USUARIOS
                       SET ESTADO_CUENTA = 'INACTIVO'
                     WHERE ID_USUARIO = :id
                """, {"id": int(id_usuario)})

                if cur.rowcount == 0:
                    raise Exception("Usuario no existe.")

                cn.commit()
