from database.conexion import Base, engine

from models.area import Area
from models.proyecto import Proyecto

from models.prestador import Prestador
from models.estudio_mercado import EstudioMercado
from models.estudio_prestador import EstudioPrestador
from models.concepto_estudio import ConceptoEstudio
from models.cotizacion_detalle import CotizacionDetalle
from models.cotizacion import Cotizacion
from models.cotizacion_detalle import CotizacionDetalle

from models.condiciones_estudio import CondicionesEstudio

from models.evaluacion_prestador import (
    EvaluacionPrestador
)

from models.documento_generado import (
    DocumentoGenerado
)   

def crear_base_datos():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos creada correctamente.")