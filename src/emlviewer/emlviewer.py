from email import policy
from email.message import EmailMessage
from email.parser import BytesParser

from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QBoxLayout, QMainWindow, QTextBrowser, QTreeView, QWidget


class EMLViewer(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setCentralWidget(centralWidget := QWidget())

        centralWidget.setLayout(layout := QBoxLayout(QBoxLayout.Direction.TopToBottom))
        layout.addWidget(headerView := QTreeView())
        layout.addWidget(bodyView := QTextBrowser())

        headerView.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        headerView.setRootIsDecorated(False)
        headerView.setFixedHeight(200)

        self.resize(600, 800)

        self.headerView = headerView
        self.bodyView = bodyView

    def open(self, path: str) -> None:
        headerModel: QStandardItemModel = QStandardItemModel()
        headerModel.setHorizontalHeaderLabels(["Key", "Value"])

        with open(path, "rb") as fp:
            message: EmailMessage = BytesParser(policy=policy.default).parse(fp)
        
        for key, value in message.items():
            row: list[QStandardItem] = [
                QStandardItem(str(key)),
                QStandardItem(str(value)),
            ]
            headerModel.appendRow(row)
        self.headerView.setModel(headerModel)
        self.headerView.setColumnWidth(0, 150)

        if (body := message.get_body()) is not None:
            self.bodyView.setHtml(body.get_content())
