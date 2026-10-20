from PySide6.QtCore import Qt


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QGroupBox,
    QFormLayout
)

from repositories.cotizacion_repository import (
    CotizacionRepository
)

from views.evaluacion_prestadores import (
    EvaluacionPrestadoresView
)


class ComparativoView(QWidget):

    def __init__(
        self,
        estudio,
        ventana_anterior=None
    ):

        super().__init__()

        self.estudio = estudio
        self.ventana_anterior = ventana_anterior

        self.repository = (
            CotizacionRepository()
        )

        self.cotizaciones = []

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_datos()

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Comparativo de Cotizaciones"
        )

        self.resize(
            1400,
            750
        )

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout = QVBoxLayout()

        titulo = QLabel(
            "Comparativo de Cotizaciones"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout.addWidget(
            titulo
        )

        expediente = QLabel(
            f"Expediente: "
            f"{self.estudio.expediente}"
        )

        layout.addWidget(
            expediente
        )

        # ----------------------------------------------
        # TABLA
        # ----------------------------------------------

        self.tabla = QTableWidget()

        layout.addWidget(
            self.tabla
        )

        # ----------------------------------------------
        # RESUMEN
        # ----------------------------------------------

        self.layout_resumen = QHBoxLayout()

        layout.addLayout(
            self.layout_resumen
        )

        # ----------------------------------------------
        # RESULTADO
        # ----------------------------------------------

        self.label_resultado = QLabel()

        self.label_resultado.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        """)

        layout.addWidget(
            self.label_resultado
        )

        # ----------------------------------------------
        # BOTONES
        # ----------------------------------------------

        botones = QHBoxLayout()

        self.boton_volver = QPushButton(
            "Volver"
        )

        self.boton_continuar = QPushButton(
            "Continuar"
        )

        self.boton_volver.clicked.connect(
            self.volver
        )

        self.boton_continuar.clicked.connect(
            self.continuar
        )

        botones.addWidget(
            self.boton_volver
        )

        botones.addStretch()

        botones.addWidget(
            self.boton_continuar
        )

        layout.addLayout(
            botones
        )

        self.setLayout(
            layout
        )

    # ==================================================
    # CARGAR DATOS
    # ==================================================

    def cargar_datos(self):

        self.cotizaciones = (
            self.repository
            .obtener_por_estudio(
                self.estudio.id
            )
        )

        if not self.cotizaciones:

            QMessageBox.warning(
                self,
                "Sin cotizaciones",
                "No existen cotizaciones "
                "registradas para este estudio."
            )

            return

        # Usamos los detalles de la primera
        # cotización para obtener los conceptos.
        detalles_base = (
            self.repository
            .obtener_detalles(
                self.cotizaciones[0].id
            )
        )

        columnas = (
            3
            + len(self.cotizaciones)
        )

        self.tabla.setColumnCount(
            columnas
        )

        encabezados = [
            "No.",
            "Concepto",
            "Cantidad"
        ]

        for cotizacion in self.cotizaciones:

            encabezados.append(
                cotizacion
                .prestador
                .nombre_razon_social
            )

        self.tabla.setHorizontalHeaderLabels(
            encabezados
        )

        self.tabla.setRowCount(
            len(detalles_base)
        )

        # ----------------------------------------------
        # LLENAR FILAS
        # ----------------------------------------------

        for fila, detalle_base in enumerate(
            detalles_base
        ):

            concepto = (
                detalle_base.concepto
            )

            item_numero = QTableWidgetItem(
                str(concepto.numero)
            )

            item_concepto = QTableWidgetItem(
                concepto.descripcion
            )

            item_cantidad = QTableWidgetItem(
                f"{float(concepto.cantidad):g}"
            )

            for item in (
                item_numero,
                item_concepto,
                item_cantidad
            ):

                item.setFlags(
                    item.flags()
                    & ~Qt.ItemIsEditable
                )

            self.tabla.setItem(
                fila,
                0,
                item_numero
            )

            self.tabla.setItem(
                fila,
                1,
                item_concepto
            )

            self.tabla.setItem(
                fila,
                2,
                item_cantidad
            )

        # ----------------------------------------------
        # PRECIOS / IMPORTES
        # ----------------------------------------------

        for indice, cotizacion in enumerate(
            self.cotizaciones
        ):

            detalles = (
                self.repository
                .obtener_detalles(
                    cotizacion.id
                )
            )

            columna = (
                3 + indice
            )

            for fila, detalle in enumerate(
                detalles
            ):

                texto = (
                    f"P.U. ${float(detalle.precio_unitario):,.2f}\n"
                    f"Importe ${float(detalle.importe):,.2f}"
                )

                item = QTableWidgetItem(
                    texto
                )

                item.setFlags(
                    item.flags()
                    & ~Qt.ItemIsEditable
                )

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

        # ----------------------------------------------
        # TAMAÑO DE COLUMNAS
        # ----------------------------------------------

        header = (
            self.tabla.horizontalHeader()
        )

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        for columna in range(
            3,
            self.tabla.columnCount()
        ):

            header.setSectionResizeMode(
                columna,
                QHeaderView.ResizeToContents
            )

        self.tabla.resizeRowsToContents()

        # ----------------------------------------------
        # RESUMEN POR PROVEEDOR
        # ----------------------------------------------

        for cotizacion in self.cotizaciones:

            grupo = QGroupBox(
                cotizacion
                .prestador
                .nombre_razon_social
            )

            formulario = QFormLayout()

            formulario.addRow(
                "Subtotal:",
                QLabel(
                    f"${float(cotizacion.subtotal):,.2f}"
                )
            )

            formulario.addRow(
                f"IVA ({float(cotizacion.porcentaje_iva):g}%):",
                QLabel(
                    f"${float(cotizacion.iva):,.2f}"
                )
            )

            total = QLabel(
                f"${float(cotizacion.total):,.2f}"
            )

            total.setStyleSheet(
                "font-weight: bold;"
            )

            formulario.addRow(
                "Total:",
                total
            )

            grupo.setLayout(
                formulario
            )

            self.layout_resumen.addWidget(
                grupo
            )

        self.calcular_menor_total()

    # ==================================================
    # MENOR TOTAL
    # ==================================================

    def calcular_menor_total(self):

        if not self.cotizaciones:
            return

        menor = min(
            self.cotizaciones,
            key=lambda cotizacion: float(
                cotizacion.total
            )
        )

        self.cotizacion_menor = menor

        self.label_resultado.setText(
            "Menor importe total: "
            f"{menor.prestador.nombre_razon_social} "
            f"(${float(menor.total):,.2f})"
        )

    # ==================================================
    # CONTINUAR
    # ==================================================

    def continuar(self):

        if not self.cotizaciones:

            QMessageBox.warning(
                self,
                "Sin cotizaciones",
                "No existen cotizaciones "
                "para continuar."
            )

            return

        self.ventana_evaluacion = (
            EvaluacionPrestadoresView(
                estudio=self.estudio,
                cotizaciones=self.cotizaciones,
                ventana_anterior=self
            )
        )

        self.ventana_evaluacion.show()

        self.hide()

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:

            self.ventana_anterior.show()

        self.close()