from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from database.conexion import Base


class ConceptoEstudio(Base):
    __tablename__ = "conceptos_estudio"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    estudio_id: Mapped[int] = mapped_column(
        ForeignKey("estudios_mercado.id"),
        nullable=False
    )

    numero: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    unidad_medida: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    cantidad: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    estudio = relationship(
        "EstudioMercado"
    )

    