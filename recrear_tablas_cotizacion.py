from database.conexion import engine

from models.area import Area
from models.proyecto import Proyecto
from models.prestador import Prestador
from models.estudio_mercado import EstudioMercado
from models.estudio_prestador import EstudioPrestador
from models.concepto_estudio import ConceptoEstudio
from models.cotizacion import Cotizacion
from models.cotizacion_detalle import CotizacionDetalle


def main():

    print("Recreando tablas de cotización...")

    CotizacionDetalle.__table__.drop(
        engine,
        checkfirst=True
    )

    Cotizacion.__table__.drop(
        engine,
        checkfirst=True
    )

    Cotizacion.__table__.create(
        engine,
        checkfirst=True
    )

    CotizacionDetalle.__table__.create(
        engine,
        checkfirst=True
    )

    print(
        "Tablas de cotización recreadas correctamente."
    )


if __name__ == "__main__":
    main()