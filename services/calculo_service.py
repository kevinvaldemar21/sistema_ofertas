class CalculoService:


    @staticmethod
    def calcular(
        cantidad,
        precio_unitario,
        porcentaje_iva
    ):


        importe = (
            cantidad *
            precio_unitario
        )


        iva = (
            importe *
            porcentaje_iva
        ) / 100


        total = (
            importe +
            iva
        )


        return {

            "importe": round(
                importe,
                2
            ),

            "iva": round(
                iva,
                2
            ),

            "total": round(
                total,
                2
            )
        }