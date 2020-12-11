from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pdf2image import convert_from_path 
import signal
import os

try:
    from PIL import Image
except ImportError:
    import Image
    
import pytesseract

signal.signal(signal.SIGINT, signal.SIG_DFL)

"""
TODO

 Done Export -> window with all/single export, location
 Done Menu bar -> language, about...
 Convert as a backgound task
 Only show available Languages

"""


# Custom widget for the list
class CustomQWidget(QWidget):
	def __init__(self, parent=None, connected_item=None, filepath=None):
		super(CustomQWidget, self).__init__(parent)

		self.connected_item = connected_item

		label = QLabel(QFileInfo(filepath).fileName())

		button_close = QPushButton()
		button_close.setIcon(QIcon("close.png"))
		button_close.setMaximumWidth(24)
		button_close.clicked.connect(lambda: removeListItem(button_close))
		
		layout = QHBoxLayout()
		layout.addWidget(label)
		layout.addWidget(button_close)

		self.setLayout(layout)
		
def removeListItem(button_close):
	print(button_close.parent().content)
	
	item = button_close.parent().connected_item
	
	if item.isSelected():
		textEdit.clear()

	listWidget.removeItemWidget(item)
	listWidget.takeItem(listWidget.indexFromItem(item).row())
	
def listItemClicked(item):
	if item != None:
		textEdit.setPlainText(listWidget.itemWidget(item).content)


class Worker(QObject):
	finished = pyqtSignal()
	intReady = pyqtSignal(int)

	def __init__(self, filepath, widget):
		super().__init__()
	
		self.filepath = filepath
		self.widget = widget

	@pyqtSlot()
	def proc_convert_to_text(self):
		# PDF or IMG to TEXT conversion 
		filetype = os.path.splitext(self.filepath)[1]
		
		print("Start Converting...")

		self.widget.content = ""

		if filetype == ".pdf":
			# Store Pdf with convert_from_path function 
			images = convert_from_path(self.filepath) 
			for img in images: 
				self.widget.content += pytesseract.image_to_string(img, lang=exportSettings['Language'])

		else:
			# Text conversion
			self.widget.content += pytesseract.image_to_string(Image.open(self.filepath), lang=exportSettings['Language'])

		print("Done Converting.")

		self.finished.emit()


class PopUpProgressB(QDialog):

	def __init__(self, filenames):
		super().__init__()
		self.pbar = QProgressBar(self)
		self.pbar.setGeometry(30, 40, 500, 75)
		self.pbar.setMaximum(len(filenames))
		self.count = 0
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.pbar)
		self.setLayout(self.layout)
		self.setGeometry(300, 300, 550, 100)
		self.setWindowTitle('Progress Bar')
		self.show()
		
		self.threads = []
		self.objs = []

		for filepath in filenames:
		
			item = QListWidgetItem(listWidget)
			item_widget = CustomQWidget(connected_item=item, filepath=filepath)
			item.setSizeHint(item_widget.sizeHint())
			listWidget.addItem(item)
			listWidget.setItemWidget(item, item_widget)

			obj = Worker(filepath, item_widget)
			thread = QThread()
			
			obj.moveToThread(thread)
			obj.finished.connect(thread.quit)
			obj.finished.connect(self.thread_finished)
			thread.started.connect(obj.proc_convert_to_text)
			thread.start()
			
			self.threads.append(thread)
			self.objs.append(obj)

	def thread_finished(self):
		self.count += 1
		self.pbar.setValue(self.count)
		
		if (self.count >= self.pbar.maximum()):
			self.hide()
			
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
		print("Files:" + str(filenames))

		popup = PopUpProgressB(filenames)
		popup.exec()

def textEditChanged():
	item = listWidget.currentItem()
	if item != None:
		listWidget.itemWidget(item).content = textEdit.toPlainText()

exportSettings = {'AllFiles': False, 'FilePath': None, 'FileName': "New.txt", 'Language': "eng"}

class CustomDialog(QDialog):
	def __init__(self, *args, **kwargs):
		super(CustomDialog, self).__init__(*args, **kwargs)

		self.setWindowTitle("Export to textfile")

		self.b1 = QRadioButton("Export all files")
		self.b1.setChecked(True)
		self.b1.toggled.connect(self.onClicked)
		self.b2 = QRadioButton("Export this file")
		self.b2.setChecked(False)
		self.b2.toggled.connect(self.onClicked)
		

		self.textBox = QLineEdit()
		self.textBox.setPlaceholderText("file name")
		self.textBox.textChanged.connect(self.textChanged)
		
		self.button_path = QPushButton("Select path")
		self.button_path.clicked.connect(self.selectPath)

		buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

		self.buttonBox = QDialogButtonBox(buttons)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.b1)
		self.layout.addWidget(self.b2)
		self.layout.addWidget(self.textBox)
		self.layout.addWidget(self.button_path)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)
		
	def onClicked(self):
		global exportSettings
		if self.b1.isChecked():
			exportSettings['AllFiles'] = False
		elif self.b2.isChecked():
			exportSettings['AllFiles'] = True
		print(exportSettings['AllFiles'])

	def textChanged(self):
		global exportSettings
		exportSettings['FileName'] = self.textBox.text()
		if exportSettings['FileName'].endswith(".txt") == False:
			exportSettings['FileName'] += ".txt"
	
	def selectPath(self):
		global exportSettings
		
		self.dir_path=QFileDialog.getExistingDirectory(self,"Choose Directory","~\\")
		exportSettings['FilePath'] = self.dir_path
		print(exportSettings['FilePath'])

def exportTxt():
	dlg = CustomDialog()
	Text = ""
	print(exportSettings['AllFiles'])
	if dlg.exec_():
		print("Success!")
		
		# export one or all files
		if exportSettings['AllFiles'] == False: 
			fo = open((exportSettings['FilePath']+"/"+exportSettings['FileName']), "w+")
			#Text = ""
			for i in range(listWidget.count()):
				item = listWidget.item(i)
				Text += listWidget.itemWidget(item).content
				print (Text)
			fo.write(Text)
			fo.close()
		elif exportSettings['AllFiles'] == True:
			fo = open(exportSettings['FileName'], "w+")
			#Text = ""
			print(Text)
			Text = textEdit.toPlainText()
			fo.write(Text)
			fo.close()

	else:
		print("Cancel!")

def DeuLanguage():
	global exportSettings
	exportSettings['Language'] = "deu"
	print(exportSettings['Language'])
		
def EngLanguage():
	global exportSettings
	exportSettings['Language'] = "eng"
	print(exportSettings['Language'])


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
	layoutV = QVBoxLayout()
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
	
		# Menubar
	menubar = QMenuBar()
	layoutV.addWidget(menubar)
	menubar.addMenu("Info")
	SettingsMenu = menubar.addMenu("Settings")
	OpenButton = QAction("Open")
	OpenButton.triggered.connect(addPdf)
	SettingsMenu.addAction(OpenButton)
	LanguageMenu = SettingsMenu.addMenu("Language")
	DeuButton = QAction("Deutsch")
	LanguageMenu.addAction(DeuButton)
	DeuButton.triggered.connect(DeuLanguage)
	EngButton = QAction("Englisch")
	LanguageMenu.addAction(EngButton)
	EngButton.triggered.connect(EngLanguage)

	# Create textEdit
	textEdit = QTextEdit()
	textEdit.setPlainText("")
	layoutV2.addWidget(textEdit)
	
	# Save changes at textEdit
	textEdit.textChanged.connect(textEditChanged)
	
	# Add layouts
	layoutV.addLayout(layoutH)
	layoutH.addLayout(layoutV1)
	layoutH.addLayout(layoutV2)

	window.setLayout(layoutV)
	
	window.setWindowTitle("pdf2Text-PyQt")
	window.show()

	app.exec_()
