from sqlalchemy import text

from database.conexion import engine


with engine.begin() as conexion:

    columnas = conexion.execute(
        text(
            "PRAGMA table_info(condiciones_estudio)"
        )
    ).fetchall()

    nombres_columnas = [
        columna[1]
        for columna in columnas
    ]

    if "tipo_procedimiento" not in nombres_columnas:

        conexion.execute(
            text("""
                ALTER TABLE condiciones_estudio
                ADD COLUMN tipo_procedimiento VARCHAR(255)
            """)
        )

        print(
            "Columna tipo_procedimiento agregada correctamente."
        )

    else:

        print(
            "La columna tipo_procedimiento ya existe."
        )