from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)
from PySide6.QtCore import Qt
from views.cotizaciones import CotizacionesView
from repositories.concepto_repository import ConceptoRepository
from views.cotizaciones import CotizacionesView

class ConceptosEstudioView(QWidget):

    def __init__(
        self,
        estudio,
        prestadores,
        ventana_anterior=None
    ):

        super().__init__()

        self.estudio = estudio
        self.prestadores = prestadores
        self.ventana_anterior = ventana_anterior
        self.concepto_repository = ConceptoRepository()

        self.configurar_ventana()
        self.crear_interfaz()

    def configurar_ventana(self):

        self.setWindowTitle(
            "Conceptos Requeridos"
        )

        self.resize(
            1000,
            650
        )

    def crear_interfaz(self):

        layout = QVBoxLayout()

        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        titulo = QLabel(
            "Conceptos o Servicios a Cotizar"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout.addWidget(titulo)

        expediente = QLabel(
            f"Expediente: "
            f"{self.estudio.expediente}"
        )

        layout.addWidget(expediente)

        # ----------------------------------------------
        # TABLA
        # ----------------------------------------------

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "N.P.",
            "Descripción",
            "Unidad de medida",
            "Cantidad"
        ])

        encabezado = (
            self.tabla.horizontalHeader()
        )

        encabezado.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        encabezado.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        encabezado.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        encabezado.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        layout.addWidget(
            self.tabla
        )

        # ----------------------------------------------
        # AGREGAR / QUITAR
        # ----------------------------------------------

        layout_edicion = QHBoxLayout()

        self.boton_agregar = QPushButton(
            "+ Agregar concepto"
        )

        self.boton_eliminar = QPushButton(
            "Eliminar concepto"
        )

        self.boton_agregar.clicked.connect(
            self.agregar_fila
        )

        self.boton_eliminar.clicked.connect(
            self.eliminar_fila
        )

        layout_edicion.addWidget(
            self.boton_agregar
        )

        layout_edicion.addWidget(
            self.boton_eliminar
        )

        layout_edicion.addStretch()

        layout.addLayout(
            layout_edicion
        )

        # ----------------------------------------------
        # BOTONES
        # ----------------------------------------------

        layout_botones = QHBoxLayout()

        self.boton_volver = QPushButton(
            "Volver"
        )

        self.boton_continuar = QPushButton(
            "Continuar a cotizaciones"
        )

        self.boton_volver.clicked.connect(
            self.volver
        )

        self.boton_continuar.clicked.connect(
            self.continuar
        )

        layout_botones.addWidget(
            self.boton_volver
        )

        layout_botones.addStretch()

        layout_botones.addWidget(
            self.boton_continuar
        )

        layout.addLayout(
            layout_botones
        )

        self.setLayout(layout)

        # Primera fila automáticamente
        self.agregar_fila()

    # ==================================================
    # FILAS
    # ==================================================

    def agregar_fila(self):

        fila = self.tabla.rowCount()

        self.tabla.insertRow(fila)

        numero = QTableWidgetItem(
            str(fila + 1)
        )

        numero.setFlags(
            numero.flags()
            & ~Qt.ItemIsEditable
        )

        self.tabla.setItem(
            fila,
            0,
            numero
        )

        self.tabla.setItem(
            fila,
            1,
            QTableWidgetItem("")
        )

        self.tabla.setItem(
            fila,
            2,
            QTableWidgetItem("")
        )

        self.tabla.setItem(
            fila,
            3,
            QTableWidgetItem("1")
        )

    def eliminar_fila(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            return

        self.tabla.removeRow(
            fila
        )

        self.renumerar()

    def renumerar(self):

        for fila in range(
            self.tabla.rowCount()
        ):

            self.tabla.setItem(
                fila,
                0,
                QTableWidgetItem(
                    str(fila + 1)
                )
            )

    # ==================================================
    # VALIDACIÓN
    # ==================================================

    def obtener_datos(self):

        conceptos = []

        for fila in range(
            self.tabla.rowCount()
        ):

            descripcion_item = (
                self.tabla.item(
                    fila,
                    1
                )
            )

            unidad_item = (
                self.tabla.item(
                    fila,
                    2
                )
            )

            cantidad_item = (
                self.tabla.item(
                    fila,
                    3
                )
            )

            descripcion = (
                descripcion_item.text().strip()
                if descripcion_item
                else ""
            )

            unidad = (
                unidad_item.text().strip()
                if unidad_item
                else ""
            )

            cantidad_texto = (
                cantidad_item.text().strip()
                if cantidad_item
                else ""
            )

            if not descripcion:

                QMessageBox.warning(
                    self,
                    "Dato requerido",
                    f"Ingrese la descripción "
                    f"del concepto {fila + 1}."
                )

                return None

            if not unidad:

                QMessageBox.warning(
                    self,
                    "Dato requerido",
                    f"Ingrese la unidad de medida "
                    f"del concepto {fila + 1}."
                )

                return None

            try:

                cantidad = float(
                    cantidad_texto
                )

            except ValueError:

                QMessageBox.warning(
                    self,
                    "Cantidad inválida",
                    f"La cantidad del concepto "
                    f"{fila + 1} no es válida."
                )

                return None

            if cantidad <= 0:

                QMessageBox.warning(
                    self,
                    "Cantidad inválida",
                    "La cantidad debe ser "
                    "mayor que cero."
                )

                return None

            conceptos.append({
                "numero": fila + 1,
                "descripcion": descripcion,
                "unidad_medida": unidad,
                "cantidad": cantidad
            })

        self.conceptos_capturados = conceptos

        return conceptos

    def continuar(self):

        conceptos_datos = self.obtener_datos()

        if conceptos_datos is None:
            return

        if len(conceptos_datos) == 0:

            QMessageBox.warning(
                self,
                "Conceptos requeridos",
                "Debe agregar al menos un concepto."
            )

            return

        try:

            conceptos_guardados = (
                self.concepto_repository.guardar_lista(
                    estudio_id=self.estudio.id,
                    conceptos_datos=conceptos_datos
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible guardar "
                "los conceptos.\n\n"
                f"{error}"
            )

            return

        self.ventana_cotizaciones = CotizacionesView(
            estudio=self.estudio,
            conceptos=conceptos_guardados,
            prestadores=self.prestadores,
            ventana_anterior=self
        )

        self.ventana_cotizaciones.show()

        self.hide()

    def volver(self):

        if self.ventana_anterior:
            self.ventana_anterior.show()

        self.close()