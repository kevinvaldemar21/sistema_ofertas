from sqlalchemy import select

from database.conexion import obtener_sesion
from models.condiciones_estudio import CondicionesEstudio


class CondicionesRepository:

    def obtener_por_estudio(
        self,
        estudio_id
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(CondicionesEstudio)
                .where(
                    CondicionesEstudio.estudio_id
                    == estudio_id
                )
            )

            return sesion.scalar(
                consulta
            )

        finally:

            sesion.close()

    def guardar(
        self,
        estudio_id,
        lugar_entrega,
        plazo_entrega,
        forma_pago,
        vigencia_cotizacion,
        tipo_procedimiento
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(CondicionesEstudio)
                .where(
                    CondicionesEstudio.estudio_id
                    == estudio_id
                )
            )

            condiciones = sesion.scalar(
                consulta
            )

            if condiciones is None:

                condiciones = CondicionesEstudio(
                    estudio_id=estudio_id,
                    lugar_entrega=lugar_entrega,
                    plazo_entrega=plazo_entrega,
                    forma_pago=forma_pago,
                    vigencia_cotizacion=vigencia_cotizacion,
                    tipo_procedimiento=tipo_procedimiento
                )

                sesion.add(
                    condiciones
                )

            else:

                condiciones.lugar_entrega = (
                    lugar_entrega
                )

                condiciones.plazo_entrega = (
                    plazo_entrega
                )

                condiciones.forma_pago = (
                    forma_pago
                )

                condiciones.vigencia_cotizacion = (
                    vigencia_cotizacion
                )

                condiciones.tipo_procedimiento = (
                    tipo_procedimiento
                )

            sesion.commit()

            sesion.refresh(
                condiciones
            )

            return condiciones

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()