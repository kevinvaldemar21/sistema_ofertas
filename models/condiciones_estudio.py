from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.conexion import Base


class CondicionesEstudio(Base):

    __tablename__ = "condiciones_estudio"

    __table_args__ = (
        UniqueConstraint(
            "estudio_id",
            name="uq_condiciones_estudio"
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

    lugar_entrega: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    plazo_entrega: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    forma_pago: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    vigencia_cotizacion: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    estudio = relationship(
        "EstudioMercado"
    )

    tipo_procedimiento: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )