from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.conexion import Base


class DocumentoGenerado(Base):

    __tablename__ = "documentos_generados"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    estudio_id: Mapped[int] = mapped_column(
        ForeignKey("estudios_mercado.id"),
        nullable=False
    )

    tipo_documento: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ESTUDIO_MERCADO"
    )

    nombre_archivo: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ruta_relativa: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    fecha_generacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now
    )

    estudio = relationship(
        "EstudioMercado"
    )