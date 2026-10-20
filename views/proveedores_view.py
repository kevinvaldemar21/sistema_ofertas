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
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox
)

from repositories.prestador_repository import PrestadorRepository


class ProveedoresView(QWidget):

    # ==================================================
    # SEÑALES
    # ==================================================

    nuevo_proveedor_solicitado = Signal()

    ver_proveedor_solicitado = Signal(
        int
    )

    editar_proveedor_solicitado = Signal(
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

        self.cargar_registros()

        # ==============================================
        # DATOS TEMPORALES DE PRUEBA
        # ==============================================
        # Se eliminarán cuando conectemos SQLite.



    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout(
            self
        )

        # MainWindow ya controla los márgenes generales.
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
            "Proveedores"
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        descripcion = QLabel(
            "Consulte y administre los proveedores "
            "registrados en el sistema."
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

        # ----------------------------------------------
        # NUEVO PROVEEDOR
        # ----------------------------------------------

        self.boton_nuevo = QPushButton(
            "+  Nuevo proveedor"
        )

        self.boton_nuevo.setObjectName(
            "botonPrimario"
        )

        self.boton_nuevo.setMinimumSize(
            185,
            44
        )

        self.boton_nuevo.setCursor(
            Qt.PointingHandCursor
        )

        self.boton_nuevo.clicked.connect(
            self.nuevo_proveedor_solicitado.emit
        )

        encabezado.addWidget(
            self.boton_nuevo,
            alignment=Qt.AlignTop
        )

        layout_principal.addLayout(
            encabezado
        )

        layout_principal.addSpacing(
            28
        )

        # ==============================================
        # BÚSQUEDA
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

        self.input_busqueda = QLineEdit()

        self.input_busqueda.setObjectName(
            "inputBusqueda"
        )

        self.input_busqueda.setPlaceholderText(
            "Buscar por nombre, RFC o registro en padrón..."
        )

        self.input_busqueda.setClearButtonEnabled(
            True
        )

        self.input_busqueda.setMinimumHeight(
            40
        )

        layout_filtros.addWidget(
            self.input_busqueda
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
            "tablaProveedores"
        )

        self.tabla.setColumnCount(
            5
        )

        self.tabla.setHorizontalHeaderLabels(
            [
                "Proveedor",
                "RFC",
                "Teléfono",
                "Registro en padrón",
                "Acciones"
            ]
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

        self.tabla.setAlternatingRowColors(
            False
        )

        self.tabla.verticalHeader().setVisible(
            False
        )

        self.tabla.verticalHeader().setDefaultSectionSize(
            56
        )

        # ==============================================
        # TAMAÑOS DE COLUMNAS
        # ==============================================

        header = (
            self.tabla.horizontalHeader()
        )

        # Proveedor
        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        # RFC
        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        # Teléfono
        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        # Registro padrón
        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        # Acciones
        header.setSectionResizeMode(
            4,
            QHeaderView.Fixed
        )

        self.tabla.setColumnWidth(
            4,
            190
        )

        layout_principal.addWidget(
            self.tabla,
            1
        )

        # ==============================================
        # EVENTOS
        # ==============================================

        self.input_busqueda.textChanged.connect(
            self.aplicar_filtro
        )

    # ==================================================
    # CARGAR REGISTROS
    # ==================================================


    def cargar_registros(self, registros=None):

        if registros is None:

            try:

                repositorio = PrestadorRepository()

                prestadores = repositorio.obtener_todos()

                registros = []

                for prestador in prestadores:

                    registros.append({
                        "id": prestador.id,

                        "nombre":
                            prestador.nombre_razon_social or "",

                        "rfc":
                            prestador.rfc or "",

                        "telefono":
                            prestador.telefono or "",



                        "registro_padron":
                            prestador.registro_padron or ""
                    })

            except Exception as error:

                print(
                    f"Error al cargar proveedores: {error}"
                )

                QMessageBox.critical(
                    self,
                    "Error al cargar proveedores",
                    "No fue posible consultar los proveedores "
                    "guardados en la base de datos."
                )

                registros = []

        self.registros = registros

        self.aplicar_filtro()

    # ==================================================
    # FILTRAR
    # ==================================================

    def aplicar_filtro(self):

        texto = (
            self.input_busqueda
            .text()
            .strip()
            .lower()
        )

        registros_filtrados = []

        for registro in self.registros:

            nombre = str(
                registro.get(
                    "nombre",
                    ""
                )
            )

            rfc = str(
                registro.get(
                    "rfc",
                    ""
                )
            )

            registro_padron = str(
                registro.get(
                    "registro_padron",
                    ""
                )
            )

            coincide = (
                texto == ""
                or texto in nombre.lower()
                or texto in rfc.lower()
                or texto in registro_padron.lower()
            )

            if coincide:

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
            # PROVEEDOR
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                0,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "nombre",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # RFC
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                1,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "rfc",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # TELÉFONO
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                2,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "telefono",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # REGISTRO EN PADRÓN
            # ------------------------------------------

            self.tabla.setItem(
                fila,
                3,
                QTableWidgetItem(
                    str(
                        registro.get(
                            "registro_padron",
                            ""
                        )
                    )
                )
            )

            # ------------------------------------------
            # ACCIONES
            # ------------------------------------------

            contenedor_acciones = QWidget()

            layout_acciones = QHBoxLayout(
                contenedor_acciones
            )

            layout_acciones.setContentsMargins(
                6,
                5,
                6,
                5
            )

            layout_acciones.setSpacing(
                7
            )

            layout_acciones.setAlignment(
                Qt.AlignCenter
            )

            proveedor_id = registro.get(
                "id"
            )

            # ------------------------------------------
            # VER
            # ------------------------------------------

            boton_ver = QPushButton(
                "Ver"
            )

            boton_ver.setObjectName(
                "botonTabla"
            )

            boton_ver.setCursor(
                Qt.PointingHandCursor
            )

            boton_ver.setMinimumHeight(
                32
            )

            boton_ver.setMinimumWidth(
                65
            )

            boton_ver.clicked.connect(
                lambda checked=False,
                id_proveedor=proveedor_id:
                self.ver_proveedor_solicitado.emit(
                    id_proveedor
                )
            )

            # ------------------------------------------
            # EDITAR
            # ------------------------------------------

            boton_editar = QPushButton(
                "Editar"
            )

            boton_editar.setObjectName(
                "botonTabla"
            )

            boton_editar.setCursor(
                Qt.PointingHandCursor
            )

            boton_editar.setMinimumHeight(
                32
            )

            boton_editar.setMinimumWidth(
                70
            )

            boton_editar.clicked.connect(
                lambda checked=False,
                id_proveedor=proveedor_id:
                self.editar_proveedor_solicitado.emit(
                    id_proveedor
                )
            )

            layout_acciones.addWidget(
                boton_ver
            )

            layout_acciones.addWidget(
                boton_editar
            )

            self.tabla.setCellWidget(
                fila,
                4,
                contenedor_acciones
            )