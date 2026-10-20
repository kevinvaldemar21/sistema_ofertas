from PySide6.QtCore import (
    Qt,
    Signal
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QAbstractItemView
)


class EvaluacionesView(QWidget):

    # ==================================================
    # SEÑALES
    # ==================================================

    nueva_evaluacion_solicitada = Signal()

    ver_evaluacion_solicitada = Signal(
        int
    )

    # ==================================================
    # INICIALIZACIÓN
    # ==================================================

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.registros = []

        self.crear_interfaz()

        self.cargar_registros(
            [
            ]
        )

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout(
            self
        )

        layout_principal.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout_principal.setSpacing(
            0
        )

        # ==============================================
        # ENCABEZADO
        # ==============================================

        encabezado = QHBoxLayout()

        encabezado.setSpacing(
            20
        )

        bloque_titulo = QVBoxLayout()

        bloque_titulo.setSpacing(
            4
        )

        titulo = QLabel(
            "Evaluaciones de ofertas"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        descripcion = QLabel(
            "Consulte y administre los procesos "
            "de evaluación de ofertas registrados."
        )

        descripcion.setObjectName(
            "descripcionPagina"
        )

        descripcion.setWordWrap(
            True
        )

        bloque_titulo.addWidget(
            titulo
        )

        bloque_titulo.addWidget(
            descripcion
        )

        encabezado.addLayout(
            bloque_titulo,
            1
        )

        self.boton_nueva = QPushButton(
            "+  Nueva evaluación"
        )

        self.boton_nueva.setObjectName(
            "botonPrimario"
        )

        self.boton_nueva.setMinimumSize(
            185,
            44
        )

        self.boton_nueva.setCursor(
            Qt.PointingHandCursor
        )

        self.boton_nueva.clicked.connect(
            self.nueva_evaluacion_solicitada.emit
        )

        encabezado.addWidget(
            self.boton_nueva,
            alignment=Qt.AlignTop
        )

        layout_principal.addLayout(
            encabezado
        )

        layout_principal.addSpacing(
            28
        )

        # ==============================================
        # FILTROS
        # ==============================================

        contenedor_filtros = QFrame()

        contenedor_filtros.setObjectName(
            "contenedorFiltros"
        )

        layout_filtros = QHBoxLayout(
            contenedor_filtros
        )

        layout_filtros.setContentsMargins(
            18,
            16,
            18,
            16
        )

        layout_filtros.setSpacing(
            14
        )

        # ----------------------------------------------
        # BÚSQUEDA
        # ----------------------------------------------

        self.input_busqueda = QLineEdit()

        self.input_busqueda.setObjectName(
            "inputBusqueda"
        )

        self.input_busqueda.setPlaceholderText(
            "Buscar por expediente, área o responsable..."
        )

        self.input_busqueda.setClearButtonEnabled(
            True
        )

        self.input_busqueda.setMinimumHeight(
            40
        )

        # ----------------------------------------------
        # ESTADO
        # ----------------------------------------------

        self.combo_estado = QComboBox()

        self.combo_estado.setObjectName(
            "comboFiltro"
        )

        self.combo_estado.setMinimumHeight(
            40
        )

        self.combo_estado.setMinimumWidth(
            170
        )

        self.combo_estado.addItems(
            [
                "Todos los estados",
                "BORRADOR",
                "FINALIZADO"
            ]
        )

        layout_filtros.addWidget(
            self.input_busqueda,
            1
        )

        layout_filtros.addWidget(
            self.combo_estado
        )

        layout_principal.addWidget(
            contenedor_filtros
        )

        layout_principal.addSpacing(
            20
        )

        # ==============================================
        # TABLA
        # ==============================================

        self.tabla = QTableWidget()

        self.tabla.setObjectName(
            "tablaEvaluaciones"
        )

        self.tabla.setColumnCount(
            6
        )

        self.tabla.setHorizontalHeaderLabels(
            [
                "Expediente",
                "Fecha",
                "Área",
                "Responsable",
                "Estado",
                "Acciones"
            ]
        )

        self.tabla.setAlternatingRowColors(
            False
        )

        self.tabla.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.tabla.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.tabla.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.tabla.setShowGrid(
            False
        )

        self.tabla.verticalHeader().setVisible(
            False
        )

        self.tabla.verticalHeader().setDefaultSectionSize(
            56
        )

        header = (
            self.tabla.horizontalHeader()
        )

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.Fixed
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.Fixed
        )

        self.tabla.setColumnWidth(
            4,
            125
        )

        self.tabla.setColumnWidth(
            5,
            145
        )

        layout_principal.addWidget(
            self.tabla,
            1
        )

        # ==============================================
        # EVENTOS DE FILTRO
        # ==============================================

        self.input_busqueda.textChanged.connect(
            self.aplicar_filtros
        )

        self.combo_estado.currentTextChanged.connect(
            self.aplicar_filtros
        )

    # ==================================================
    # CARGAR REGISTROS
    # ==================================================

    def cargar_registros(
        self,
        registros
    ):

        self.registros = registros

        self.aplicar_filtros()

    # ==================================================
    # FILTROS
    # ==================================================

    def aplicar_filtros(self):

        texto = (
            self.input_busqueda
            .text()
            .strip()
            .lower()
        )

        estado = (
            self.combo_estado
            .currentText()
        )

        registros_filtrados = []

        for registro in self.registros:

            expediente = str(
                registro.get(
                    "expediente",
                    ""
                )
            )

            area = str(
                registro.get(
                    "area",
                    ""
                )
            )

            responsable = str(
                registro.get(
                    "responsable",
                    ""
                )
            )

            estado_registro = str(
                registro.get(
                    "estado",
                    ""
                )
            )

            coincide_texto = (
                texto == ""
                or texto in expediente.lower()
                or texto in area.lower()
                or texto in responsable.lower()
            )

            coincide_estado = (
                estado == "Todos los estados"
                or estado_registro == estado
            )

            if (
                coincide_texto
                and coincide_estado
            ):

                registros_filtrados.append(
                    registro
                )

        self.mostrar_registros(
            registros_filtrados
        )

    # ==================================================
    # MOSTRAR REGISTROS
    # ==================================================

    def mostrar_registros(
        self,
        registros
    ):

        self.tabla.setRowCount(
            0
        )

        for registro in registros:

            fila = (
                self.tabla.rowCount()
            )

            self.tabla.insertRow(
                fila
            )

            # ------------------------------------------
            # EXPEDIENTE
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                0,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "expediente",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # FECHA
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                1,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "fecha",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # ÁREA
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                2,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "area",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # PROYECTO
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                3,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "responsable",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # ESTADO
            # ------------------------------------------

            valor_estado = str(
                registro.get(
                    "estado",
                    ""
                )
            )

            contenedor_estado = QWidget()

            layout_estado = QHBoxLayout(
                contenedor_estado
            )

            layout_estado.setContentsMargins(
                8,
                6,
                8,
                6
            )

            layout_estado.setAlignment(
                Qt.AlignCenter
            )

            etiqueta_estado = QLabel(
                valor_estado
            )

            etiqueta_estado.setObjectName(
                "etiquetaEstado"
            )

            etiqueta_estado.setProperty(
                "estado",
                valor_estado
            )

            etiqueta_estado.setAlignment(
                Qt.AlignCenter
            )

            etiqueta_estado.setMinimumWidth(
                90
            )

            etiqueta_estado.setMinimumHeight(
                30
            )

            layout_estado.addWidget(
                etiqueta_estado
            )

            self.tabla.setCellWidget(
                fila,
                4,
                contenedor_estado
            )

            # ------------------------------------------
            # ACCIONES
            # ------------------------------------------

            contenedor_acciones = QWidget()

            layout_acciones = QHBoxLayout(
                contenedor_acciones
            )

            layout_acciones.setContentsMargins(
                8,
                5,
                8,
                5
            )

            layout_acciones.setAlignment(
                Qt.AlignCenter
            )

            boton_ver = QPushButton(
                "Ver evaluación"
            )

            boton_ver.setObjectName(
                "botonTabla"
            )

            boton_ver.setCursor(
                Qt.PointingHandCursor
            )

            boton_ver.setMinimumWidth(
                110
            )

            boton_ver.setMinimumHeight(
                32
            )

            estudio_id = registro.get(
                "id"
            )

            boton_ver.clicked.connect(
                lambda checked=False,
                id_estudio=estudio_id:
                self.ver_evaluacion_solicitada.emit(
                    id_estudio
                )
            )

            layout_acciones.addWidget(
                boton_ver
            )

            self.tabla.setCellWidget(
                fila,
                5,
                contenedor_acciones
            )