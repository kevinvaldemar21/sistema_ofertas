from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from database.conexion import Base


class Prestador(Base):
    __tablename__ = "prestadores"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre_razon_social: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    rfc: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    domicilio: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    registro_padron: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )