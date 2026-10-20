from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class Area(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    codigo_dg: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    codigo_da: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        String(255),
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

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    proyectos = relationship(
        "Proyecto",
        back_populates="area",
        cascade="all, delete-orphan"
    )