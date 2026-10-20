from sqlalchemy import select

from database.conexion import obtener_sesion
from models.concepto_estudio import ConceptoEstudio


class ConceptoRepository:

    def guardar_lista(
        self,
        estudio_id,
        conceptos_datos
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(ConceptoEstudio)
                .where(
                    ConceptoEstudio.estudio_id
                    == estudio_id
                )
            )

            existentes = list(
                sesion.scalars(
                    consulta
                ).all()
            )

            existentes_por_numero = {
                concepto.numero: concepto
                for concepto in existentes
            }

            numeros_recibidos = set()

            conceptos_guardados = []

            for datos in conceptos_datos:

                numero = datos["numero"]

                numeros_recibidos.add(
                    numero
                )

                if numero in existentes_por_numero:

                    concepto = (
                        existentes_por_numero[
                            numero
                        ]
                    )

                    concepto.descripcion = (
                        datos["descripcion"]
                    )

                    concepto.unidad_medida = (
                        datos["unidad_medida"]
                    )

                    concepto.cantidad = (
                        datos["cantidad"]
                    )

                else:

                    concepto = ConceptoEstudio(
                        estudio_id=estudio_id,
                        numero=numero,
                        descripcion=(
                            datos["descripcion"]
                        ),
                        unidad_medida=(
                            datos["unidad_medida"]
                        ),
                        cantidad=(
                            datos["cantidad"]
                        )
                    )

                    sesion.add(
                        concepto
                    )

                conceptos_guardados.append(
                    concepto
                )

            # Si el usuario eliminó una fila,
            # eliminamos el concepto correspondiente
            for concepto in existentes:

                if (
                    concepto.numero
                    not in numeros_recibidos
                ):

                    sesion.delete(
                        concepto
                    )

            sesion.commit()

            # Aseguramos que tengan ID
            for concepto in conceptos_guardados:

                sesion.refresh(
                    concepto
                )

            return conceptos_guardados

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()