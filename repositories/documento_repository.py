from sqlalchemy import select

from database.conexion import obtener_sesion

from datetime import datetime

from models.documento_generado import (
    DocumentoGenerado
)


class DocumentoRepository:

    def registrar(
        self,
        estudio_id,
        tipo_documento,
        nombre_archivo,
        ruta_relativa
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(DocumentoGenerado)
                .where(
                    DocumentoGenerado.estudio_id
                    == estudio_id,

                    DocumentoGenerado.tipo_documento
                    == tipo_documento
                )
            )

            documento = sesion.scalar(
                consulta
            )

            if documento is None:

                documento = DocumentoGenerado(
                    estudio_id=estudio_id,
                    tipo_documento=tipo_documento,
                    nombre_archivo=nombre_archivo,
                    ruta_relativa=ruta_relativa
                )

                sesion.add(
                    documento
                )

            else:

                documento.nombre_archivo = (
                    nombre_archivo
                )

                documento.ruta_relativa = (
                    ruta_relativa
                )

                

                documento.fecha_generacion = (
                    datetime.now()
                )

            sesion.commit()

            sesion.refresh(
                documento
            )

            return documento

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()

    # ==================================================
    # OBTENER DOCUMENTOS DE UN ESTUDIO
    # ==================================================

    def obtener_por_estudio(
        self,
        estudio_id
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(DocumentoGenerado)
                .where(
                    DocumentoGenerado.estudio_id
                    == estudio_id
                )
                .order_by(
                    DocumentoGenerado.fecha_generacion.desc()
                )
            )

            return list(
                sesion.scalars(
                    consulta
                )
            )

        finally:

            sesion.close()