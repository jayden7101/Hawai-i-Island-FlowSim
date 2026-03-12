import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication
from lava_gui import LavaGui

# to help debugging - disables gpu hardware acceleration
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"

def main():
    try:
        app = QApplication(sys.argv)
        
        # GUI is now in lava_gui.py --> dont need the mainwindowdebug file or the big main file anymore
        window = LavaGui() 
        window.show()
        
        sys.exit(app.exec_())
        
    except Exception as error:
        print(f"Application failed to start: {error}")
        traceback.print_exc() 

# catch crashes that happen outside
def handle_exception(exc_type, exc_value, exc_traceback):
    print("unhandled exception:")
    traceback.print_exception(exc_type, exc_value, exc_traceback)

if __name__ == "__main__":
    sys.excepthook = handle_exception
    main()
