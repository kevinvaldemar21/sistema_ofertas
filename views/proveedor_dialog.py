
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QMessageBox
)


class ProveedorDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Nuevo proveedor")
        self.setMinimumWidth(540)
        self.setModal(True)

        layout_principal = QVBoxLayout(self)

        layout_principal.setContentsMargins(
            24, 24, 24, 24
        )

        layout_principal.setSpacing(14)

        # ENCABEZADO

        titulo = QLabel("Registrar proveedor")
        titulo.setObjectName("tituloPagina")

        descripcion = QLabel(
            "Capture los datos generales del proveedor."
        )
        descripcion.setObjectName("descripcionPagina")
        descripcion.setWordWrap(True)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descripcion)

        # CAMPOS DEL FORMULARIO

        formulario = QFormLayout()
        formulario.setSpacing(12)

        self.input_nombre = QLineEdit()
        self.input_nombre.setMaxLength(255)
        self.input_nombre.setPlaceholderText(
            "Nombre completo o razón social"
        )

        self.input_rfc = QLineEdit()
        self.input_rfc.setMaxLength(20)
        self.input_rfc.setPlaceholderText(
            "RFC del proveedor"
        )

        self.input_telefono = QLineEdit()
        self.input_telefono.setMaxLength(30)
        self.input_telefono.setPlaceholderText(
            "Teléfono de contacto"
        )

        self.input_registro_padron = QLineEdit()
        self.input_registro_padron.setMaxLength(100)
        self.input_registro_padron.setPlaceholderText(
            "Número o referencia del padrón"
        )

        self.input_domicilio = QPlainTextEdit()
        self.input_domicilio.setPlaceholderText(
            "Domicilio del proveedor"
        )
        self.input_domicilio.setFixedHeight(80)

        formulario.addRow(
            "Nombre o razón social *",
            self.input_nombre
        )

        formulario.addRow(
            "RFC",
            self.input_rfc
        )

        formulario.addRow(
            "Teléfono",
            self.input_telefono
        )

        formulario.addRow(
            "Registro en padrón",
            self.input_registro_padron
        )

        formulario.addRow(
            "Domicilio",
            self.input_domicilio
        )

        layout_principal.addLayout(formulario)

        # BOTONES

        botones = QHBoxLayout()
        botones.addStretch()

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setCursor(
            Qt.PointingHandCursor
        )

        self.boton_guardar = QPushButton(
            "Guardar proveedor"
        )
        self.boton_guardar.setObjectName(
            "botonPrimario"
        )
        self.boton_guardar.setCursor(
            Qt.PointingHandCursor
        )

        botones.addWidget(self.boton_cancelar)
        botones.addWidget(self.boton_guardar)

        layout_principal.addLayout(botones)

        # EVENTOS

        self.boton_cancelar.clicked.connect(
            self.reject
        )

        self.boton_guardar.clicked.connect(
            self.validar_datos
        )

    def validar_datos(self):

        nombre = self.input_nombre.text().strip()

        if not nombre:

            QMessageBox.warning(
                self,
                "Dato obligatorio",
                "Ingresa el nombre o la razón social "
                "del proveedor."
            )

            self.input_nombre.setFocus()
            return

        self.accept()

    def obtener_datos(self):

        return {
            "nombre_razon_social":
                self.input_nombre.text().strip(),

            "rfc":
                self.input_rfc.text().strip().upper() or None,

            "telefono":
                self.input_telefono.text().strip() or None,

            "registro_padron":
                self.input_registro_padron.text().strip() or None,

            "domicilio":
                self.input_domicilio.toPlainText().strip() or None
        }
