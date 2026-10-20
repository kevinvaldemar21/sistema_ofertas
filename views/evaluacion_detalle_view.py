
from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFormLayout,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class EvaluacionDetalleView(QWidget):

    volver_solicitado = Signal()

    def __init__(
        self,
        estudio,
        cotizaciones,
        evaluaciones,
        parent=None
    ):
        super().__init__(parent)

        self.estudio = estudio
        self.cotizaciones = cotizaciones

        self.evaluaciones_por_prestador = {
            evaluacion.prestador_id: evaluacion
            for evaluacion in evaluaciones
        }

        self.crear_interfaz()

    def crear_interfaz(self):

        layout_principal = QVBoxLayout(self)

        # Encabezado
        encabezado = QHBoxLayout()

        bloque_titulo = QVBoxLayout()

        titulo = QLabel("Detalle de evaluación")
        titulo.setObjectName("tituloPagina")

        descripcion = QLabel(
            "Consulta de los criterios evaluados "
            "para cada prestador del estudio."
        )
        descripcion.setObjectName("descripcionPagina")
        descripcion.setWordWrap(True)

        bloque_titulo.addWidget(titulo)
        bloque_titulo.addWidget(descripcion)

        encabezado.addLayout(bloque_titulo, 1)

        boton_volver = QPushButton("Volver al listado")
        boton_volver.setMinimumHeight(38)
        boton_volver.clicked.connect(
            self.volver_solicitado.emit
        )

        encabezado.addWidget(
            boton_volver,
            alignment=Qt.AlignTop
        )

        layout_principal.addLayout(encabezado)
        layout_principal.addSpacing(18)

        # Datos generales del estudio
        grupo_datos = QGroupBox("Datos del estudio")
        formulario = QFormLayout(grupo_datos)

        fecha = (
            self.estudio.fecha_elaboracion.strftime("%d/%m/%Y")
            if self.estudio.fecha_elaboracion
            else "-"
        )

        datos = [
            ("Expediente:", self.estudio.expediente or "-"),
            ("Fecha:", fecha),
            ("Área:", self.estudio.area_descripcion or "-"),
            ("Proyecto:", self.estudio.concepto_proyecto or "-"),
            ("Responsable:", self.estudio.responsable or "-"),
            ("Estado:", self.estudio.estado or "-"),
            (
                "Objeto de contratación:",
                self.estudio.objeto_contratacion or "-"
            )
        ]

        for etiqueta, valor in datos:
            texto = QLabel(str(valor))
            texto.setWordWrap(True)
            formulario.addRow(etiqueta, texto)

        layout_principal.addWidget(grupo_datos)
        layout_principal.addSpacing(18)

        # Resultados por prestador
        titulo_tabla = QLabel("Resultados por prestador")
        titulo_tabla.setObjectName("subtituloSeccion")

        layout_principal.addWidget(titulo_tabla)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Prestador",
            "Cantidad",
            "Calidad",
            "Oportunidad"
        ])

        self.tabla.setRowCount(len(self.cotizaciones))
        self.tabla.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().setVisible(False)

        encabezado_tabla = self.tabla.horizontalHeader()
        encabezado_tabla.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        for columna in range(1, 4):
            encabezado_tabla.setSectionResizeMode(
                columna,
                QHeaderView.ResizeToContents
            )

        for fila, cotizacion in enumerate(self.cotizaciones):

            prestador = cotizacion.prestador

            nombre = (
                prestador.nombre_razon_social
                if prestador
                else "Prestador no disponible"
            )

            evaluacion = self.evaluaciones_por_prestador.get(
                cotizacion.prestador_id
            )

            valores = [
                nombre,
                self.texto_cumplimiento(
                    evaluacion.cumple_cantidad
                    if evaluacion else None
                ),
                self.texto_cumplimiento(
                    evaluacion.cumple_calidad
                    if evaluacion else None
                ),
                self.texto_cumplimiento(
                    evaluacion.cumple_oportunidad
                    if evaluacion else None
                )
            ]

            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                self.tabla.setItem(fila, columna, item)

        layout_principal.addWidget(self.tabla, 1)

        if not self.cotizaciones:
            mensaje = QLabel(
                "Este estudio todavía no tiene cotizaciones registradas."
            )
            mensaje.setWordWrap(True)
            layout_principal.addWidget(mensaje)

    @staticmethod
    def texto_cumplimiento(valor):

        if valor is None:
            return "Sin evaluar"

        return "Sí" if bool(valor) else "No"
