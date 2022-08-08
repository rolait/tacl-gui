from PyQt5.QtWidgets import QMessageBox


class ExceptionHandler:

    def handle(self, exception: Exception, stackTrace: str):
        logMessage: str = "{}\n{}".format(str(exception), stackTrace)
        print(logMessage)

        errorBox = QMessageBox()
        errorBox.setIcon(QMessageBox.Critical)
        errorBox.setWindowTitle("TACL-GUI 鬼")
        errorBox.setText("An unexpected error was encountered.")
        errorBox.setInformativeText(str(exception))
        errorBox.setDetailedText(stackTrace)
        errorBox.exec_()