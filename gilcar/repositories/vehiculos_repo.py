import oracledb
from typing import List, Dict, Any
from gilcar.data import get_connection

class VehiculosRepo:
    def listar_disponibles(self) -> List[Dict[str, Any]]:
        with get_connection() as cn:
            with cn.cursor() as cur:
                out_cur = cur.var(oracledb.CURSOR)
                cur.callproc("PKG_VEHICULOS.SP_LISTAR_DISPONIBLES", [out_cur])
                rows = out_cur.getvalue().fetchall()

        vehiculos = []
        for r in rows:
            # Según tu SELECT del paquete, vienen varios campos; para UI usamos los principales.
            vehiculos.append({
                "id_vehiculo": r[0],
                "marca": r[1],
                "modelo": r[2],
                "anio": r[3],
                "tipo": r[4],
                "km": r[5],
                "combustible": r[6],
                "precio": float(r[7]),
                "color": r[8],
            })
        return vehiculos

    def insertar(self, data: Dict[str, Any]) -> int:
        with get_connection() as cn:
            with cn.cursor() as cur:
                out_id = cur.var(int)
                cur.callproc("PKG_VEHICULOS.SP_INSERTAR", [
                    data["marca"],
                    data["modelo"],
                    int(data["anio"]),
                    data["tipo"],
                    int(data["km"]),
                    data["combustible"],
                    float(data["precio"]),
                    data["color"],
                    data.get("descripcion"),
                    out_id
                ])
                cn.commit()
                return int(out_id.getvalue())

    def actualizar(self, id_vehiculo: int, data: Dict[str, Any]) -> None:
        with get_connection() as cn:
            with cn.cursor() as cur:
                cur.callproc("PKG_VEHICULOS.SP_ACTUALIZAR", [
                    int(id_vehiculo),
                    data["marca"],
                    data["modelo"],
                    int(data["anio"]),
                    data["tipo"],
                    int(data["km"]),
                    data["combustible"],
                    float(data["precio"]),
                    data["color"],
                    data.get("descripcion")
                ])
                cn.commit()

    def inactivar(self, id_vehiculo: int) -> None:
        with get_connection() as cn:
            with cn.cursor() as cur:
                cur.callproc("PKG_VEHICULOS.SP_INACTIVAR", [int(id_vehiculo)])
                cn.commit()
