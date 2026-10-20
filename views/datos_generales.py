from PySide6.QtCore import QDate
from views.prestadores_estudio import PrestadoresEstudioView
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QDateEdit,
    QMessageBox
)

from repositories.estudio_repository import (
    EstudioRepository
)

from PySide6.QtWidgets import QMessageBox

class DatosGeneralesView(QWidget):

    def __init__(self, area, proyecto, ventana_anterior=None):
        super().__init__()

        self.area = area
        self.proyecto = proyecto
        self.ventana_anterior = ventana_anterior

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_datos_automaticos()
        self.estudio_repository = (
            EstudioRepository()
        )

    # ==================================================
    # CONFIGURACIÓN
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Datos del Proceso de Cotización"
        )

        self.resize(900, 650)

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout()

        # --------------------------------------------------
        # TÍTULO
        # --------------------------------------------------

        titulo = QLabel(
            "Datos Generales"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        """)

        layout_principal.addWidget(titulo)

        # ==================================================
        # INFORMACIÓN PROGRAMÁTICA
        # ==================================================

        grupo_programatico = QGroupBox(
            "Información programática"
        )

        formulario_programatico = QFormLayout()

        self.label_area = QLabel("-")
        self.label_dg = QLabel("-")
        self.label_da = QLabel("-")
        self.label_proyecto = QLabel("-")
        self.label_concepto = QLabel("-")
        self.label_responsable = QLabel("-")
        self.label_cargo = QLabel("-")

        self.label_area.setWordWrap(True)
        self.label_concepto.setWordWrap(True)
        self.label_responsable.setWordWrap(True)
        self.label_cargo.setWordWrap(True)

        formulario_programatico.addRow(
            "Área administrativa:",
            self.label_area
        )

        formulario_programatico.addRow(
            "DG:",
            self.label_dg
        )

        formulario_programatico.addRow(
            "DA:",
            self.label_da
        )

        formulario_programatico.addRow(
            "Proyecto:",
            self.label_proyecto
        )

        formulario_programatico.addRow(
            "Concepto:",
            self.label_concepto
        )

        formulario_programatico.addRow(
            "Responsable:",
            self.label_responsable
        )

        formulario_programatico.addRow(
            "Cargo:",
            self.label_cargo
        )

        grupo_programatico.setLayout(
            formulario_programatico
        )

        layout_principal.addWidget(
            grupo_programatico
        )

        # ==================================================
        # DATOS DEL ESTUDIO
        # ==================================================

        grupo_estudio = QGroupBox(
            "Datos del proceso"
        )

        formulario_estudio = QFormLayout()

        # --------------------------------------------------
        # FECHA
        # --------------------------------------------------

        self.input_fecha = QDateEdit()

        self.input_fecha.setCalendarPopup(True)

        self.input_fecha.setDisplayFormat(
            "dd/MM/yyyy"
        )

        self.input_fecha.setDate(
            QDate.currentDate()
        )

        self.input_fecha.setMinimumHeight(32)

        # --------------------------------------------------
        # EXPEDIENTE
        # --------------------------------------------------

        self.input_expediente = QLineEdit()

        self.input_expediente.setPlaceholderText(
            "Ingrese el número o clave del expediente"
        )

        self.input_expediente.setMinimumHeight(32)

        # --------------------------------------------------
        # PARTIDA
        # --------------------------------------------------

        self.input_partida = QLineEdit()

        self.input_partida.setPlaceholderText(
            "Ingrese la partida presupuestal"
        )

        self.input_partida.setMinimumHeight(32)

        # --------------------------------------------------
        # OBJETO DE CONTRATACIÓN
        # --------------------------------------------------

        self.input_objeto = QTextEdit()

        self.input_objeto.setPlaceholderText(
            "Describa el objeto de contratación o adquisición"
        )

        self.input_objeto.setMinimumHeight(100)

        # --------------------------------------------------
        # AGREGAR CAMPOS
        # --------------------------------------------------

        formulario_estudio.addRow(
            "Fecha de elaboración:",
            self.input_fecha
        )

        formulario_estudio.addRow(
            "Expediente:",
            self.input_expediente
        )

        formulario_estudio.addRow(
            "Partida presupuestal:",
            self.input_partida
        )

        formulario_estudio.addRow(
            "Objeto de contratación:",
            self.input_objeto
        )

        grupo_estudio.setLayout(
            formulario_estudio
        )

        layout_principal.addWidget(
            grupo_estudio
        )

        # ==================================================
        # BOTONES
        # ==================================================

        layout_botones = QHBoxLayout()

        self.boton_volver = QPushButton(
            "Volver"
        )

        self.boton_continuar = QPushButton(
            "Continuar"
        )

        self.boton_volver.setMinimumSize(
            130,
            40
        )

        self.boton_continuar.setMinimumSize(
            130,
            40
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

        layout_principal.addLayout(
            layout_botones
        )

        self.setLayout(
            layout_principal
        )

    # ==================================================
    # CARGAR INFORMACIÓN AUTOMÁTICA
    # ==================================================

    def cargar_datos_automaticos(self):

        self.label_area.setText(
            self.area.descripcion or "-"
        )

        self.label_dg.setText(
            self.area.codigo_dg or "-"
        )

        self.label_da.setText(
            self.area.codigo_da or "-"
        )

        self.label_proyecto.setText(
            self.proyecto.codigo_proyecto or "-"
        )

        self.label_concepto.setText(
            self.proyecto.concepto or "-"
        )

        self.label_responsable.setText(
            self.area.responsable
            or "Sin responsable registrado"
        )

        self.label_cargo.setText(
            self.area.cargo_responsable
            or "Sin cargo registrado"
        )

    # ==================================================
    # VALIDACIÓN
    # ==================================================

    def validar_datos(self):

        expediente = (
            self.input_expediente
            .text()
            .strip()
        )

        partida = (
            self.input_partida
            .text()
            .strip()
        )

        objeto = (
            self.input_objeto
            .toPlainText()
            .strip()
        )

        if not expediente:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar el expediente."
            )

            self.input_expediente.setFocus()

            return False

        if not partida:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar la partida presupuestal."
            )

            self.input_partida.setFocus()

            return False

        if not objeto:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar el objeto de contratación."
            )

            self.input_objeto.setFocus()

            return False

        return True

    # ==================================================
    # CONTINUAR
    # ==================================================

    def continuar(self):

        if not self.validar_datos():
            return

        fecha_qdate = (
            self.input_fecha.date()
        )

        fecha_python = (
            fecha_qdate.toPython()
        )

        expediente = (
            self.input_expediente
            .text()
            .strip()
        )

        partida = (
            self.input_partida
            .text()
            .strip()
        )

        objeto = (
            self.input_objeto
            .toPlainText()
            .strip()
        )

        datos_generales = {
            "fecha_elaboracion": fecha_python,
            "expediente": expediente,
            "partida_presupuestal": partida,
            "objeto_contratacion": objeto
        }

        expediente = (
            self.input_expediente
            .text()
            .strip()
        )

        if self.estudio_repository.existe_expediente(
            expediente
        ):

            QMessageBox.warning(
                self,
                "Expediente existente",
                "Ya existe un proceso registrado "
                f"con el expediente '{expediente}'.\n\n"
                "Ingrese un expediente diferente."
            )

            self.input_expediente.setFocus()

            return

        self.ventana_prestadores = (
            PrestadoresEstudioView(
                area=self.area,
                proyecto=self.proyecto,
                datos_generales=datos_generales,
                ventana_anterior=self
            )
        )

        self.ventana_prestadores.show()

        self.hide()

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:

            self.ventana_anterior.show()

        self.close()