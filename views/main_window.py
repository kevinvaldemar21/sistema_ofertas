from PySide6.QtCore import (
    Qt,
    QSize
)

from PySide6.QtGui import (
    QIcon
)


from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox
)

from views.seleccion_area import (
    SeleccionAreaView
)

from widgets.hover_card import (
    HoverCard
)

from PySide6.QtGui import (
    QIcon,
    QPixmap
)

from views.evaluaciones_view import(
    EvaluacionesView
)

from views.proveedores_view import (
    ProveedoresView
)

from views.proveedor_dialog import ProveedorDialog
from repositories.prestador_repository import PrestadorRepository

from views.proveedor_form_view import ProveedorFormView
from repositories.prestador_repository import PrestadorRepository

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ventana_actual = None

        self.base_dir = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        self.icons_dir = (
            self.base_dir
            / "resources"
            / "icons"
        )

        self.images_dir = (
            self.base_dir
            / "resources"
            / "images"
        )

        self.configurar_ventana()
        self.crear_interfaz()

    # ==================================================
    # CONFIGURACIÓN GENERAL
    # ==================================================

    def configurar_ventana(self):

        self.setWindowTitle(
            "Sistema de Gestión y Evaluación de Ofertas"
        )

        self.resize(
            1200,
            750
        )

        self.setMinimumSize(
            1000,
            650
        )

    # ==================================================
    # INTERFAZ PRINCIPAL
    # ==================================================

    def crear_interfaz(self):

        contenedor = QWidget()

        layout_principal = QHBoxLayout(
            contenedor
        )

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
        # MENÚ LATERAL
        # ==============================================

        menu = self.crear_menu_lateral()

        layout_principal.addWidget(
            menu
        )

        # ==============================================
        # ÁREA CENTRAL
        # ==============================================

        self.contenido = QWidget()

        self.contenido.setObjectName(
            "contenidoPrincipal"
        )

        self.layout_contenido = QVBoxLayout(
            self.contenido
        )

        self.layout_contenido.setContentsMargins(
            40,
            35,
            40,
            35
        )

        self.layout_contenido.setSpacing(
            0
        )

        layout_principal.addWidget(
            self.contenido,
            1
        )

        self.setCentralWidget(
            contenedor
        )

        # ==============================================
        # PÁGINA INICIAL
        # ==============================================

        self.mostrar_inicio()

    # ==================================================
    # MENÚ LATERAL
    # ==================================================

    def crear_menu_lateral(self):

        menu = QFrame()

        menu.setObjectName(
            "menuLateral"
        )

        menu.setFixedWidth(
            240
        )

        layout = QVBoxLayout(
            menu
        )

        layout.setContentsMargins(
            20,
            18,
            20,
            20
        )

        layout.setSpacing(
            10
        )

        # ----------------------------------------------
        # LOGOTIPO INSTITUCIONAL
        # ----------------------------------------------

        logo = QLabel()

        logo.setObjectName(
            "logoInstitucional"
        )

        logo.setAlignment(
            Qt.AlignCenter
        )

        ruta_logo = (
            self.images_dir
            / "logo_dif_t.png"
        )

        if ruta_logo.exists():

            pixmap = QPixmap(
                str(ruta_logo)
            )

            pixmap = pixmap.scaled(
                130,
                85,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            logo.setPixmap(
                pixmap
            )

        layout.addWidget(
            logo
        )

        layout.addSpacing(
            6
        )

        # ----------------------------------------------
        # IDENTIDAD DEL SISTEMA
        # ----------------------------------------------

        titulo = QLabel(
            "GESTIÓN DE OFERTAS"
        )

        titulo.setObjectName(
            "tituloMenu"
        )

        titulo.setWordWrap(
            True
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )


        subtitulo = QLabel(
            "Panel Principal"
        )

        subtitulo.setObjectName(
            "subtituloMenu"
        )

        subtitulo.setAlignment(
            Qt.AlignCenter
        )


        layout.addWidget(
            titulo
        )

        layout.addWidget(
            subtitulo
        )

        layout.addSpacing(
            15
        )

        # ----------------------------------------------
        # BOTONES DEL MENÚ
        # ----------------------------------------------

        self.boton_inicio = QPushButton(
            "Inicio"
        )

        self.boton_evaluaciones = QPushButton(
            "Evaluaciones de ofertas"
        )

        self.boton_proveedores = QPushButton(
            "Proveedores"
        )

        self.boton_documentos = QPushButton(
            "Documentos"
        )

        self.asignar_icono(
            self.boton_inicio,
            "inicio.svg", 
            19
        )

        self.asignar_icono(
            self.boton_evaluaciones,
            "evaluacion.svg"
        )

        self.asignar_icono(
            self.boton_proveedores,
            "proveedor.svg"
        )

        self.asignar_icono(
            self.boton_documentos,
            "documento.svg"
        )




        self.botones_menu = [
            self.boton_inicio,
            self.boton_evaluaciones,
            self.boton_proveedores,
            self.boton_documentos
        ]


        for boton in self.botones_menu:

            boton.setMinimumHeight(
                46
            )

            boton.setCursor(
                Qt.PointingHandCursor
            )

            layout.addWidget(
                boton
            )

        # ----------------------------------------------
        # ESPACIO FLEXIBLE
        # ----------------------------------------------

        layout.addStretch()

        # ----------------------------------------------
        # BOTÓN SALIR
        # ----------------------------------------------

        self.boton_salir = QPushButton(
            "Salir"
        )

        self.boton_salir.setObjectName(
            "botonSalir"
        )

        self.boton_salir.setMinimumHeight(
            42
        )

        self.boton_salir.setCursor(
            Qt.PointingHandCursor
        )

        self.asignar_icono(
            self.boton_salir,
            "salir.svg"
        )
        
        layout.addWidget(
            self.boton_salir
        )

        # ----------------------------------------------
        # EVENTOS
        # ----------------------------------------------

        self.boton_inicio.clicked.connect(
            self.mostrar_inicio
        )

        self.boton_evaluaciones.clicked.connect(
            self.mostrar_evaluaciones
        )

        self.boton_proveedores.clicked.connect(
            self.mostrar_proveedores
        )

        self.boton_documentos.clicked.connect(
            self.modulo_pendiente
        )

        self.boton_salir.clicked.connect(
            self.close
        )

        return menu

    def asignar_icono(
        self,
        boton,
        nombre_archivo,
        tamaño=20
    ):

        ruta = (
            self.icons_dir
            / nombre_archivo
        )

        if ruta.exists():

            boton.setIcon(
                QIcon(
                    str(ruta)
                )
            )

            boton.setIconSize(
                QSize(
                    16,
                    16
                )
            )

    # ==================================================
    # ACTUALIZAR BOTÓN ACTIVO DEL MENÚ
    # ==================================================

    
    def actualizar_menu_activo(
        self,
        boton_activo
    ):

        for boton in self.botones_menu:

            boton.setProperty(
                "activo",
                False
            )

            boton.style().unpolish(
                boton
            )

            boton.style().polish(
                boton
            )

        boton_activo.setProperty(
            "activo",
            True
        )

        boton_activo.style().unpolish(
            boton_activo
        )

        boton_activo.style().polish(
            boton_activo
        )

    # ==================================================
    # LIMPIAR CONTENIDO CENTRAL
    # ==================================================

    def limpiar_contenido(self):

        while self.layout_contenido.count():

            item = (
                self.layout_contenido
                .takeAt(0)
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

                continue

            layout = item.layout()

            if layout is not None:

                self.eliminar_layout(
                    layout
                )

    # ==================================================
    # ELIMINAR LAYOUTS INTERNOS
    # ==================================================

    def eliminar_layout(
        self,
        layout
    ):

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

            layout_hijo = item.layout()

            if layout_hijo is not None:

                self.eliminar_layout(
                    layout_hijo
                )

    # ==================================================
    # TARJETA DE MÓDULO
    # ==================================================

    def crear_tarjeta_modulo(
        self,
        titulo,
        descripcion,
        callback, 
        icono=None
    ):  

        tarjeta = HoverCard()

        tarjeta.setObjectName(
            "tarjetaModulo"
        )

        tarjeta.clicked.connect(
            callback
        )

        tarjeta.setCursor(
            Qt.PointingHandCursor
        )

        tarjeta.setMinimumHeight(
            175
        )

        tarjeta.clicked.connect(
            callback
        )

        layout = QVBoxLayout(
            tarjeta
        )

        layout.setContentsMargins(
            24,
            22,
            24,
            20
        )

        layout.setSpacing(
            8
        )

        # ----------------------------------------------
        # TÍTULO
        # ----------------------------------------------

        titulo_label = QLabel(
            titulo
        )

        titulo_label.setObjectName(
            "tituloTarjeta"
        )

        # ----------------------------------------------
        # DESCRIPCIÓN
        # ----------------------------------------------

        descripcion_label = QLabel(
            descripcion
        )

        descripcion_label.setObjectName(
            "descripcionTarjeta"
        )

        descripcion_label.setWordWrap(
            True
        )

        # ----------------------------------------------
        # BOTÓN
        # ----------------------------------------------

        boton = QPushButton(
            "Abrir módulo  →"
        )

        boton.setObjectName(
            "botonSecundario"
        )

        boton.setCursor(
            Qt.PointingHandCursor
        )

        boton.setMinimumHeight(
            36
        )

        if icono:
            self.asignar_icono(
                boton,
                icono,
                16
            )

        boton.clicked.connect(
            callback
        )

        # ----------------------------------------------
        # AGREGAR ELEMENTOS
        # ----------------------------------------------

        layout.addWidget(
            titulo_label
        )

        layout.addWidget(
            descripcion_label
        )

        layout.addStretch()

        layout.addWidget(
            boton,
            alignment=Qt.AlignLeft
        )

        return tarjeta

    # ==================================================
    # DASHBOARD / INICIO
    # ==================================================

    def mostrar_inicio(self):

        self.actualizar_menu_activo(
            self.boton_inicio
        )

        self.limpiar_contenido()

        # ==============================================
        # ENCABEZADO
        # ==============================================

        titulo = QLabel(
            "Panel principal"
        )

        titulo.setObjectName(
            "tituloPagina"
        )


        descripcion = QLabel(
            "Gestione evaluaciones de ofertas, "
            "proveedores y documentos administrativos."
        )

        descripcion.setObjectName(
            "descripcionPagina"
        )

        descripcion.setWordWrap(
            True
        )


        self.layout_contenido.addWidget(
            titulo
        )

        self.layout_contenido.addWidget(
            descripcion
        )

        self.layout_contenido.addSpacing(
            30
        )

        # ==============================================
        # TARJETA NUEVA EVALUACIÓN
        # ==============================================

        tarjeta_nueva = HoverCard()

        tarjeta_nueva.setObjectName(
            "tarjetaPrincipal"
        )


        layout_tarjeta = QHBoxLayout(
            tarjeta_nueva
        )

        layout_tarjeta.setContentsMargins(
            28,
            24,
            28,
            24
        )

        layout_tarjeta.setSpacing(
            20
        )

        # ----------------------------------------------
        # INFORMACIÓN
        # ----------------------------------------------

        contenido_tarjeta = QVBoxLayout()

        contenido_tarjeta.setSpacing(
            7
        )


        titulo_nueva = QLabel(
            "Nueva evaluación de ofertas"
        )

        titulo_nueva.setObjectName(
            "tituloTarjeta"
        )


        descripcion_nueva = QLabel(
            "Inicie un nuevo proceso para registrar "
            "proveedores, comparar sus ofertas y generar "
            "el documento administrativo correspondiente."
        )

        descripcion_nueva.setObjectName(
            "descripcionTarjeta"
        )

        descripcion_nueva.setWordWrap(
            True
        )


        contenido_tarjeta.addWidget(
            titulo_nueva
        )

        contenido_tarjeta.addWidget(
            descripcion_nueva
        )

        # ----------------------------------------------
        # BOTÓN PRINCIPAL
        # ----------------------------------------------

        boton_nueva = QPushButton(
            "+  Nueva evaluación"
        )

        boton_nueva.setObjectName(
            "botonPrimario"
        )

        boton_nueva.setCursor(
            Qt.PointingHandCursor
        )

        boton_nueva.setMinimumSize(
            185,
            44
        )

        boton_nueva.clicked.connect(
            self.nueva_evaluacion
        )


        layout_tarjeta.addLayout(
            contenido_tarjeta,
            1
        )

        layout_tarjeta.addWidget(
            boton_nueva,
            alignment=Qt.AlignVCenter
        )


        self.layout_contenido.addWidget(
            tarjeta_nueva
        )

        self.layout_contenido.addSpacing(
            30
        )

        # ==============================================
        # MÓDULOS PRINCIPALES
        # ==============================================

        titulo_modulos = QLabel(
            "Módulos principales"
        )

        titulo_modulos.setObjectName(
            "subtituloPagina"
        )


        self.layout_contenido.addWidget(
            titulo_modulos
        )

        self.layout_contenido.addSpacing(
            12
        )

        # ==============================================
        # TARJETAS DE MÓDULOS
        # ==============================================

        layout_modulos = QHBoxLayout()

        layout_modulos.setSpacing(
            18
        )


        tarjeta_evaluaciones = (
            self.crear_tarjeta_modulo(
                "Evaluaciones",
                "Consulte y gestione los procesos "
                "de evaluación de ofertas.",
                self.mostrar_evaluaciones,
                "evaluacion.svg"
            )
        )


        tarjeta_proveedores = (
            self.crear_tarjeta_modulo(
                "Proveedores",
                "Administre la información de los "
                "proveedores registrados.",
                self.modulo_pendiente,
                "proveedor.svg"
            )
        )


        tarjeta_documentos = (
            self.crear_tarjeta_modulo(
                "Documentos",
                "Consulte los Estudios de Mercado "
                "generados por el sistema.",
                self.modulo_pendiente,
                "documento.svg"
            )
        )


        layout_modulos.addWidget(
            tarjeta_evaluaciones,
            1
        )

        layout_modulos.addWidget(
            tarjeta_proveedores,
            1
        )

        layout_modulos.addWidget(
            tarjeta_documentos,
            1
        )


        self.layout_contenido.addLayout(
            layout_modulos
        )

        self.layout_contenido.addStretch()

    # ==================================================
    # PÁGINA DE EVALUACIONES
    # ==================================================

    def mostrar_evaluaciones(self):

        self.actualizar_menu_activo(
            self.boton_evaluaciones
        )

        self.limpiar_contenido()

        # ==============================================
        # CREAR VISTA DE EVALUACIONES
        # ==============================================

        self.vista_evaluaciones = (
            EvaluacionesView()
        )

        # ==============================================
        # EVENTOS
        # ==============================================

        self.vista_evaluaciones.nueva_evaluacion_solicitada.connect(
            self.nueva_evaluacion
        )

        self.vista_evaluaciones.ver_evaluacion_solicitada.connect(
            self.ver_evaluacion
        )

        # ==============================================
        # AGREGAR AL CONTENIDO PRINCIPAL
        # ==============================================

        self.layout_contenido.addWidget(
            self.vista_evaluaciones
        )



        #self.layout_contenido.addStretch()

    def ver_evaluacion(
        self,
        estudio_id
    ):

        QMessageBox.information(
            self,
            "Evaluación",
            f"Se seleccionó la evaluación con ID: {estudio_id}"
        )

    # ==================================================
    # NUEVA EVALUACIÓN
    # ==================================================

    def nueva_evaluacion(self):

        self.ventana_actual = (
            SeleccionAreaView()
        )

        self.ventana_actual.show()

    # ==================================================
    # MÓDULO PENDIENTE
    # ==================================================

    def modulo_pendiente(self):

        QMessageBox.information(
            self,
            "Módulo en desarrollo",
            "Este módulo será incorporado "
            "en una etapa posterior."
        )

    # ==================================================
    # PÁGINA DE PROVEEDORES
    # ==================================================

    def mostrar_proveedores(self):

        self.actualizar_menu_activo(
            self.boton_proveedores
        )

        self.limpiar_contenido()

        # ==============================================
        # CREAR VISTA
        # ==============================================

        self.vista_proveedores = (
            ProveedoresView()
        )

        # ==============================================
        # EVENTOS
        # ==============================================

        self.vista_proveedores.nuevo_proveedor_solicitado.connect(
            self.nuevo_proveedor
        )

        self.vista_proveedores.ver_proveedor_solicitado.connect(
            self.ver_proveedor
        )

        self.vista_proveedores.editar_proveedor_solicitado.connect(
            self.editar_proveedor
        )

        # ==============================================
        # AGREGAR VISTA
        # ==============================================

        self.layout_contenido.addWidget(
            self.vista_proveedores
        )


    def nuevo_proveedor(self):

        self.limpiar_contenido()

        self.formulario_proveedor = ProveedorFormView()

        self.formulario_proveedor.guardar_solicitado.connect(
            self.guardar_proveedor
        )

        self.formulario_proveedor.cancelar_solicitado.connect(
            self.mostrar_proveedores
        )

        self.layout_contenido.addWidget(
            self.formulario_proveedor
        )




    def ver_proveedor(self, proveedor_id):

        self.abrir_proveedor(
            proveedor_id,
            "ver"
        )


    def editar_proveedor(self, proveedor_id):

        self.abrir_proveedor(
            proveedor_id,
            "editar"
        )


    def abrir_proveedor(self, proveedor_id, modo):

        try:

            repositorio = PrestadorRepository()

            prestador = repositorio.obtener_por_id(
                proveedor_id
            )

            if prestador is None:

                self.mostrar_proveedores()
                return

        except Exception as error:

            print(
                f"Error al consultar proveedor: {error}"
            )

            self.mostrar_proveedores()
            return

        self.limpiar_contenido()

        self.formulario_proveedor = ProveedorFormView(
            prestador=prestador,
            modo=modo
        )

        self.formulario_proveedor.cancelar_solicitado.connect(
            self.mostrar_proveedores
        )

        if modo == "editar":

            self.formulario_proveedor.guardar_solicitado.connect(
                lambda datos, id_proveedor=proveedor_id:
                self.actualizar_proveedor(
                    id_proveedor,
                    datos
                )
            )

        self.layout_contenido.addWidget(
            self.formulario_proveedor
        )


    def actualizar_proveedor(self, proveedor_id, datos):

        try:

            repositorio = PrestadorRepository()

            repositorio.actualizar(
                proveedor_id,
                **datos
            )

        except ValueError as error:

            self.formulario_proveedor.mostrar_error(
                str(error)
            )

            return

        except Exception as error:

            print(
                f"Error al actualizar proveedor: {error}"
            )

            self.formulario_proveedor.mostrar_error(
                "No fue posible actualizar el proveedor. "
                "Verifica los datos e inténtalo nuevamente."
            )

            return

        self.mostrar_proveedores()


    def guardar_proveedor(self, datos):

        try:

            repositorio = PrestadorRepository()

            repositorio.crear(**datos)

        except ValueError as error:

            self.formulario_proveedor.mostrar_error(
                str(error)
            )

            return

        except Exception as error:

            print(
                f"Error al guardar proveedor: {error}"
            )

            self.formulario_proveedor.mostrar_error(
                "No fue posible guardar el proveedor. "
                "Verifica los datos e inténtalo nuevamente."
            )

            return

        # Regresar a la tabla actualizada
        self.mostrar_proveedores()