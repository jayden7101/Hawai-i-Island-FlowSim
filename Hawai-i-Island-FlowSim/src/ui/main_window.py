import sys
from PyQt5.QtWidgets import QApplication
from lava_ui import LavaFlowUI

def main():
    app = QApplication(sys.argv)  
    window = LavaFlowUI()
    window.show()    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()