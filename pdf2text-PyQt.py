from PyQt5.QtWidgets import *

# Custom widget for the list
class CustomQWidget(QWidget):
	def __init__(self, parent=None, text="empty"):
		super(CustomQWidget, self).__init__(parent)

		label = QLabel(text)

		button = QPushButton("Button")
		# button.setIcon(QIcon("close.png"))

		layout = QHBoxLayout()
		layout.addWidget(label)
		layout.addWidget(button)

		self.setLayout(layout)

if __name__ == '__main__':
	app = QApplication([])
	window = QWidget()
	
	layoutH = QHBoxLayout()
	layoutV1 = QVBoxLayout()
	layoutV2 = QVBoxLayout()

	layoutV1.addWidget(QPushButton("Add pdf"))
	layoutV1.addWidget(QLabel("bla"))
	
	listWidget = QListWidget()
	layoutV1.addWidget(listWidget)
	
	for i in range(0, 5):
	
		item = QListWidgetItem(listWidget)
		item_widget = CustomQWidget(text="Hello everyone " + str(i))
		item.setSizeHint(item_widget.sizeHint())
		listWidget.addItem(item)
		listWidget.setItemWidget(item, item_widget)
	
	
	layoutV2.addWidget(QPushButton('Export to txt'))
	layoutV2.addWidget(QLabel('blabla'))

	layoutH.addLayout(layoutV1)
	layoutH.addLayout(layoutV2)

	window.setLayout(layoutH)
	
	window.setWindowTitle("pdf2Text-PyQt")
	window.show()

	app.exec_()
