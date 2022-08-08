from PyQt5.QtWidgets import QMenu, QMenuBar, QAction


class MainMenuBar(QMenuBar):

    def __init__(self):
        super().__init__()

        self._initFileMenu()

    def _initFileMenu(self):
        self._generateAction = QAction()
        self._importAction = QAction()
        self._selectAction = QAction()
        self._exitAction = QAction()

        self._fileMenu = QMenu()
        self._fileMenu.addAction(self._selectAction)
        self._fileMenu.addAction(self._importAction)
        self._fileMenu.addAction(self._generateAction)
        self._fileMenu.addSeparator()
        self._fileMenu.addAction(self._exitAction)

        self.addMenu(self._fileMenu)


    def updateTranslations(self):
        self._fileMenu.setTitle(self.tr("&File"))
        self._generateAction.setText(self.tr("&Generate Database") + "...")
        self._importAction.setText(self.tr("&Import Database") + "...")
        self._selectAction.setText(self.tr("&Select Database") + "...")
        self._exitAction.setText(self.tr("&Exit"))

    def getGenerateAction(self) -> QAction:
        return self._generateAction

    def getImportAction(self) -> QAction:
        return self._importAction

    def getSelectAction(self) -> QAction:
        return self._selectAction

    def getExitAction(self) -> QAction:
        return self._exitAction