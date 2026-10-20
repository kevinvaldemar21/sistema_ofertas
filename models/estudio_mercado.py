from datetime import date, datetime

from sqlalchemy import (
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.conexion import Base


class EstudioMercado(Base):
    __tablename__ = "estudios_mercado"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # --------------------------------------------------
    # REFERENCIAS
    # --------------------------------------------------

    area_id: Mapped[int] = mapped_column(
        ForeignKey("areas.id"),
        nullable=False
    )

    proyecto_id: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id"),
        nullable=False
    )

    # --------------------------------------------------
    # DATOS GENERALES
    # --------------------------------------------------

    fecha_elaboracion: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    expediente: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    partida_presupuestal: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    objeto_contratacion: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # --------------------------------------------------
    # COPIA HISTÓRICA DE DATOS PROGRAMÁTICOS
    # --------------------------------------------------

    codigo_dg: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    codigo_da: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    area_descripcion: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    codigo_proyecto: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    concepto_proyecto: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    responsable: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    cargo_responsable: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    # --------------------------------------------------
    # CONTROL
    # --------------------------------------------------

    estado: Mapped[str] = mapped_column(
        String(30),
        default="BORRADOR",
        nullable=False
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    # --------------------------------------------------
    # RELACIONES
    # --------------------------------------------------

    area = relationship(
        "Area"
    )

    proyecto = relationship(
        "Proyecto"
    )