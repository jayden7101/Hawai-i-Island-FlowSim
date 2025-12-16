import sys
from PyQt5.QtWidgets import QApplication
from lava_gui import LavaGui

def main():
    try:
        app = QApplication(sys.argv)
        
        # GUI is now in lava_gui.py --> dont need the mainwindowdebug file or the big main file anymore
        window = LavaGui() 
        window.show()
        
        sys.exit(app.exec_())
        
    except Exception as error:
        print(f"Application failed to start: {error}")

if __name__ == "__main__":
    main()