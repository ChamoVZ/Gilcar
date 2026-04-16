from dataclasses import dataclass
from typing import Optional

@dataclass
class Vehiculo:
    id_vehiculo: Optional[int]
    marca: str
    modelo: str
    anio: int
    tipo: str
    km: int
    combustible: str
    precio: float
    color: str
    descripcion: str = ""

from .vehiculo import Vehiculo
__all__ = ["Vehiculo"]
