from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QScrollArea
)

from repositories.cotizacion_repository import (
    CotizacionRepository
)

from repositories.condiciones_repository import (
    CondicionesRepository
)

from services.excel_service import (
    ExcelService
)

from repositories.evaluacion_repository import (
    EvaluacionRepository
)

from repositories.estudio_repository import (
    EstudioRepository
)

from repositories.documento_repository import (
    DocumentoRepository
)

class RevisionEstudioView(QWidget):

    def __init__(
        self,
        estudio,
        ventana_anterior=None
    ):

        super().__init__()

        self.estudio = estudio
        self.ventana_anterior = ventana_anterior

        self.cotizacion_repository = (
            CotizacionRepository()
        )

        self.condiciones_repository = (
            CondicionesRepository()
        )

        self.evaluacion_repository = (
            EvaluacionRepository()
        )

        self.estudio_repository = (
            EstudioRepository()
        )

        self.documento_repository = (
            DocumentoRepository()
        )

        self.excel_service = (
            ExcelService()
        )

        self.cotizaciones = []
        self.cotizacion_seleccionada = None
        self.condiciones = None
        self.evaluaciones = []

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_informacion()

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Revisión Final - Evaluación de Oferta"
        )

        self.resize(
            1250,
            800
        )

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_ventana = QVBoxLayout()

        titulo = QLabel(
            "Revisión Final de la Evaluación de Oferta"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout_ventana.addWidget(
            titulo
        )

        # ----------------------------------------------
        # SCROLL
        # ----------------------------------------------

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        contenido = QWidget()

        self.layout_contenido = QVBoxLayout(
            contenido
        )

        scroll.setWidget(
            contenido
        )

        layout_ventana.addWidget(
            scroll
        )

        # ----------------------------------------------
        # DATOS PROGRAMÁTICOS
        # ----------------------------------------------

        grupo_programatico = QGroupBox(
            "Información programática"
        )

        form_programatico = QFormLayout()

        self.label_area = QLabel()
        self.label_dg = QLabel()
        self.label_da = QLabel()
        self.label_proyecto = QLabel()
        self.label_concepto = QLabel()
        self.label_responsable = QLabel()
        self.label_cargo = QLabel()

        for label in [
            self.label_area,
            self.label_concepto,
            self.label_responsable,
            self.label_cargo
        ]:
            label.setWordWrap(True)

        form_programatico.addRow(
            "Área administrativa:",
            self.label_area
        )

        form_programatico.addRow(
            "DG:",
            self.label_dg
        )

        form_programatico.addRow(
            "DA:",
            self.label_da
        )

        form_programatico.addRow(
            "Proyecto:",
            self.label_proyecto
        )

        form_programatico.addRow(
            "Concepto:",
            self.label_concepto
        )

        form_programatico.addRow(
            "Responsable:",
            self.label_responsable
        )

        form_programatico.addRow(
            "Cargo:",
            self.label_cargo
        )

        grupo_programatico.setLayout(
            form_programatico
        )

        self.layout_contenido.addWidget(
            grupo_programatico
        )

        # ----------------------------------------------
        # DATOS GENERALES
        # ----------------------------------------------

        grupo_general = QGroupBox(
            "Datos generales"
        )

        form_general = QFormLayout()

        self.label_fecha = QLabel()
        self.label_expediente = QLabel()
        self.label_partida = QLabel()
        self.label_objeto = QLabel()

        self.label_objeto.setWordWrap(
            True
        )

        form_general.addRow(
            "Fecha de elaboración:",
            self.label_fecha
        )

        form_general.addRow(
            "Expediente:",
            self.label_expediente
        )

        form_general.addRow(
            "Partida presupuestal:",
            self.label_partida
        )

        form_general.addRow(
            "Objeto de contratación:",
            self.label_objeto
        )

        grupo_general.setLayout(
            form_general
        )

        self.layout_contenido.addWidget(
            grupo_general
        )

        # ----------------------------------------------
        # COMPARATIVO
        # ----------------------------------------------

        grupo_cotizaciones = QGroupBox(
            "Comparativo de cotizaciones"
        )

        layout_cotizaciones = QVBoxLayout()

        self.tabla = QTableWidget()

        layout_cotizaciones.addWidget(
            self.tabla
        )

        grupo_cotizaciones.setLayout(
            layout_cotizaciones
        )

        self.layout_contenido.addWidget(
            grupo_cotizaciones
        )

        # ----------------------------------------------
        # PRESTADOR SELECCIONADO
        # ----------------------------------------------

        grupo_seleccionado = QGroupBox(
            "Prestador seleccionado"
        )

        form_seleccionado = QFormLayout()

        self.label_prestador = QLabel()
        self.label_rfc = QLabel()
        self.label_total = QLabel()

        self.label_prestador.setWordWrap(
            True
        )

        self.label_total.setStyleSheet(
            "font-weight: bold;"
        )

        form_seleccionado.addRow(
            "Nombre / Razón social:",
            self.label_prestador
        )

        form_seleccionado.addRow(
            "RFC:",
            self.label_rfc
        )

        form_seleccionado.addRow(
            "Total:",
            self.label_total
        )

        grupo_seleccionado.setLayout(
            form_seleccionado
        )

        self.layout_contenido.addWidget(
            grupo_seleccionado
        )

        # ----------------------------------------------
        # CONDICIONES
        # ----------------------------------------------

        grupo_condiciones = QGroupBox(
            "Condiciones comerciales"
        )

        form_condiciones = QFormLayout()

        self.label_lugar = QLabel()
        self.label_plazo = QLabel()
        self.label_pago = QLabel()
        self.label_vigencia = QLabel()

        self.label_lugar.setWordWrap(True)
        self.label_pago.setWordWrap(True)

        self.label_tipo_procedimiento = QLabel()

        self.label_tipo_procedimiento.setWordWrap(
            True
        )

        form_condiciones.addRow(
            "Lugar de entrega / prestación:",
            self.label_lugar
        )

        form_condiciones.addRow(
            "Plazo de entrega:",
            self.label_plazo
        )

        form_condiciones.addRow(
            "Forma de pago:",
            self.label_pago
        )

        form_condiciones.addRow(
            "Vigencia de la cotización:",
            self.label_vigencia
        )

        form_condiciones.addRow(
            "Tipo de procedimiento:",
            self.label_tipo_procedimiento
        )

        grupo_condiciones.setLayout(
            form_condiciones
        )

        self.layout_contenido.addWidget(
            grupo_condiciones
        )

        # ----------------------------------------------
        # BOTONES
        # ----------------------------------------------

        botones = QHBoxLayout()

        self.boton_volver = QPushButton(
            "Volver"
        )

        self.boton_generar = QPushButton(
            "Generar formato Excel"
        )

        self.boton_volver.setMinimumSize(
            130,
            40
        )

        self.boton_generar.setMinimumSize(
            190,
            40
        )

        self.boton_volver.clicked.connect(
            self.volver
        )

        self.boton_generar.clicked.connect(
            self.generar_excel
        )

        botones.addWidget(
            self.boton_volver
        )

        botones.addStretch()

        botones.addWidget(
            self.boton_generar
        )

        layout_ventana.addLayout(
            botones
        )

        self.setLayout(
            layout_ventana
        )

    # ==================================================
    # CARGAR INFORMACIÓN
    # ==================================================

    def cargar_informacion(self):

        # ----------------------------------------------
        # PROGRAMÁTICOS
        # ----------------------------------------------

        self.label_area.setText(
            self.estudio.area_descripcion
        )

        self.label_dg.setText(
            self.estudio.codigo_dg
        )

        self.label_da.setText(
            self.estudio.codigo_da
        )

        self.label_proyecto.setText(
            self.estudio.codigo_proyecto
        )

        self.label_concepto.setText(
            self.estudio.concepto_proyecto
        )

        self.label_responsable.setText(
            self.estudio.responsable
            or "-"
        )

        self.label_cargo.setText(
            self.estudio.cargo_responsable
            or "-"
        )

        # ----------------------------------------------
        # GENERALES
        # ----------------------------------------------

        self.label_fecha.setText(
            self.estudio.fecha_elaboracion.strftime(
                "%d/%m/%Y"
            )
        )

        self.label_expediente.setText(
            self.estudio.expediente
        )

        self.label_partida.setText(
            self.estudio.partida_presupuestal
        )

        self.label_objeto.setText(
            self.estudio.objeto_contratacion
        )

        # ----------------------------------------------
        # COTIZACIONES
        # ----------------------------------------------

        self.cotizaciones = (
            self.cotizacion_repository
            .obtener_por_estudio(
                self.estudio.id
            )
        )

        self.cargar_comparativo()

        # ----------------------------------------------
        # SELECCIONADA
        # ----------------------------------------------

        self.cotizacion_seleccionada = (
            self.cotizacion_repository
            .obtener_seleccionada(
                self.estudio.id
            )
        )

        if self.cotizacion_seleccionada:

            prestador = (
                self.cotizacion_seleccionada
                .prestador
            )

            self.label_prestador.setText(
                prestador.nombre_razon_social
            )

            self.label_rfc.setText(
                prestador.rfc or "-"
            )

            self.label_total.setText(
                f"${float(self.cotizacion_seleccionada.total):,.2f}"
            )

        else:

            self.label_prestador.setText(
                "Sin prestador seleccionado"
            )

            self.label_rfc.setText("-")
            self.label_total.setText("-")

        # ----------------------------------------------
        # CONDICIONES
        # ----------------------------------------------

        self.condiciones = (
            self.condiciones_repository
            .obtener_por_estudio(
                self.estudio.id
            )
        )

        if self.condiciones:

            self.label_lugar.setText(
                self.condiciones.lugar_entrega
            )

            self.label_plazo.setText(
                self.condiciones.plazo_entrega
            )

            self.label_pago.setText(
                self.condiciones.forma_pago
            )

            self.label_vigencia.setText(
                self.condiciones.vigencia_cotizacion
            )

            self.label_tipo_procedimiento.setText(
                self.condiciones.tipo_procedimiento
                or "Sin información"
            )


        else:

            self.label_lugar.setText(
                "Sin información"
            )

            self.label_plazo.setText(
                "Sin información"
            )

            self.label_pago.setText(
                "Sin información"
            )

            self.label_vigencia.setText(
                "Sin información"
            )

        # ----------------------------------------------
        # EVALUACIONES
        # ----------------------------------------------

        self.evaluaciones = (
            self.evaluacion_repository
            .obtener_por_estudio(
                self.estudio.id
            )
        )

    # ==================================================
    # COMPARATIVO
    # ==================================================

    def cargar_comparativo(self):

        if not self.cotizaciones:
            return

        detalles_base = (
            self.cotizacion_repository
            .obtener_detalles(
                self.cotizaciones[0].id
            )
        )

        columnas = (
            4
            + len(self.cotizaciones)
        )

        self.tabla.setColumnCount(
            columnas
        )

        encabezados = [
            "No.",
            "Concepto",
            "Unidad",
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
        # DATOS BASE
        # ----------------------------------------------

        for fila, detalle in enumerate(
            detalles_base
        ):

            concepto = detalle.concepto

            datos = [
                str(concepto.numero),
                concepto.descripcion,
                concepto.unidad_medida,
                f"{float(concepto.cantidad):g}"
            ]

            for columna, texto in enumerate(
                datos
            ):

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
        # COTIZACIONES
        # ----------------------------------------------

        for indice, cotizacion in enumerate(
            self.cotizaciones
        ):

            detalles = (
                self.cotizacion_repository
                .obtener_detalles(
                    cotizacion.id
                )
            )

            columna = (
                4 + indice
            )

            for fila, detalle in enumerate(
                detalles
            ):

                texto = (
                    f"P.U. "
                    f"${float(detalle.precio_unitario):,.2f}\n"
                    f"Importe "
                    f"${float(detalle.importe):,.2f}"
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
        # TAMAÑO
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

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        for columna in range(
            4,
            self.tabla.columnCount()
        ):

            header.setSectionResizeMode(
                columna,
                QHeaderView.ResizeToContents
            )

        self.tabla.resizeRowsToContents()

    # ==================================================
    # VALIDACIÓN FINAL
    # ==================================================

    def validar_estudio(self):

        errores = []

        if not self.evaluaciones:
            errores.append(
                "No se registraron las evaluaciones "
                "de los prestadores."
            )

        if not self.cotizaciones:

            errores.append(
                "No existen cotizaciones."
            )

        if self.cotizacion_seleccionada is None:

            errores.append(
                "No existe un prestador seleccionado."
            )

        if self.condiciones is None:

            errores.append(
                "No se registraron las condiciones comerciales."
            )

        if errores:

            QMessageBox.warning(
                self,
                "Estudio incompleto",
                "No es posible generar el formato:\n\n"
                + "\n".join(
                    f"• {error}"
                    for error in errores
                )
            )

            return False

        return True

    # ==================================================
    # GENERAR EXCEL
    # ==================================================

    def generar_excel(self):

        if not self.validar_estudio():
            return

        # ==============================================
        # COMPROBAR SI EL DOCUMENTO YA EXISTE
        # ==============================================

        ruta_existente = (
            self.excel_service
            .obtener_ruta_documento(
                self.estudio
            )
        )

        if ruta_existente.exists():

            respuesta = QMessageBox.question(
                self,
                "Documento existente",
                "Ya existe un Estudio de Mercado "
                "generado para este proceso.\n\n"
                f"{ruta_existente.name}\n\n"
                "¿Desea regenerarlo y reemplazar "
                "el archivo actual?",
                QMessageBox.Yes
                | QMessageBox.No,
                QMessageBox.No
            )

            if respuesta != QMessageBox.Yes:

                return

        try:

            ruta = (
                self.excel_service
                .generar_estudio(
                    estudio=self.estudio,
                    cotizaciones=self.cotizaciones,
                    cotizacion_repository=(
                        self.cotizacion_repository
                    ),
                    condiciones=self.condiciones,
                    evaluaciones=self.evaluaciones
                )
            )

        except FileNotFoundError as error:

            QMessageBox.critical(
                self,
                "Plantilla no encontrada",
                str(error)
            )

            return

        except PermissionError:

            QMessageBox.critical(
                self,
                "Archivo en uso",
                "No fue posible reemplazar "
                "el documento existente.\n\n"
                "Es posible que el archivo esté "
                "abierto en Microsoft Excel.\n\n"
                "Cierre el documento e intente "
                "nuevamente."
            )

            return

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible generar "
                "el formato Excel.\n\n"
                f"{error}"
            )

            return

        # ==============================================
        # REGISTRAR DOCUMENTO
        # ==============================================

        try:

            ruta_relativa = (
                f"documentos/{ruta.name}"
            )

            self.documento_repository.registrar(
                estudio_id=self.estudio.id,
                tipo_documento="ESTUDIO_MERCADO",
                nombre_archivo=ruta.name,
                ruta_relativa=ruta_relativa
            )

        except Exception as error:

            QMessageBox.warning(
                self,
                "Documento generado",
                "El archivo Excel fue generado "
                "correctamente, pero no fue posible "
                "registrarlo en la base de datos.\n\n"
                f"{error}"
            )

            return

        try:

            self.estudio_repository.finalizar(
                self.estudio.id
            )

        except Exception as error:

            QMessageBox.warning(
                self,
                "Documento generado",
                "El archivo Excel fue generado "
                "correctamente, pero no fue posible "
                "actualizar el estado del proceso.\n\n"
                f"{error}"
            )

            return

        QMessageBox.information(
            self,
            "Proceso finalizado",
            "El proceso fue finalizado y el "
            "formato Excel fue generado "
            "correctamente.\n\n"
            f"Ubicación:\n{ruta}"
        )

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:

            self.ventana_anterior.show()

        self.close()