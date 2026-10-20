from sqlalchemy import (
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.conexion import Base


class EvaluacionPrestador(Base):

    __tablename__ = "evaluaciones_prestadores"

    __table_args__ = (
        UniqueConstraint(
            "estudio_id",
            "prestador_id",
            name="uq_evaluacion_estudio_prestador"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    estudio_id: Mapped[int] = mapped_column(
        ForeignKey("estudios_mercado.id"),
        nullable=False
    )

    prestador_id: Mapped[int] = mapped_column(
        ForeignKey("prestadores.id"),
        nullable=False
    )

    cumple_cantidad: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    cumple_calidad: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    cumple_oportunidad: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    estudio = relationship(
        "EstudioMercado"
    )

    prestador = relationship(
        "Prestador"
    )