from PyQt5.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QDialog,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QLineEdit,
)
import sys


class WindowContinue(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_field = QLineEdit()
        self.pop_up_info()

    def pop_up_info(self):
        self.setWindowTitle("Important Information!")

        input_label = QLabel("Enter the name of the output file:")
        message = QLabel(
            "If you want to continue extracting data\ngo to the category and press continue.\nIf not, press Exit to finish extraction"
        )

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.button(QDialogButtonBox.Ok).setText("Continue")
        buttons.button(QDialogButtonBox.Cancel).setText("Exit")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(input_label)
        layout.addWidget(self.input_field)
        layout.addWidget(message)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self.setGeometry(400, 400, 300, 150)

    def get_result(self):
        code = self.exec_()
        if code == QDialog.Accepted:
            return self.input_field.text()
        return None
