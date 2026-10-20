from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QMessageBox
)

from repositories.condiciones_repository import (
    CondicionesRepository
)

from views.revision_estudio import (
    RevisionEstudioView
)

class CondicionesEstudioView(QWidget):

    def __init__(
        self,
        estudio,
        cotizacion_seleccionada,
        ventana_anterior=None
    ):

        super().__init__()

        self.estudio = estudio

        self.cotizacion_seleccionada = (
            cotizacion_seleccionada
        )

        self.ventana_anterior = (
            ventana_anterior
        )

        self.repository = (
            CondicionesRepository()
        )

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_existentes()

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Condiciones - Estudio de Mercado"
        )

        self.resize(
            900,
            650
        )

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout()

        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        titulo = QLabel(
            "Condiciones Comerciales"
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

        # ----------------------------------------------
        # PRESTADOR SELECCIONADO
        # ----------------------------------------------

        prestador = (
            self.cotizacion_seleccionada
            .prestador
        )

        grupo_prestador = QGroupBox(
            "Prestador seleccionado"
        )

        formulario_prestador = QFormLayout()

        formulario_prestador.addRow(
            "Nombre / Razón social:",
            QLabel(
                prestador.nombre_razon_social
            )
        )

        formulario_prestador.addRow(
            "RFC:",
            QLabel(
                prestador.rfc or "-"
            )
        )

        formulario_prestador.addRow(
            "Total cotizado:",
            QLabel(
                f"${float(self.cotizacion_seleccionada.total):,.2f}"
            )
        )

        grupo_prestador.setLayout(
            formulario_prestador
        )

        layout_principal.addWidget(
            grupo_prestador
        )

        # ----------------------------------------------
        # CONDICIONES
        # ----------------------------------------------

        grupo = QGroupBox(
            "Condiciones"
        )

        formulario = QFormLayout()

        self.input_lugar = QTextEdit()

        self.input_lugar.setPlaceholderText(
            "Ingrese el lugar de entrega o "
            "prestación del servicio"
        )

        self.input_lugar.setMaximumHeight(
            90
        )

        self.input_plazo = QLineEdit()

        self.input_plazo.setPlaceholderText(
            "Ej. 5 días hábiles"
        )

        self.input_pago = QTextEdit()

        self.input_pago.setPlaceholderText(
            "Ingrese la forma de pago"
        )

        self.input_pago.setMaximumHeight(
            90
        )

        self.input_tipo_procedimiento = (
            QLineEdit()
        )

        self.input_tipo_procedimiento.setPlaceholderText(
            "Ej. Adjudicación directa por contrato pedido"
        )

        self.input_vigencia = QLineEdit()

        self.input_vigencia.setPlaceholderText(
            "Ej. 30 días naturales"
        )

        formulario.addRow(
            "Lugar de entrega / prestación:",
            self.input_lugar
        )

        formulario.addRow(
            "Plazo de entrega:",
            self.input_plazo
        )

        formulario.addRow(
            "Forma de pago:",
            self.input_pago
        )

        formulario.addRow(
            "Tipo de procedimiento:",
            self.input_tipo_procedimiento
        )

        formulario.addRow(
            "Vigencia de la cotización:",
            self.input_vigencia
        )

        grupo.setLayout(
            formulario
        )

        layout_principal.addWidget(
            grupo
        )

        # ----------------------------------------------
        # BOTONES
        # ----------------------------------------------

        layout_botones = QHBoxLayout()

        self.boton_volver = QPushButton(
            "Volver"
        )

        self.boton_continuar = QPushButton(
            "Guardar y continuar"
        )

        self.boton_volver.setMinimumSize(
            130,
            40
        )

        self.boton_continuar.setMinimumSize(
            170,
            40
        )

        self.boton_volver.clicked.connect(
            self.volver
        )

        self.boton_continuar.clicked.connect(
            self.guardar
        )

        layout_botones.addWidget(
            self.boton_volver
        )

        layout_botones.addStretch()

        layout_botones.addWidget(
            self.boton_continuar
        )

        layout_principal.addLayout(
            layout_botones
        )

        self.setLayout(
            layout_principal
        )

    # ==================================================
    # CARGAR SI YA EXISTEN
    # ==================================================

    def cargar_existentes(self):

        condiciones = (
            self.repository.obtener_por_estudio(
                self.estudio.id
            )
        )

        if condiciones is None:
            return

        self.input_lugar.setPlainText(
            condiciones.lugar_entrega
        )

        self.input_plazo.setText(
            condiciones.plazo_entrega
        )

        self.input_pago.setPlainText(
            condiciones.forma_pago
        )

        self.input_vigencia.setText(
            condiciones.vigencia_cotizacion
        )

        self.input_tipo_procedimiento.setText(
            condiciones.tipo_procedimiento
            or ""
        )

    # ==================================================
    # VALIDAR
    # ==================================================

    def validar(self):

        lugar = (
            self.input_lugar
            .toPlainText()
            .strip()
        )

        plazo = (
            self.input_plazo
            .text()
            .strip()
        )

        pago = (
            self.input_pago
            .toPlainText()
            .strip()
        )

        vigencia = (
            self.input_vigencia
            .text()
            .strip()
        )

        tipo_procedimiento = (
            self.input_tipo_procedimiento
            .text()
            .strip()
        )

        if not lugar:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar el lugar "
                "de entrega o prestación."
            )

            self.input_lugar.setFocus()

            return False

        if not plazo:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar el plazo "
                "de entrega."
            )

            self.input_plazo.setFocus()

            return False

        if not pago:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar la forma "
                "de pago."
            )

            self.input_pago.setFocus()

            return False

        if not vigencia:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar la vigencia "
                "de la cotización."
            )

            self.input_vigencia.setFocus()

            return False

        if not tipo_procedimiento:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar el tipo de procedimiento."
            )

            self.input_tipo_procedimiento.setFocus()

            return False

        return True

    # ==================================================
    # GUARDAR
    # ==================================================

    def guardar(self):

        if not self.validar():
            return

        lugar = (
            self.input_lugar
            .toPlainText()
            .strip()
        )

        plazo = (
            self.input_plazo
            .text()
            .strip()
        )

        pago = (
            self.input_pago
            .toPlainText()
            .strip()
        )

        vigencia = (
            self.input_vigencia
            .text()
            .strip()
        )

        tipo_procedimiento = (
            self.input_tipo_procedimiento
            .text()
            .strip()
        )



        try:

            self.repository.guardar(
                estudio_id=self.estudio.id,
                lugar_entrega=lugar,
                plazo_entrega=plazo,
                forma_pago=pago,
                vigencia_cotizacion=vigencia,
                tipo_procedimiento=tipo_procedimiento
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible guardar "
                "las condiciones.\n\n"
                f"{error}"
            )

            return

        QMessageBox.information(
            self,
            "Condiciones guardadas",
            "Las condiciones fueron "
            "guardadas correctamente."
        )

        self.ventana_revision = (
            RevisionEstudioView(
                estudio=self.estudio,
                ventana_anterior=self
            )
        )

        self.ventana_revision.show()

        self.hide()

        # Aquí abriremos posteriormente
        # la revisión final del estudio.

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:

            self.ventana_anterior.show()

        self.close()