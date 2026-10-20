from sqlalchemy import select

from database.conexion import obtener_sesion
from models.area import Area
from models.proyecto import Proyecto


class AreaRepository:

    def obtener_areas(self):
        sesion = obtener_sesion()

        try:
            consulta = (
                select(Area)
                .where(Area.activo == True)
                .order_by(Area.descripcion)
            )

            return list(
                sesion.scalars(consulta).all()
            )

        finally:
            sesion.close()

    def obtener_proyectos_por_area(self, area_id):
        sesion = obtener_sesion()

        try:
            consulta = (
                select(Proyecto)
                .where(
                    Proyecto.area_id == area_id,
                    Proyecto.activo == True
                )
                .order_by(Proyecto.codigo_proyecto)
            )

            return list(
                sesion.scalars(consulta).all()
            )

        finally:
            sesion.close()