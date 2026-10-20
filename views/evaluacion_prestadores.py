from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QGridLayout,
    QComboBox,
    QMessageBox
)

from repositories.evaluacion_repository import (
    EvaluacionRepository
)


class EvaluacionPrestadoresView(QWidget):

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
            EvaluacionRepository()
        )

        self.controles = {}

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_evaluaciones()

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Evaluación de Prestadores"
        )

        self.resize(
            1000,
            600
        )

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout()

        titulo = QLabel(
            "Evaluación de Prestadores"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout_principal.addWidget(
            titulo
        )

        expediente = QLabel(
            f"Expediente: "
            f"{self.estudio.expediente}"
        )

        layout_principal.addWidget(
            expediente
        )

        descripcion = QLabel(
            "Indique si cada prestador cumple "
            "con los criterios de cantidad, "
            "calidad y oportunidad."
        )

        descripcion.setWordWrap(
            True
        )

        layout_principal.addWidget(
            descripcion
        )

        # ----------------------------------------------
        # TABLA DE EVALUACIÓN
        # ----------------------------------------------

        grupo = QGroupBox(
            "Criterios"
        )

        grid = QGridLayout()

        grid.addWidget(
            QLabel("<b>Prestador</b>"),
            0,
            0
        )

        grid.addWidget(
            QLabel("<b>Cantidad</b>"),
            0,
            1
        )

        grid.addWidget(
            QLabel("<b>Calidad</b>"),
            0,
            2
        )

        grid.addWidget(
            QLabel("<b>Oportunidad</b>"),
            0,
            3
        )

        for fila, cotizacion in enumerate(
            self.cotizaciones,
            start=1
        ):

            prestador = (
                cotizacion.prestador
            )

            nombre = QLabel(
                prestador.nombre_razon_social
            )

            nombre.setWordWrap(
                True
            )

            combo_cantidad = (
                self.crear_combo()
            )

            combo_calidad = (
                self.crear_combo()
            )

            combo_oportunidad = (
                self.crear_combo()
            )

            grid.addWidget(
                nombre,
                fila,
                0
            )

            grid.addWidget(
                combo_cantidad,
                fila,
                1
            )

            grid.addWidget(
                combo_calidad,
                fila,
                2
            )

            grid.addWidget(
                combo_oportunidad,
                fila,
                3
            )

            self.controles[
                prestador.id
            ] = {
                "cantidad": combo_cantidad,
                "calidad": combo_calidad,
                "oportunidad": combo_oportunidad
            }

        grupo.setLayout(
            grid
        )

        layout_principal.addWidget(
            grupo
        )

        # ----------------------------------------------
        # BOTONES
        # ----------------------------------------------

        layout_botones = QHBoxLayout()

        boton_volver = QPushButton(
            "Volver"
        )

        boton_continuar = QPushButton(
            "Guardar y continuar"
        )

        boton_volver.setMinimumSize(
            130,
            40
        )

        boton_continuar.setMinimumSize(
            170,
            40
        )

        boton_volver.clicked.connect(
            self.volver
        )

        boton_continuar.clicked.connect(
            self.guardar
        )

        layout_botones.addWidget(
            boton_volver
        )

        layout_botones.addStretch()

        layout_botones.addWidget(
            boton_continuar
        )

        layout_principal.addLayout(
            layout_botones
        )

        self.setLayout(
            layout_principal
        )

    # ==================================================
    # COMBO
    # ==================================================

    def crear_combo(self):

        combo = QComboBox()

        combo.addItem(
            "Sí",
            True
        )

        combo.addItem(
            "No",
            False
        )

        return combo

    # ==================================================
    # CARGAR EVALUACIONES EXISTENTES
    # ==================================================

    def cargar_evaluaciones(self):

        evaluaciones = (
            self.repository
            .obtener_por_estudio(
                self.estudio.id
            )
        )

        for evaluacion in evaluaciones:

            controles = (
                self.controles.get(
                    evaluacion.prestador_id
                )
            )

            if controles is None:
                continue

            self.seleccionar_valor(
                controles["cantidad"],
                evaluacion.cumple_cantidad
            )

            self.seleccionar_valor(
                controles["calidad"],
                evaluacion.cumple_calidad
            )

            self.seleccionar_valor(
                controles["oportunidad"],
                evaluacion.cumple_oportunidad
            )

    # ==================================================
    # SELECCIONAR VALOR DEL COMBO
    # ==================================================

    @staticmethod
    def seleccionar_valor(
        combo,
        valor
    ):

        indice = combo.findData(
            bool(valor)
        )

        if indice >= 0:

            combo.setCurrentIndex(
                indice
            )

    # ==================================================
    # GUARDAR
    # ==================================================

    def guardar(self):

        try:

            for cotizacion in self.cotizaciones:

                prestador = (
                    cotizacion.prestador
                )

                controles = (
                    self.controles[
                        prestador.id
                    ]
                )

                cantidad = (
                    controles["cantidad"]
                    .currentData()
                )

                calidad = (
                    controles["calidad"]
                    .currentData()
                )

                oportunidad = (
                    controles["oportunidad"]
                    .currentData()
                )

                self.repository.guardar(
                    estudio_id=self.estudio.id,
                    prestador_id=prestador.id,
                    cumple_cantidad=cantidad,
                    cumple_calidad=calidad,
                    cumple_oportunidad=oportunidad
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible guardar "
                "la evaluación.\n\n"
                f"{error}"
            )

            return

        QMessageBox.information(
            self,
            "Evaluación guardada",
            "La evaluación de los prestadores "
            "fue guardada correctamente."
        )

        self.abrir_seleccion()

    # ==================================================
    # SELECCIÓN DEL PRESTADOR
    # ==================================================

    def abrir_seleccion(self):

        from views.seleccion_prestador import (
            SeleccionPrestadorView
        )

        self.ventana_seleccion = (
            SeleccionPrestadorView(
                estudio=self.estudio,
                cotizaciones=self.cotizaciones,
                ventana_anterior=self
            )
        )

        self.ventana_seleccion.show()

        self.hide()

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:

            self.ventana_anterior.show()

        self.close()