from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QDialog,
    QLabel,
    QVBoxLayout,
    QStyle,
)


class WindowInfo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.info()

    def info(self):
        self.setWindowTitle("Important Information!")

        icon_label = QLabel()
        style = QApplication.style()
        pixmap = style.standardPixmap(QStyle.SP_MessageBoxWarning)
        big_pix = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(big_pix)

        text_label = QLabel(
            "BE AWARE!\n" "DO NOT INTERACT WITH THE MARKET WHILE SCRAPING!"
        )

        buttons = QDialogButtonBox(QDialogButtonBox.Ok, self)
        btn = buttons.button(QDialogButtonBox.Ok)
        btn.setText("Got it!")
        buttons.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addWidget(buttons)
        self.setGeometry(400, 400, 300, 150)

    def get_result(self):
        return self.exec_() == QDialog.Accepted
