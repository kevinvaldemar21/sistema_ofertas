from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.conexion import obtener_sesion

from models.evaluacion_prestador import (
    EvaluacionPrestador
)


class EvaluacionRepository:

    # ==================================================
    # OBTENER POR ESTUDIO
    # ==================================================

    def obtener_por_estudio(
        self,
        estudio_id
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(EvaluacionPrestador)
                .options(
                    joinedload(
                        EvaluacionPrestador.prestador
                    )
                )
                .where(
                    EvaluacionPrestador.estudio_id
                    == estudio_id
                )
                .order_by(
                    EvaluacionPrestador.id
                )
            )

            return list(
                sesion.scalars(
                    consulta
                )
            )

        finally:

            sesion.close()

    # ==================================================
    # GUARDAR
    # ==================================================

    def guardar(
        self,
        estudio_id,
        prestador_id,
        cumple_cantidad,
        cumple_calidad,
        cumple_oportunidad
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(EvaluacionPrestador)
                .where(
                    EvaluacionPrestador.estudio_id
                    == estudio_id,

                    EvaluacionPrestador.prestador_id
                    == prestador_id
                )
            )

            evaluacion = sesion.scalar(
                consulta
            )

            if evaluacion is None:

                evaluacion = EvaluacionPrestador(
                    estudio_id=estudio_id,
                    prestador_id=prestador_id,
                    cumple_cantidad=cumple_cantidad,
                    cumple_calidad=cumple_calidad,
                    cumple_oportunidad=cumple_oportunidad
                )

                sesion.add(
                    evaluacion
                )

            else:

                evaluacion.cumple_cantidad = (
                    cumple_cantidad
                )

                evaluacion.cumple_calidad = (
                    cumple_calidad
                )

                evaluacion.cumple_oportunidad = (
                    cumple_oportunidad
                )

            sesion.commit()

            return evaluacion

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()