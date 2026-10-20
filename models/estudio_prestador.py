from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class EstudioPrestador(Base):
    __tablename__ = "estudio_prestadores"

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

    orden: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    estudio = relationship(
        "EstudioMercado"
    )

    prestador = relationship(
        "Prestador"
    )