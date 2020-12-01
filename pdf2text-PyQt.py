from PyQt5.QtWidgets import *

if __name__ == '__main__':
	app = QApplication([])
	window = QWidget()
	
	layoutH = QHBoxLayout()
	layoutV1 = QVBoxLayout()
	layoutV2 = QVBoxLayout()

	layoutV1.addWidget(QPushButton("Add pdf"))
	layoutV1.addWidget(QLabel("bla"))
	layoutV2.addWidget(QPushButton('Export to txt'))
	layoutV2.addWidget(QLabel('blabla'))

	layoutH.addLayout(layoutV1)
	layoutH.addLayout(layoutV2)

	window.setLayout(layoutH)
	
	window.setWindowTitle("pdf2Text-PyQt")
	window.show()

	app.exec_()
