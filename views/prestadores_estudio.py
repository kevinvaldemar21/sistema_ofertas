from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QMessageBox,
    QDialog,
    QLineEdit,
    QTextEdit,
    QDialogButtonBox
)

from repositories.prestador_repository import PrestadorRepository
from repositories.estudio_repository import EstudioRepository
from views.conceptos_estudio import ConceptosEstudioView


class NuevoPrestadorDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.repository = PrestadorRepository()

        self.setWindowTitle(
            "Registrar nuevo prestador"
        )

        self.resize(500, 420)

        self.crear_interfaz()

    def crear_interfaz(self):

        layout = QVBoxLayout()

        formulario = QFormLayout()

        self.input_nombre = QLineEdit()

        self.input_nombre.setPlaceholderText(
            "Nombre o razón social"
        )

        self.input_rfc = QLineEdit()

        self.input_rfc.setPlaceholderText(
            "RFC"
        )

        self.input_telefono = QLineEdit()

        self.input_telefono.setPlaceholderText(
            "Teléfono"
        )

        self.input_domicilio = QTextEdit()

        self.input_domicilio.setPlaceholderText(
            "Domicilio"
        )

        self.input_domicilio.setMaximumHeight(
            90
        )

        self.input_padron = QLineEdit()

        self.input_padron.setPlaceholderText(
            "Registro en padrón"
        )

        formulario.addRow(
            "Nombre / Razón social:",
            self.input_nombre
        )

        formulario.addRow(
            "RFC:",
            self.input_rfc
        )

        formulario.addRow(
            "Teléfono:",
            self.input_telefono
        )

        formulario.addRow(
            "Domicilio:",
            self.input_domicilio
        )

        formulario.addRow(
            "Registro en padrón:",
            self.input_padron
        )

        layout.addLayout(formulario)

        botones = QDialogButtonBox(
            QDialogButtonBox.Save
            | QDialogButtonBox.Cancel
        )

        botones.accepted.connect(
            self.guardar
        )

        botones.rejected.connect(
            self.reject
        )

        layout.addWidget(botones)

        self.setLayout(layout)

    def guardar(self):

        nombre = (
            self.input_nombre
            .text()
            .strip()
        )

        rfc = (
            self.input_rfc
            .text()
            .strip()
            .upper()
        )

        telefono = (
            self.input_telefono
            .text()
            .strip()
        )

        domicilio = (
            self.input_domicilio
            .toPlainText()
            .strip()
        )

        padron = (
            self.input_padron
            .text()
            .strip()
        )

        if not nombre:

            QMessageBox.warning(
                self,
                "Campo requerido",
                "Debe ingresar el nombre "
                "o razón social."
            )

            self.input_nombre.setFocus()

            return

        try:

            self.repository.crear(
                nombre_razon_social=nombre,
                rfc=rfc or None,
                telefono=telefono or None,
                domicilio=domicilio or None,
                registro_padron=padron or None
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Prestador duplicado",
                str(error)
            )

            return

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible registrar "
                "el prestador.\n\n"
                f"{error}"
            )

            return

        QMessageBox.information(
            self,
            "Prestador registrado",
            "El prestador fue registrado "
            "correctamente."
        )

        self.accept()


class PrestadoresEstudioView(QWidget):

    def __init__(
        self,
        area,
        proyecto,
        datos_generales,
        ventana_anterior=None
    ):

        super().__init__()

        self.area = area
        self.proyecto = proyecto
        self.datos_generales = datos_generales
        self.ventana_anterior = ventana_anterior

        self.repository = PrestadorRepository()
        self.estudio_repository = EstudioRepository()

        self.prestadores = []

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_prestadores()

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Prestadores - Evaluación de Oferta"
        )

        self.resize(900, 650)

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout()

        titulo = QLabel(
            "Prestadores de Servicios"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        """)

        layout_principal.addWidget(titulo)

        # --------------------------------------------------
        # RESUMEN DEL ESTUDIO
        # --------------------------------------------------

        grupo_resumen = QGroupBox(
            "Resumen del proceso"
        )

        formulario_resumen = QFormLayout()

        self.label_area = QLabel(
            self.area.descripcion
        )

        self.label_proyecto = QLabel(
            f"{self.proyecto.codigo_proyecto} "
            f"- {self.proyecto.concepto}"
        )

        self.label_expediente = QLabel(
            self.datos_generales[
                "expediente"
            ]
        )

        self.label_objeto = QLabel(
            self.datos_generales[
                "objeto_contratacion"
            ]
        )

        self.label_objeto.setWordWrap(True)

        formulario_resumen.addRow(
            "Área:",
            self.label_area
        )

        formulario_resumen.addRow(
            "Proyecto:",
            self.label_proyecto
        )

        formulario_resumen.addRow(
            "Expediente:",
            self.label_expediente
        )

        formulario_resumen.addRow(
            "Objeto:",
            self.label_objeto
        )

        grupo_resumen.setLayout(
            formulario_resumen
        )

        layout_principal.addWidget(
            grupo_resumen
        )

        # --------------------------------------------------
        # PRESTADORES
        # --------------------------------------------------

        grupo_prestadores = QGroupBox(
            "Seleccione los prestadores"
        )

        formulario_prestadores = QFormLayout()

        self.combo_prestador_1 = QComboBox()
        self.combo_prestador_2 = QComboBox()
        self.combo_prestador_3 = QComboBox()

        self.combos = [
            self.combo_prestador_1,
            self.combo_prestador_2,
            self.combo_prestador_3
        ]

        for combo in self.combos:
            combo.setMinimumHeight(35)

        formulario_prestadores.addRow(
            "Prestador 1:",
            self.combo_prestador_1
        )

        formulario_prestadores.addRow(
            "Prestador 2:",
            self.combo_prestador_2
        )

        formulario_prestadores.addRow(
            "Prestador 3:",
            self.combo_prestador_3
        )

        grupo_prestadores.setLayout(
            formulario_prestadores
        )

        layout_principal.addWidget(
            grupo_prestadores
        )

        # --------------------------------------------------
        # NUEVO PRESTADOR
        # --------------------------------------------------

        self.boton_nuevo = QPushButton(
            "+ Registrar nuevo prestador"
        )

        self.boton_nuevo.setMinimumHeight(
            38
        )

        self.boton_nuevo.clicked.connect(
            self.registrar_nuevo_prestador
        )

        layout_principal.addWidget(
            self.boton_nuevo
        )

        # --------------------------------------------------
        # BOTONES
        # --------------------------------------------------

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
    # CARGAR PRESTADORES
    # ==================================================

    def cargar_prestadores(self):

        self.prestadores = (
            self.repository.obtener_todos()
        )

        for combo in self.combos:

            combo.clear()

            combo.addItem(
                "Seleccione un prestador...",
                None
            )

            for prestador in self.prestadores:

                combo.addItem(
                    prestador.nombre_razon_social,
                    prestador.id
                )

    # ==================================================
    # REGISTRAR NUEVO
    # ==================================================

    def registrar_nuevo_prestador(self):

        dialogo = NuevoPrestadorDialog(
            self
        )

        resultado = dialogo.exec()

        if resultado == QDialog.Accepted:

            self.cargar_prestadores()

    # ==================================================
    # VALIDACIÓN
    # ==================================================

    def obtener_ids_seleccionados(self):

        return [
            combo.currentData()
            for combo in self.combos
            if combo.currentData()
            is not None
        ]

    def validar_prestadores(self):

        ids = (
            self.obtener_ids_seleccionados()
        )

        if len(ids) < 2:

            QMessageBox.warning(
                self,
                "Prestadores requeridos",
                "Debe seleccionar al menos "
                "dos prestadores."
            )

            return False

        if len(ids) != len(set(ids)):

            QMessageBox.warning(
                self,
                "Prestadores duplicados",
                "No puede seleccionar "
                "el mismo prestador más "
                "de una vez."
            )

            return False

        return True

    # ==================================================
    # CONTINUAR
    # ==================================================

    def continuar(self):
        if not self.validar_prestadores():
            return

        ids = self.obtener_ids_seleccionados()

        seleccionados = []

        # Conservamos exactamente el orden de los combos
        for prestador_id in ids:

            prestador = next(
                (
                    p
                    for p in self.prestadores
                    if p.id == prestador_id
                ),
                None
            )

            if prestador:
                seleccionados.append(
                    prestador
                )

        try:

            # Crear estudio como BORRADOR
            estudio = (
                self.estudio_repository.crear(
                    area=self.area,
                    proyecto=self.proyecto,

                    fecha_elaboracion=(
                        self.datos_generales[
                            "fecha_elaboracion"
                        ]
                    ),

                    expediente=(
                        self.datos_generales[
                            "expediente"
                        ]
                    ),

                    partida_presupuestal=(
                        self.datos_generales[
                            "partida_presupuestal"
                        ]
                    ),

                    objeto_contratacion=(
                        self.datos_generales[
                            "objeto_contratacion"
                        ]
                    )
                )
            )

            # Asociar prestadores
            self.estudio_repository.agregar_prestadores(
                estudio.id,
                seleccionados
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Expediente existente",
                str(error)
            )

            return

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible guardar el proceso.\n\n"
                f"{error}"
            )

            return

        self.ventana_conceptos = ConceptosEstudioView(
            estudio=estudio,
            prestadores=seleccionados,
            ventana_anterior=self
        )

        self.ventana_conceptos.show()

        self.hide()

    # ==================================================
    # VOLVER
    # ==================================================

    def volver(self):

        if self.ventana_anterior is not None:
            self.ventana_anterior.show()

        self.close()