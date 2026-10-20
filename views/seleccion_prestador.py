from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QMessageBox
)

from repositories.cotizacion_repository import (
    CotizacionRepository
)

from views.condiciones_estudio import (
    CondicionesEstudioView
)

class SeleccionPrestadorView(QWidget):

    def __init__(
        self,
        estudio,
        cotizaciones,
        ventana_anterior=None
    ):

        super().__init__()

        self.estudio = estudio
        self.cotizaciones = cotizaciones
        self.ventana_anterior = ventana_anterior

        self.repository = (
            CotizacionRepository()
        )

        self.radio_group = QButtonGroup(
            self
        )

        self.configurar_ventana()
        self.crear_interfaz()

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Selección de Prestador"
        )

        self.resize(
            900,
            600
        )

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout = QVBoxLayout()

        titulo = QLabel(
            "Selección del Prestador"
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

        instruccion = QLabel(
            "Seleccione el prestador que "
            "cumple con las condiciones "
            "requeridas para el proceso."
        )

        instruccion.setWordWrap(
            True
        )

        layout.addWidget(
            instruccion
        )

        # ==============================================
        # COTIZACIONES
        # ==============================================

        for cotizacion in self.cotizaciones:

            prestador = (
                cotizacion.prestador
            )

            grupo = QGroupBox(
                prestador.nombre_razon_social
            )

            layout_grupo = QVBoxLayout()

            radio = QRadioButton(
                "Seleccionar este prestador"
            )

            self.radio_group.addButton(
                radio,
                cotizacion.id
            )

            layout_grupo.addWidget(
                radio
            )

            datos = QLabel(
                f"RFC: "
                f"{prestador.rfc or '-'}\n"
                f"Teléfono: "
                f"{prestador.telefono or '-'}\n"
                f"Subtotal: "
                f"${float(cotizacion.subtotal):,.2f}\n"
                f"IVA: "
                f"${float(cotizacion.iva):,.2f}\n"
                f"Total: "
                f"${float(cotizacion.total):,.2f}"
            )

            layout_grupo.addWidget(
                datos
            )

            grupo.setLayout(
                layout_grupo
            )

            layout.addWidget(
                grupo
            )

        # ==============================================
        # BOTONES
        # ==============================================

        botones = QHBoxLayout()

        boton_volver = QPushButton(
            "Volver"
        )

        boton_confirmar = QPushButton(
            "Confirmar selección"
        )

        boton_volver.clicked.connect(
            self.volver
        )

        boton_confirmar.clicked.connect(
            self.confirmar
        )

        botones.addWidget(
            boton_volver
        )

        botones.addStretch()

        botones.addWidget(
            boton_confirmar
        )

        layout.addLayout(
            botones
        )

        self.setLayout(
            layout
        )

    # ==================================================
    # CONFIRMAR
    # ==================================================

    def confirmar(self):

        cotizacion_id = (
            self.radio_group.checkedId()
        )

        if cotizacion_id == -1:

            QMessageBox.warning(
                self,
                "Prestador requerido",
                "Debe seleccionar un prestador."
            )

            return

        cotizacion = next(
            (
                cot
                for cot in self.cotizaciones
                if cot.id == cotizacion_id
            ),
            None
        )

        if cotizacion is None:
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar selección",
            "¿Desea seleccionar a:\n\n"
            f"{cotizacion.prestador.nombre_razon_social}\n\n"
            f"Total cotizado: "
            f"${float(cotizacion.total):,.2f}?"
        )

        if respuesta != QMessageBox.Yes:
            return

        try:

            self.repository.seleccionar_cotizacion(
                estudio_id=self.estudio.id,
                cotizacion_id=cotizacion.id
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible guardar "
                "la selección.\n\n"
                f"{error}"
            )

            return

        QMessageBox.information(
            self,
            "Prestador seleccionado",
            "La selección fue guardada "
            "correctamente."
        )

        self.ventana_condiciones = (
            CondicionesEstudioView(
                estudio=self.estudio,
                cotizacion_seleccionada=cotizacion,
                ventana_anterior=self
            )
        )

        self.ventana_condiciones.show()

        self.hide()

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:

            self.ventana_anterior.show()

        self.close()