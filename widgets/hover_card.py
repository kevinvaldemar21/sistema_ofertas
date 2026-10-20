from PySide6.QtCore import (
    Signal
)

from PySide6.QtWidgets import (
    QFrame
)


class HoverCard(QFrame):

    clicked = Signal()

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setProperty(
            "hover",
            False
        )

        self.setCursor(
            self.cursor()
        )

    def enterEvent(
        self,
        event
    ):

        self.setProperty(
            "hover",
            True
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        super().enterEvent(
            event
        )

    def leaveEvent(
        self,
        event
    ):

        self.setProperty(
            "hover",
            False
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        super().leaveEvent(
            event
        )

    def mousePressEvent(
        self,
        event
    ):

        self.clicked.emit()

        super().mousePressEvent(
            event
        )