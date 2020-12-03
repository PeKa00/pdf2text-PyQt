from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import signal

try:
    from PIL import Image
except ImportError:
    import Image
    
import pytesseract

signal.signal(signal.SIGINT, signal.SIG_DFL)

# Custom widget for the list
class CustomQWidget(QWidget):
	def __init__(self, parent=None, filepath=None):
		super(CustomQWidget, self).__init__(parent)

		label = QLabel(filepath)

		button = QPushButton()
		button.setIcon(QIcon("close.png"))
		button.setMaximumWidth(24)
		
		
		# TODO we have to check if the path points to an image or PDF
		# For a PDF convert the PDF to images and for every image convert to text -> append to self.content
		# For an image directly convert to text and set self.content
		
		# Text conversion
		self.content = "Content: \n" + pytesseract.image_to_string(Image.open(filepath))

		layout = QHBoxLayout()
		layout.addWidget(label)
		layout.addWidget(button)

		self.setLayout(layout)
		
def removeListItem(status, button):
	# TODO .parent()
	button.parent()
	
def listItemClicked(item):
	textEdit.setPlainText(listWidget.itemWidget(item).content)
	

def addPdf():
	dialog = QFileDialog()
	dialog.setWindowTitle('Open PDF Files')
	
	filters = [ "PDF files (*.pdf)",
	"Image files (*.png *.xpm *.jpg)",
	"Any files (*)" ]
	
	dialog.setNameFilters(filters)
	dialog.setDirectory(QDir.homePath()) #currentPath()
	dialog.setFileMode(QFileDialog.ExistingFiles)
	filename = None
	if dialog.exec_() == QDialog.Accepted:
		filenames = dialog.selectedFiles()
		print(filenames)
		
		for filepath in filenames:
			item = QListWidgetItem(listWidget)
			item_widget = CustomQWidget(filepath=filepath)
			item.setSizeHint(item_widget.sizeHint())
			listWidget.addItem(item)
			listWidget.setItemWidget(item, item_widget)
	
def exportTxt():
	fo = open("name.txt", "w+")
	fo.write(textEdit.toPlainText())
	fo.close()

if __name__ == '__main__':
	app = QApplication([])
	window = QWidget()
	
	window.setMinimumSize(500,300)
	
	# Move window to the screen center
	qtRectangle = window.frameGeometry()
	centerPoint = QDesktopWidget().availableGeometry().center()
	qtRectangle.moveCenter(centerPoint)
	window.move(qtRectangle.topLeft())

	# Create layouts
	layoutH = QHBoxLayout()
	layoutV1 = QVBoxLayout()
	layoutV2 = QVBoxLayout()

	# --- Left side

	button_pdf = QPushButton("Add PDF or image file")
	layoutV1.addWidget(button_pdf)
	button_pdf.clicked.connect(addPdf)
	
	# Create list
	listWidget = QListWidget()
	listWidget.currentItemChanged.connect(listItemClicked)
	layoutV1.addWidget(listWidget)
	
	# --- Right side
	button_export = QPushButton('Export to textfile')
	layoutV2.addWidget(button_export)
	button_export.clicked.connect(exportTxt)
	
	# Create textEdit
	textEdit = QTextEdit()
	textEdit.setPlainText("")
	layoutV2.addWidget(textEdit)
	
	# Add layouts
	layoutH.addLayout(layoutV1)
	layoutH.addLayout(layoutV2)

	window.setLayout(layoutH)
	
	window.setWindowTitle("pdf2Text-PyQt")
	window.show()

	app.exec_()
