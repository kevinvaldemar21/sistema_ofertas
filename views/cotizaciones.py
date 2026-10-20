from PySide6.QtCore import Qt
from views.comparativo import ComparativoView

from repositories.cotizacion_repository import (
    CotizacionRepository
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QDoubleSpinBox,
    QMessageBox,
    QHeaderView,
    QGroupBox,
    QFormLayout
)


class CotizacionesView(QWidget):

    def __init__(
        self,
        estudio,
        conceptos,
        prestadores,
        ventana_anterior=None
    ):

        super().__init__()

        self.estudio = estudio
        self.conceptos = conceptos
        self.prestadores = prestadores
        self.ventana_anterior = ventana_anterior

        self.cotizacion_repository = (
            CotizacionRepository()
        )

        self.cargando_tabla = False

        self.labels_subtotal = []
        self.labels_iva = []
        self.labels_total = []

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_tabla()

        self.recalcular_todo()

        

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Cotizaciones"
        )

        self.resize(
            1400,
            750
        )

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout()

        titulo = QLabel(
            "Captura de Cotizaciones"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout_principal.addWidget(
            titulo
        )

        etiqueta_expediente = QLabel(
            f"Expediente: "
            f"{self.estudio.expediente}"
        )

        layout_principal.addWidget(
            etiqueta_expediente
        )

        # ----------------------------------------------
        # IVA
        # ----------------------------------------------

        layout_iva = QHBoxLayout()

        etiqueta_iva = QLabel(
            "IVA aplicado:"
        )

        self.input_iva = QDoubleSpinBox()

        self.input_iva.setRange(
            0,
            100
        )

        self.input_iva.setDecimals(
            2
        )

        self.input_iva.setValue(
            16
        )

        self.input_iva.setSuffix(
            " %"
        )

        self.input_iva.setSingleStep(
            1
        )

        self.input_iva.valueChanged.connect(
            self.recalcular_todo
        )

        layout_iva.addWidget(
            etiqueta_iva
        )

        layout_iva.addWidget(
            self.input_iva
        )

        layout_iva.addStretch()

        layout_principal.addLayout(
            layout_iva
        )

        # ----------------------------------------------
        # TABLA
        # ----------------------------------------------

        self.tabla = QTableWidget()

        columnas_base = 4

        columnas_proveedores = (
            len(self.prestadores) * 2
        )

        self.tabla.setColumnCount(
            columnas_base
            + columnas_proveedores
        )

        encabezados = [
            "No.",
            "Concepto",
            "Unidad",
            "Cantidad"
        ]

        for prestador in self.prestadores:

            nombre = (
                prestador.nombre_razon_social
            )

            encabezados.append(
                f"{nombre}\nPrecio unitario"
            )

            encabezados.append(
                f"{nombre}\nImporte"
            )

        self.tabla.setHorizontalHeaderLabels(
            encabezados
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
                QHeaderView.Interactive
            )

            self.tabla.setColumnWidth(
                columna,
                160
            )

        self.tabla.itemChanged.connect(
            self.celda_modificada
        )

        layout_principal.addWidget(
            self.tabla
        )

        # ----------------------------------------------
        # RESUMEN POR PROVEEDOR
        # ----------------------------------------------

        layout_resumen = QHBoxLayout()

        for prestador in self.prestadores:

            grupo = QGroupBox(
                prestador.nombre_razon_social
            )

            formulario = QFormLayout()

            label_subtotal = QLabel(
                "$0.00"
            )

            label_iva = QLabel(
                "$0.00"
            )

            label_total = QLabel(
                "$0.00"
            )

            label_total.setStyleSheet("""
                font-weight: bold;
            """)

            formulario.addRow(
                "Subtotal:",
                label_subtotal
            )

            formulario.addRow(
                "IVA:",
                label_iva
            )

            formulario.addRow(
                "Total:",
                label_total
            )

            grupo.setLayout(
                formulario
            )

            layout_resumen.addWidget(
                grupo
            )

            self.labels_subtotal.append(
                label_subtotal
            )

            self.labels_iva.append(
                label_iva
            )

            self.labels_total.append(
                label_total
            )

        layout_principal.addLayout(
            layout_resumen
        )

        # ----------------------------------------------
        # BOTONES
        # ----------------------------------------------

        layout_botones = QHBoxLayout()

        self.boton_volver = QPushButton(
            "Volver"
        )

        self.boton_guardar = QPushButton(
            "Guardar cotizaciones"
        )

        self.boton_volver.setMinimumSize(
            130,
            40
        )

        self.boton_guardar.setMinimumSize(
            180,
            40
        )

        self.boton_volver.clicked.connect(
            self.volver
        )

        self.boton_guardar.clicked.connect(
            self.guardar
        )

        layout_botones.addWidget(
            self.boton_volver
        )

        layout_botones.addStretch()

        layout_botones.addWidget(
            self.boton_guardar
        )

        layout_principal.addLayout(
            layout_botones
        )

        self.setLayout(
            layout_principal
        )

    # ==================================================
    # CARGAR TABLA
    # ==================================================

    def cargar_tabla(self):

        self.cargando_tabla = True

        self.tabla.setRowCount(
            len(self.conceptos)
        )

        for fila, concepto in enumerate(
            self.conceptos
        ):

            # Número
            item_numero = QTableWidgetItem(
                str(concepto.numero)
            )

            item_numero.setFlags(
                item_numero.flags()
                & ~Qt.ItemIsEditable
            )

            self.tabla.setItem(
                fila,
                0,
                item_numero
            )

            # Concepto
            item_concepto = QTableWidgetItem(
                concepto.descripcion
            )

            item_concepto.setFlags(
                item_concepto.flags()
                & ~Qt.ItemIsEditable
            )

            self.tabla.setItem(
                fila,
                1,
                item_concepto
            )

            # Unidad
            item_unidad = QTableWidgetItem(
                concepto.unidad_medida
            )

            item_unidad.setFlags(
                item_unidad.flags()
                & ~Qt.ItemIsEditable
            )

            self.tabla.setItem(
                fila,
                2,
                item_unidad
            )

            # Cantidad
            cantidad = float(
                concepto.cantidad
            )

            item_cantidad = QTableWidgetItem(
                f"{cantidad:g}"
            )

            item_cantidad.setFlags(
                item_cantidad.flags()
                & ~Qt.ItemIsEditable
            )

            self.tabla.setItem(
                fila,
                3,
                item_cantidad
            )

            # Proveedores
            for indice, _ in enumerate(
                self.prestadores
            ):

                columna_precio = (
                    4 + indice * 2
                )

                columna_importe = (
                    columna_precio + 1
                )

                item_precio = QTableWidgetItem(
                    "0.00"
                )

                item_precio.setTextAlignment(
                    Qt.AlignRight
                    | Qt.AlignVCenter
                )

                self.tabla.setItem(
                    fila,
                    columna_precio,
                    item_precio
                )

                item_importe = QTableWidgetItem(
                    "$0.00"
                )

                item_importe.setFlags(
                    item_importe.flags()
                    & ~Qt.ItemIsEditable
                )

                item_importe.setTextAlignment(
                    Qt.AlignRight
                    | Qt.AlignVCenter
                )

                self.tabla.setItem(
                    fila,
                    columna_importe,
                    item_importe
                )

        self.cargando_tabla = False

    # ==================================================
    # CELDA MODIFICADA
    # ==================================================

    def celda_modificada(
        self,
        item
    ):

        if self.cargando_tabla:
            return

        columna = item.column()

        # Sólo columnas de precio unitario:
        # 4, 6, 8, ...
        if columna < 4:
            return

        if (columna - 4) % 2 != 0:
            return

        texto = (
            item.text()
            .strip()
            .replace(",", "")
            .replace("$", "")
        )

        try:

            precio = float(
                texto
            )

            if precio < 0:
                raise ValueError

        except ValueError:

            QMessageBox.warning(
                self,
                "Precio inválido",
                "El precio unitario debe ser "
                "un número mayor o igual a cero."
            )

            self.cargando_tabla = True

            item.setText(
                "0.00"
            )

            self.cargando_tabla = False

            precio = 0

        item.setText(
            f"{precio:.2f}"
        )

        self.recalcular_fila(
            item.row()
        )

        self.recalcular_totales()

    # ==================================================
    # CALCULAR FILA
    # ==================================================

    def recalcular_fila(
        self,
        fila
    ):

        cantidad = float(
            self.conceptos[
                fila
            ].cantidad
        )

        self.cargando_tabla = True

        for indice, _ in enumerate(
            self.prestadores
        ):

            columna_precio = (
                4 + indice * 2
            )

            columna_importe = (
                columna_precio + 1
            )

            item_precio = self.tabla.item(
                fila,
                columna_precio
            )

            try:

                precio = float(
                    item_precio
                    .text()
                    .replace(",", "")
                    .replace("$", "")
                )

            except (ValueError, AttributeError):

                precio = 0

            importe = (
                cantidad
                * precio
            )

            item_importe = (
                self.tabla.item(
                    fila,
                    columna_importe
                )
            )

            item_importe.setText(
                f"${importe:,.2f}"
            )

        self.cargando_tabla = False

    # ==================================================
    # CALCULAR TOTALES
    # ==================================================

    def recalcular_totales(self):

        porcentaje_iva = (
            self.input_iva.value()
        )

        for indice, _ in enumerate(
            self.prestadores
        ):

            subtotal = 0

            columna_importe = (
                5 + indice * 2
            )

            for fila in range(
                self.tabla.rowCount()
            ):

                cantidad = float(
                    self.conceptos[
                        fila
                    ].cantidad
                )

                columna_precio = (
                    columna_importe - 1
                )

                item_precio = self.tabla.item(
                    fila,
                    columna_precio
                )

                try:

                    precio = float(
                        item_precio
                        .text()
                        .replace(",", "")
                        .replace("$", "")
                    )

                except (
                    ValueError,
                    AttributeError
                ):

                    precio = 0

                subtotal += (
                    cantidad
                    * precio
                )

            iva = (
                subtotal
                * porcentaje_iva
                / 100
            )

            total = (
                subtotal
                + iva
            )

            self.labels_subtotal[
                indice
            ].setText(
                f"${subtotal:,.2f}"
            )

            self.labels_iva[
                indice
            ].setText(
                f"${iva:,.2f}"
            )

            self.labels_total[
                indice
            ].setText(
                f"${total:,.2f}"
            )

    # ==================================================
    # RECALCULAR TODO
    # ==================================================

    def recalcular_todo(self):

        for fila in range(
            self.tabla.rowCount()
        ):

            self.recalcular_fila(
                fila
            )

        self.recalcular_totales()

    # ==================================================
    # VALIDAR
    # ==================================================

    def validar(self):

        for fila in range(
            self.tabla.rowCount()
        ):

            for indice, prestador in enumerate(
                self.prestadores
            ):

                columna_precio = (
                    4 + indice * 2
                )

                item = self.tabla.item(
                    fila,
                    columna_precio
                )

                try:

                    precio = float(
                        item.text()
                        .replace(",", "")
                        .replace("$", "")
                    )

                except (
                    ValueError,
                    AttributeError
                ):

                    precio = 0

                if precio <= 0:

                    QMessageBox.warning(
                        self,
                        "Precio requerido",
                        "Debe ingresar un precio "
                        "unitario mayor a cero para:\n\n"
                        f"{self.conceptos[fila].descripcion}\n"
                        f"{prestador.nombre_razon_social}"
                    )

                    self.tabla.setCurrentCell(
                        fila,
                        columna_precio
                    )

                    self.tabla.setFocus()

                    return False

        return True

    # ==================================================
    # GUARDAR
    # ==================================================

    def obtener_precios(self):

        precios = {}

        for indice, prestador in enumerate(
            self.prestadores
        ):

            precios[
                prestador.id
            ] = {}

            columna_precio = (
                4 + indice * 2
            )

            for fila, concepto in enumerate(
                self.conceptos
            ):

                item = self.tabla.item(
                    fila,
                    columna_precio
                )

                texto = (
                    item.text()
                    .strip()
                    .replace("$", "")
                    .replace(",", "")
                )

                precio = float(
                    texto
                )

                precios[
                    prestador.id
                ][
                    concepto.id
                ] = precio

        return precios

    def guardar(self):

        if not self.validar():
            return

        porcentaje_iva = (
            self.input_iva.value()
        )

        try:

            precios = (
                self.obtener_precios()
            )

            cotizaciones = (
                self.cotizacion_repository
                .guardar_cotizaciones(
                    estudio_id=self.estudio.id,
                    prestadores=self.prestadores,
                    conceptos=self.conceptos,
                    precios=precios,
                    porcentaje_iva=porcentaje_iva
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible guardar "
                "las cotizaciones.\n\n"
                f"{error}"
            )

            return

        QMessageBox.information(
            self,
            "Ofertas guardadas",
            "Las Ofertas fueron "
            "guardadas correctamente."
        )


        self.ventana_comparativo = ComparativoView(
            estudio=self.estudio,
            ventana_anterior=self
        )

        self.ventana_comparativo.show()

        self.hide()

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:

            self.ventana_anterior.show()

        self.close()