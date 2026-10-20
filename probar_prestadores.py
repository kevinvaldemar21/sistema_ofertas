from repositories.prestador_repository import (
    PrestadorRepository
)


def main():

    repository = PrestadorRepository()

    prestador = repository.crear(
        nombre_razon_social="PROVEEDOR EJEMPLO UNO",
        rfc="AAA010101AAA",
        telefono="0000000000",
        domicilio="DOMICILIO DE PRUEBA",
        registro_padron="REGISTRO DE PRUEBA"
    )

    print()
    print("Prestador creado correctamente.")
    print()
    print("ID:", prestador.id)
    print(
        "Nombre:",
        prestador.nombre_razon_social
    )
    print(
        "RFC:",
        prestador.rfc
    )


if __name__ == "__main__":
    main()