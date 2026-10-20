from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.conexion import Base


class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    area_id: Mapped[int] = mapped_column(
        ForeignKey("areas.id"),
        nullable=False
    )

    numero_origen: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    codigo_proyecto: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    concepto: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    campo_h: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    campo_i: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    area = relationship(
        "Area",
        back_populates="proyectos"
    )