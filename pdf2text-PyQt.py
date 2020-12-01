from PyQt5.QtWidgets import *

if __name__ == '__main__':
	app = QApplication([])
	window = QWidget()

	window.setWindowTitle("pdf2Text-PyQt")
	window.show()

	app.exec_()
