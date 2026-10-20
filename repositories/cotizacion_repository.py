from sqlalchemy import select, delete

from database.conexion import obtener_sesion

from models.cotizacion import Cotizacion
from models.cotizacion_detalle import CotizacionDetalle

from sqlalchemy.orm import joinedload


class CotizacionRepository:

    def guardar_cotizaciones(
        self,
        estudio_id,
        prestadores,
        conceptos,
        precios,
        porcentaje_iva
    ):
        """
        Guarda o actualiza todas las cotizaciones
        correspondientes a un estudio.

        precios:
        {
            prestador_id: {
                concepto_id: precio_unitario
            }
        }
        """

        sesion = obtener_sesion()

        try:

            cotizaciones_guardadas = []

            # ==========================================
            # RECORRER PRESTADORES
            # ==========================================

            for orden, prestador in enumerate(
                prestadores,
                start=1
            ):

                # --------------------------------------
                # Buscar si ya existe cotización
                # --------------------------------------

                consulta = select(
                    Cotizacion
                ).where(
                    Cotizacion.estudio_id
                    == estudio_id,

                    Cotizacion.prestador_id
                    == prestador.id
                )

                cotizacion = sesion.scalar(
                    consulta
                )

                # --------------------------------------
                # Crear si no existe
                # --------------------------------------

                if cotizacion is None:

                    cotizacion = Cotizacion(
                        estudio_id=estudio_id,
                        prestador_id=prestador.id,
                        porcentaje_iva=porcentaje_iva,
                        subtotal=0,
                        iva=0,
                        total=0,
                        seleccionada=False
                    )

                    sesion.add(
                        cotizacion
                    )

                    sesion.flush()

                else:

                    cotizacion.porcentaje_iva = (
                        porcentaje_iva
                    )

                # --------------------------------------
                # Eliminar detalles anteriores
                #
                # Esto permite volver a guardar sin
                # duplicar precios.
                # --------------------------------------

                sesion.execute(
                    delete(
                        CotizacionDetalle
                    ).where(
                        CotizacionDetalle.cotizacion_id
                        == cotizacion.id
                    )
                )

                subtotal_cotizacion = 0

                # --------------------------------------
                # Crear detalles
                # --------------------------------------

                for concepto in conceptos:

                    precio_unitario = float(
                        precios[
                            prestador.id
                        ][
                            concepto.id
                        ]
                    )

                    cantidad = float(
                        concepto.cantidad
                    )

                    importe = (
                        cantidad
                        * precio_unitario
                    )

                    subtotal_cotizacion += (
                        importe
                    )

                    detalle = CotizacionDetalle(
                        cotizacion_id=cotizacion.id,
                        concepto_id=concepto.id,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        importe=importe
                    )

                    sesion.add(
                        detalle
                    )

                # --------------------------------------
                # TOTALES DEL PRESTADOR
                # --------------------------------------

                importe_iva = (
                    subtotal_cotizacion
                    * porcentaje_iva
                    / 100
                )

                total = (
                    subtotal_cotizacion
                    + importe_iva
                )

                cotizacion.subtotal = round(
                    subtotal_cotizacion,
                    2
                )

                cotizacion.iva = round(
                    importe_iva,
                    2
                )

                cotizacion.total = round(
                    total,
                    2
                )

                cotizaciones_guardadas.append(
                    cotizacion
                )

            # ==========================================
            # GUARDAR TODO EN UNA SOLA TRANSACCIÓN
            # ==========================================

            sesion.commit()

            return cotizaciones_guardadas

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()

    def obtener_por_estudio(
        self,
        estudio_id
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(Cotizacion)
                .options(
                    joinedload(
                        Cotizacion.prestador
                    )
                )
                .where(
                    Cotizacion.estudio_id
                    == estudio_id
                )
                .order_by(
                    Cotizacion.id
                )
            )

            return list(
                sesion.scalars(
                    consulta
                ).all()
            )

        finally:

            sesion.close()

    def obtener_detalles(
        self,
        cotizacion_id
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(CotizacionDetalle)
                .options(
                    joinedload(
                        CotizacionDetalle.concepto
                    )
                )
                .where(
                    CotizacionDetalle.cotizacion_id
                    == cotizacion_id
                )
                .order_by(
                    CotizacionDetalle.concepto_id
                )
            )

            return list(
                sesion.scalars(
                    consulta
                ).all()
            )

        finally:

            sesion.close()

    def seleccionar_cotizacion(
        self,
        estudio_id,
        cotizacion_id
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(Cotizacion)
                .where(
                    Cotizacion.estudio_id
                    == estudio_id
                )
            )

            cotizaciones = list(
                sesion.scalars(
                    consulta
                ).all()
            )

            encontrada = False

            for cotizacion in cotizaciones:

                if cotizacion.id == cotizacion_id:

                    cotizacion.seleccionada = True

                    encontrada = True

                else:

                    cotizacion.seleccionada = False

            if not encontrada:

                raise ValueError(
                    "La cotización seleccionada "
                    "no pertenece al estudio."
                )

            sesion.commit()

        except Exception:

            sesion.rollback()
            raise

        finally:

            sesion.close()

    def obtener_seleccionada(
        self,
        estudio_id
    ):

        sesion = obtener_sesion()

        try:

            consulta = (
                select(Cotizacion)
                .options(
                    joinedload(
                        Cotizacion.prestador
                    )
                )
                .where(
                    Cotizacion.estudio_id
                    == estudio_id,

                    Cotizacion.seleccionada
                    == True
                )
            )

            return sesion.scalar(
                consulta
            )

        finally:

            sesion.close()