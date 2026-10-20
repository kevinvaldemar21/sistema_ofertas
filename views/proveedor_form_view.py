
from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton
)


class ProveedorFormView(QWidget):

    guardar_solicitado = Signal(dict)
    cancelar_solicitado = Signal()

    def __init__(
        self,
        prestador=None,
        modo="crear",
        parent=None
    ):

        super().__init__(parent)

        self.prestador = prestador
        self.modo = modo

        self.crear_interfaz()

        if self.prestador is not None:
            self.cargar_datos()

        self.configurar_modo()

    def crear_interfaz(self):

        layout_principal = QVBoxLayout(self)

        layout_principal.setContentsMargins(
            0, 0, 0, 0
        )

        layout_principal.setSpacing(18)

        # ENCABEZADO

        titulos = {
            "crear": "Registrar proveedor",
            "editar": "Editar proveedor",
            "ver": "Consultar proveedor"
        }

        descripciones = {
            "crear": "Capture los datos generales del proveedor.",
            "editar": "Modifique los datos del proveedor seleccionado.",
            "ver": "Consulte la información del proveedor."
        }

        titulo = QLabel(
            titulos.get(self.modo, "Proveedor")
        )
        titulo.setObjectName("tituloPagina")

        descripcion = QLabel(
            descripciones.get(self.modo, "")
        )
        descripcion.setObjectName("descripcionPagina")
        descripcion.setWordWrap(True)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descripcion)

        # CAMPOS

        formulario = QFormLayout()
        formulario.setSpacing(14)

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
        self.input_domicilio.setFixedHeight(90)

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

        # MENSAJE INTERNO

        self.mensaje = QLabel("")
        self.mensaje.setObjectName("mensajeFormulario")
        self.mensaje.setWordWrap(True)

        layout_principal.addWidget(self.mensaje)

        # BOTONES

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setObjectName("botonTabla")
        self.boton_cancelar.setMinimumHeight(40)
        self.boton_cancelar.setCursor(
            Qt.PointingHandCursor
        )

        self.boton_guardar = QPushButton(
            "Guardar proveedor"
        )
        self.boton_guardar.setObjectName(
            "botonPrimario"
        )
        self.boton_guardar.setMinimumHeight(40)
        self.boton_guardar.setCursor(
            Qt.PointingHandCursor
        )

        layout_botones.addWidget(self.boton_cancelar)
        layout_botones.addWidget(self.boton_guardar)

        layout_principal.addLayout(layout_botones)

        # EVENTOS

        self.boton_cancelar.clicked.connect(
            self.cancelar_solicitado.emit
        )

        self.boton_guardar.clicked.connect(
            self.validar_y_guardar
        )

    def cargar_datos(self):

        prestador = self.prestador

        self.input_nombre.setText(
            prestador.nombre_razon_social or ""
        )

        self.input_rfc.setText(
            prestador.rfc or ""
        )

        self.input_telefono.setText(
            prestador.telefono or ""
        )

        self.input_registro_padron.setText(
            prestador.registro_padron or ""
        )

        self.input_domicilio.setPlainText(
            prestador.domicilio or ""
        )

    def configurar_modo(self):

        if self.modo == "crear":

            self.input_nombre.setFocus()
            return

        if self.modo == "editar":

            self.boton_guardar.setText(
                "Guardar cambios"
            )

            return

        if self.modo == "ver":

            self.input_nombre.setReadOnly(True)
            self.input_rfc.setReadOnly(True)
            self.input_telefono.setReadOnly(True)

            self.input_registro_padron.setReadOnly(
                True
            )

            self.input_domicilio.setReadOnly(True)

            self.boton_guardar.hide()

            self.boton_cancelar.setText(
                "Volver"
            )

    def validar_y_guardar(self):

        if self.modo == "ver":
            return

        nombre = self.input_nombre.text().strip()

        if not nombre:

            self.mostrar_error(
                "Ingresa el nombre o la razón social "
                "del proveedor."
            )

            self.input_nombre.setFocus()
            return

        datos = {
            "nombre_razon_social": nombre,

            "rfc":
                self.input_rfc.text().strip().upper()
                or None,

            "telefono":
                self.input_telefono.text().strip()
                or None,

            "registro_padron":
                self.input_registro_padron.text().strip()
                or None,

            "domicilio":
                self.input_domicilio.toPlainText().strip()
                or None
        }

        self.mensaje.clear()

        self.guardar_solicitado.emit(datos)

    def mostrar_error(self, mensaje):

        self.mensaje.setText(mensaje)

        self.mensaje.setStyleSheet(
            "color: #B42318;"
        )
