from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Custom widget for the list
class CustomQWidget(QWidget):
	def __init__(self, parent=None, text="empty"):
		super(CustomQWidget, self).__init__(parent)

		label = QLabel(text)

		button = QPushButton()
		button.setIcon(QIcon("close.png"))

		layout = QHBoxLayout()
		layout.addWidget(label)
		layout.addWidget(button)

		self.setLayout(layout)

def addPdf():
	textEdit.setPlainText("add Pdf")
	
def exportTxt():
	fo = open("name", "w+")
	fo.write(textEdit.toPlainText())
	fo.close()

if __name__ == '__main__':
	app = QApplication([])
	window = QWidget()

	# Create layouts
	layoutH = QHBoxLayout()
	layoutV1 = QVBoxLayout()
	layoutV2 = QVBoxLayout()

	# --- Left side

	button_pdf = QPushButton("Add pdf")
	layoutV1.addWidget(button_pdf)
	button_pdf.clicked.connect(addPdf)
	
	# Create list
	listWidget = QListWidget()
	layoutV1.addWidget(listWidget)
	
	# Add list items
	for i in range(0, 5):
		item = QListWidgetItem(listWidget)
		item_widget = CustomQWidget(text="Hello everyone " + str(i))
		item.setSizeHint(item_widget.sizeHint())
		listWidget.addItem(item)
		listWidget.setItemWidget(item, item_widget)
	
	# --- Right side
	button_export = QPushButton('Export to txt')
	layoutV2.addWidget(button_export)
	button_export.clicked.connect(exportTxt)
	
	# Create textEdit
	textEdit = QTextEdit()
	textEdit.setPlainText("Hello World")
	layoutV2.addWidget(textEdit)
	
	

	layoutH.addLayout(layoutV1)
	layoutH.addLayout(layoutV2)

	window.setLayout(layoutH)
	
	window.setWindowTitle("pdf2Text-PyQt")
	window.show()

	app.exec_()
