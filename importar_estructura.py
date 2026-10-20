from pathlib import Path

from services.estructura_service import EstructuraService


BASE_DIR = Path(__file__).resolve().parent

ARCHIVO = (
    BASE_DIR
    / "imports"
    / "Estructura Programatica DIF.xlsx"
)


def main():

    servicio = EstructuraService()

    try:

        resultado = servicio.importar_excel(
            ARCHIVO
        )

        print("=" * 45)
        print("IMPORTACIÓN TERMINADA CORRECTAMENTE")
        print("=" * 45)

        print(
            f"Registros leídos: "
            f"{resultado['registros_leidos']}"
        )

        print()

        print(
            f"Áreas creadas: "
            f"{resultado['areas_creadas']}"
        )

        print(
            f"Áreas actualizadas: "
            f"{resultado['areas_actualizadas']}"
        )

        print()

        print(
            f"Proyectos creados: "
            f"{resultado['proyectos_creados']}"
        )

        print(
            f"Proyectos actualizados: "
            f"{resultado['proyectos_actualizados']}"
        )

        print()

        print(
            f"Registros omitidos: "
            f"{resultado['registros_omitidos']}"
        )

        print("=" * 45)

    except FileNotFoundError as error:

        print()
        print("ERROR: No se encontró el archivo.")
        print(error)

    except Exception as error:

        print()
        print("Ocurrió un error durante la importación:")
        print(type(error).__name__)
        print(error)

    finally:

        servicio.cerrar()


if __name__ == "__main__":
    main()