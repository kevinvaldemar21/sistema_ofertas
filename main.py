import sys

from PySide6.QtWidgets import (
    QApplication
)

from views.main_window import (
    MainWindow
)
from pathlib import Path

def cargar_estilos(app):

    base_dir = (
        Path(__file__)
        .resolve()
        .parent
    )

    ruta_estilo = (
        base_dir
        / "styles"
        / "main.qss"
    )

    if ruta_estilo.exists():

        with open(
            ruta_estilo,
            "r",
            encoding="utf-8"
        ) as archivo:

            app.setStyleSheet(
                archivo.read()
            )

def main():

    app = QApplication(
        sys.argv
    )

    cargar_estilos(
        app
    )

    ventana = MainWindow()

    ventana.show()

    sys.exit(
        app.exec()
    )



if __name__ == "__main__":

    main()