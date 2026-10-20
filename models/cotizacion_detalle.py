from sqlalchemy import (
    Integer,
    Numeric,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.conexion import Base


class CotizacionDetalle(Base):

    __tablename__ = "cotizaciones_detalle"

    __table_args__ = (
        UniqueConstraint(
            "cotizacion_id",
            "concepto_id",
            name="uq_cotizacion_concepto"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("cotizaciones.id"),
        nullable=False
    )

    concepto_id: Mapped[int] = mapped_column(
        ForeignKey("conceptos_estudio.id"),
        nullable=False
    )

    cantidad: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    precio_unitario: Mapped[float] = mapped_column(
        Numeric(14, 2),
        nullable=False
    )

    importe: Mapped[float] = mapped_column(
        Numeric(14, 2),
        nullable=False
    )

    cotizacion = relationship(
        "Cotizacion"
    )

    concepto = relationship(
        "ConceptoEstudio"
    )   