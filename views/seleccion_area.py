from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QMessageBox
)

from repositories.area_repository import AreaRepository
from views.datos_generales import DatosGeneralesView


class SeleccionAreaView(QWidget):

    def __init__(self):
        super().__init__()

        self.repository = AreaRepository()

        self.areas = []
        self.proyectos = []

        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_areas()

    # ==================================================
    # VENTANA
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Nueva Evaluacion de Oferta"
        )

        self.resize(850, 550)

    # ==================================================
    # INTERFAZ
    # ==================================================

    def crear_interfaz(self):

        layout_principal = QVBoxLayout()

        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        titulo = QLabel(
            "Nueva Evaluacion de Oferta"
        )

        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        """)

        layout_principal.addWidget(titulo)

        # ----------------------------------------------
        # SELECCIÓN DEL ÁREA
        # ----------------------------------------------

        etiqueta_area = QLabel(
            "Seleccione el área administrativa:"
        )

        self.combo_area = QComboBox()

        self.combo_area.setMinimumHeight(35)

        self.combo_area.currentIndexChanged.connect(
            self.area_seleccionada
        )

        layout_principal.addWidget(
            etiqueta_area
        )

        layout_principal.addWidget(
            self.combo_area
        )

        # ----------------------------------------------
        # INFORMACIÓN DEL ÁREA
        # ----------------------------------------------

        grupo_area = QGroupBox(
            "Información del área"
        )

        formulario_area = QFormLayout()

        self.label_dg = QLabel("-")
        self.label_da = QLabel("-")
        self.label_descripcion = QLabel("-")
        self.label_responsable = QLabel("-")
        self.label_cargo = QLabel("-")

        formulario_area.addRow(
            "DG:",
            self.label_dg
        )

        formulario_area.addRow(
            "DA:",
            self.label_da
        )

        formulario_area.addRow(
            "Descripción:",
            self.label_descripcion
        )

        formulario_area.addRow(
            "Responsable:",
            self.label_responsable
        )

        formulario_area.addRow(
            "Cargo:",
            self.label_cargo
        )

        grupo_area.setLayout(
            formulario_area
        )

        layout_principal.addWidget(
            grupo_area
        )

        # ----------------------------------------------
        # PROYECTOS
        # ----------------------------------------------

        etiqueta_proyecto = QLabel(
            "Proyecto / Concepto:"
        )

        self.combo_proyecto = QComboBox()

        self.combo_proyecto.setMinimumHeight(
            35
        )

        layout_principal.addWidget(
            etiqueta_proyecto
        )

        layout_principal.addWidget(
            self.combo_proyecto
        )

        # ----------------------------------------------
        # BOTÓN
        # ----------------------------------------------

        layout_botones = QHBoxLayout()

        layout_botones.addStretch()

        self.boton_continuar = QPushButton(
            "Continuar"
        )

        self.boton_continuar.setMinimumSize(
            140,
            40
        )

        self.boton_continuar.clicked.connect(
            self.continuar
        )

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
    # CARGAR ÁREAS
    # ==================================================

    def cargar_areas(self):

        self.combo_area.blockSignals(True)

        self.combo_area.clear()

        self.combo_area.addItem(
            "Seleccione un área...",
            None
        )

        self.areas = (
            self.repository.obtener_areas()
        )

        for area in self.areas:

            self.combo_area.addItem(
                area.descripcion,
                area.id
            )

        self.combo_area.blockSignals(False)

    # ==================================================
    # CUANDO CAMBIA EL ÁREA
    # ==================================================

    def area_seleccionada(self):

        area_id = (
            self.combo_area.currentData()
        )

        if area_id is None:

            self.limpiar_datos()
            return

        area = next(
            (
                area
                for area in self.areas
                if area.id == area_id
            ),
            None
        )

        if area is None:
            return

        # ----------------------------------------------
        # Mostrar información
        # ----------------------------------------------

        self.label_dg.setText(
            area.codigo_dg or "-"
        )

        self.label_da.setText(
            area.codigo_da or "-"
        )

        self.label_descripcion.setText(
            area.descripcion or "-"
        )

        self.label_responsable.setText(
            area.responsable
            or "Sin responsable registrado"
        )

        self.label_cargo.setText(
            area.cargo_responsable
            or "Sin cargo registrado"
        )

        # ----------------------------------------------
        # Cargar proyectos
        # ----------------------------------------------

        self.cargar_proyectos(
            area.id
        )

    # ==================================================
    # PROYECTOS
    # ==================================================

    def cargar_proyectos(self, area_id):

        self.combo_proyecto.clear()

        self.combo_proyecto.addItem(
            "Seleccione un proyecto...",
            None
        )

        self.proyectos = (
            self.repository
            .obtener_proyectos_por_area(
                area_id
            )
        )

        for proyecto in self.proyectos:

            texto = (
                f"{proyecto.codigo_proyecto}"
                f" - "
                f"{proyecto.concepto}"
            )

            self.combo_proyecto.addItem(
                texto,
                proyecto.id
            )

    # ==================================================
    # LIMPIAR
    # ==================================================

    def limpiar_datos(self):

        self.label_dg.setText("-")
        self.label_da.setText("-")
        self.label_descripcion.setText("-")
        self.label_responsable.setText("-")
        self.label_cargo.setText("-")

        self.combo_proyecto.clear()

        self.combo_proyecto.addItem(
            "Seleccione un proyecto...",
            None
        )

    # ==================================================
    # CONTINUAR
    # ==================================================

    def continuar(self):

        area_id = self.combo_area.currentData()

        proyecto_id = self.combo_proyecto.currentData()

        if area_id is None:

            QMessageBox.warning(
                self,
                "Área requerida",
                "Debe seleccionar un área."
            )

            return

        if proyecto_id is None:

            QMessageBox.warning(
                self,
                "Proyecto requerido",
                "Debe seleccionar un proyecto."
            )

            return

        area = next(
            (
                area
                for area in self.areas
                if area.id == area_id
            ),
            None
        )

        proyecto = next(
            (
                proyecto
                for proyecto in self.proyectos
                if proyecto.id == proyecto_id
            ),
            None
        )

        if area is None or proyecto is None:

            QMessageBox.critical(
                self,
                "Error",
                "No fue posible recuperar "
                "la información seleccionada."
            )

            return

    # Mantener una referencia a la nueva ventana.
    # Esto evita que Python la elimine de memoria.

        self.ventana_datos_generales = (
            DatosGeneralesView(
                area=area,
                proyecto=proyecto,
                ventana_anterior=self
            )
        )

        self.ventana_datos_generales.show()

        self.hide()