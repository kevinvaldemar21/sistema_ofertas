from sqlalchemy import select

from database.conexion import obtener_sesion
from models.prestador import Prestador


class PrestadorRepository:

    def obtener_todos(self):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(Prestador)
                .where(Prestador.activo == True)
                .order_by(
                    Prestador.nombre_razon_social
                )
            )

            return list(
                sesion.scalars(
                    consulta
                ).all()
            )

        finally:
            sesion.close()

    def obtener_por_id(self, prestador_id):

        sesion = obtener_sesion()

        try:

            consulta = select(
                Prestador
            ).where(
                Prestador.id == prestador_id
            )

            return sesion.scalar(
                consulta
            )

        finally:
            sesion.close()

    def buscar_por_rfc(self, rfc):

        sesion = obtener_sesion()

        try:

            consulta = select(
                Prestador
            ).where(
                Prestador.rfc == rfc
            )

            return sesion.scalar(
                consulta
            )

        finally:
            sesion.close()

    def crear(
        self,
        nombre_razon_social,
        rfc=None,
        telefono=None,
        domicilio=None,
        registro_padron=None
    ):

        if rfc:

            existente = self.buscar_por_rfc(
                rfc
            )

            if existente:

                raise ValueError(
                "Ya existe un prestador "
                "registrado con ese RFC."
                )

        sesion = obtener_sesion()

        try:

            prestador = Prestador(
                nombre_razon_social=nombre_razon_social,
                rfc=rfc,
                telefono=telefono,
                domicilio=domicilio,
                registro_padron=registro_padron,
                activo=True
            )

            sesion.add(
                prestador
            )

            sesion.commit()

            sesion.refresh(
                prestador
            )

            return prestador

        except Exception:

            sesion.rollback()
            raise

        finally:
            sesion.close()  

    
    def actualizar(
        self,
        prestador_id,
        nombre_razon_social,
        rfc=None,
        telefono=None,
        domicilio=None,
        registro_padron=None
    ):

        sesion = obtener_sesion()

        try:

            prestador = sesion.get(
                Prestador,
                prestador_id
            )

            if prestador is None:

                raise ValueError(
                    "No se encontró el proveedor seleccionado."
                )

            # Verificar que el RFC no pertenezca
            # a otro proveedor.

            if rfc:

                consulta = select(
                    Prestador
                ).where(
                    Prestador.rfc == rfc,
                    Prestador.id != prestador_id
                )

                existente = sesion.scalar(
                    consulta
                )

                if existente:

                    raise ValueError(
                        "Ya existe otro proveedor "
                        "registrado con ese RFC."
                    )

            # Actualizar los campos.

            prestador.nombre_razon_social = (
                nombre_razon_social
            )

            prestador.rfc = rfc
            prestador.telefono = telefono
            prestador.domicilio = domicilio
            prestador.registro_padron = registro_padron

            sesion.commit()

            sesion.refresh(
                prestador
            )

            return prestador

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()
