import sys
from PyQt6.QtWidgets import QApplication

from interface import App

def main():
	app = QApplication(sys.argv)
	window = App()
	window.show()
	sys.exit(app.exec())
	
if __name__ == "__main__":
	main()