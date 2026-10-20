from sqlalchemy import select

from database.conexion import obtener_sesion
from models.estudio_mercado import EstudioMercado
from models.estudio_prestador import EstudioPrestador

from datetime import datetime

class EstudioRepository:
    
    def obtener_todos(self, solo_activos=True):
        sesion = obtener_sesion()

        try:
            consulta = select(EstudioMercado)

            if solo_activos:
                consulta = consulta.where(
                    EstudioMercado.activo.is_(True)
                )

            consulta = consulta.order_by(
                EstudioMercado.fecha_elaboracion.desc(),
                EstudioMercado.id.desc()
            )

            return list(sesion.scalars(consulta))

        finally:
            sesion.close()
    
    
    def existe_expediente(self, expediente):

        sesion = obtener_sesion()

        try:

            consulta = select(
                EstudioMercado
            ).where(
                EstudioMercado.expediente == expediente
            )

            return (
                sesion.scalar(
                    consulta
                )
                is not None
            )

        finally:
            sesion.close()

    def crear(
        self,
        area,
        proyecto,
        fecha_elaboracion,
        expediente,
        partida_presupuestal,
        objeto_contratacion
    ):

        sesion = obtener_sesion()

        expediente = expediente.strip()

        if self.existe_expediente(
            expediente
        ):

            raise ValueError(
                f"Ya existe un proceso con el expediente "
                f"'{expediente}'."
            )
        
        try:

            estudio = EstudioMercado(

                # Relaciones
                area_id=area.id,
                proyecto_id=proyecto.id,

                # Datos generales
                fecha_elaboracion=fecha_elaboracion,
                expediente=expediente,
                partida_presupuestal=partida_presupuestal,
                objeto_contratacion=objeto_contratacion,

                # Copia histórica
                codigo_dg=area.codigo_dg,
                codigo_da=area.codigo_da,
                area_descripcion=area.descripcion,

                codigo_proyecto=(
                    proyecto.codigo_proyecto
                ),

                concepto_proyecto=(
                    proyecto.concepto
                ),

                responsable=area.responsable,

                cargo_responsable=(
                    area.cargo_responsable
                ),

                estado="BORRADOR",
                activo=True
            )

            sesion.add(
                estudio
            )

            sesion.commit()

            sesion.refresh(
                estudio
            )

            return estudio

        except Exception:

            sesion.rollback()
            raise

        finally:
            sesion.close()

    def agregar_prestadores(
        self,
        estudio_id,
        prestadores
    ):

        sesion = obtener_sesion()

        try:

            for orden, prestador in enumerate(
                prestadores,
                start=1
            ):

                relacion = EstudioPrestador(
                    estudio_id=estudio_id,
                    prestador_id=prestador.id,
                    orden=orden
                )

                sesion.add(relacion)

            sesion.commit()

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()

    def finalizar(
        self,
        estudio_id
    ):

        sesion = obtener_sesion()

        try:

            estudio = sesion.get(
                EstudioMercado,
                estudio_id
            )

            if estudio is None:

                raise ValueError(
                    "No se encontró el estudio."
                )

            estudio.estado = "FINALIZADO"

            estudio.fecha_actualizacion = (
                datetime.now()
            )

            sesion.commit()

            return True

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()

    
    def obtener_por_id(self, estudio_id):

        sesion = obtener_sesion()

        try:
            return sesion.get(
                EstudioMercado,
                estudio_id
            )

        finally:
            sesion.close()
