from datetime import datetime

from sqlalchemy import (
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
    Numeric,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.conexion import Base


class Cotizacion(Base):

    __tablename__ = "cotizaciones"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    estudio_id: Mapped[int] = mapped_column(
        ForeignKey(
            "estudios_mercado.id"
        ),
        nullable=False
    )


    prestador_id: Mapped[int] = mapped_column(
        ForeignKey(
            "prestadores.id"
        ),
        nullable=False
    )


    subtotal: Mapped[float] = mapped_column(
        Numeric(14,2),
        default=0
    )

    porcentaje_iva: Mapped[float] = mapped_column(
        Numeric(5,2),
        default=16,
        nullable=False
    )


    iva: Mapped[float] = mapped_column(
        Numeric(14,2),
        default=0
    )


    total: Mapped[float] = mapped_column(
        Numeric(14,2),
        default=0
    )


    observaciones: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    seleccionada: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )


    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )


    estudio = relationship(
        "EstudioMercado"
    )


    prestador = relationship(
        "Prestador"
    )