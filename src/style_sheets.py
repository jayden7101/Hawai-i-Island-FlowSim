# Theme Colors --> theme can always change if needed or swap out
COLOR_CREAM = "#D7AB9A"
COLOR_PANES = "#F0E9E0"
COLOR_SALMON = "#ffcccb"

COLOR_PAUSE = "#ffeb3b" 
COLOR_RESET = "#e0e0e0" 
COLOR_STATUS_BG = "#FFDBBB"

COLOR_TEXT = "#594b59"

COLOR_RUN_PRESS = "#B9A7A0"
COLOR_ALMOND = "#DDC5C4"
COLOR_PORCELAIN = "#FFFBF5"
COLOR_LT_ORANGE = "#E9B38D"
COLOR_DK_GRAY = "#382B2B"



# left and right panes
STYLE_PANES = f"""
    background-color: {COLOR_PANES};
    """

# pause button
STYLE_PAUSE_BTN = f"""
    background-color: {COLOR_PAUSE};
    font-weight: bold;
    padding: 12px;
    """

# status bubble
STYLE_STATUS_BUBBLE = f"""
    background-color: {COLOR_LT_ORANGE};
    font-family: Verdana, serif;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #B56831;
    font-size: 14px;
    color: {COLOR_DK_GRAY};
    """

# info button
STYLE_INFO_BTN = f"""
    border-radius: 15px;
    border: 1px solid #B56831;
    background-color: {COLOR_LT_ORANGE};
    font-size: 14px;
    font-family: Verdana, serif;
    """

# run button
STYLE_RUN_BTN = f"""
    QPushButton {{
        background-color: {COLOR_ALMOND};
        font-family: Verdana, serif;
        font-weight: bold;
        font-size: 14px;
        padding: 12px;
        border-radius: 8px;
        border-top: 1px solid #ffb3b3;
        border-left: 1px solid #ffb3b3;
        border-bottom: 2px solid #b07070;
        border-right: 2px solid #b07070;
    }}
    QPushButton:pressed {{
        background-color: #bcaaa4;
        border-top: 2px solid #b07070;
        border-left: 2px solid #b07070;
        border-bottom: 1px solid #ffb3b3;
        border-right: 1px solid #ffb3b3;
        padding-top: 13px;
        padding-left: 13px;
    }}
    QPushButton:hover {{
        background-color: #bcaaa4;
        border-top: 2px solid #b07070;
        border-left: 2px solid #b07070;
        border-bottom: 1px solid #ffb3b3;
        border-right: 1px solid #ffb3b3;
        padding-top: 13px;
        padding-left: 13px;
    }}
"""

# reset button
STYLE_RESET_BTN = f"""
    QPushButton {{
        background-color: {COLOR_RESET};
        font-family: Verdana, serif;
        font-weight: bold;
        font-size: 14px;
        padding: 12px;
        border-radius: 8px;
        border-top: 1px solid #BBBBBB;
        border-left: 1px solid #BBBBBB;
        border-bottom: 2px solid #AAAAAA;
        border-right: 2px solid #AAAAAA;
    }}
    QPushButton:pressed {{
        background-color: {COLOR_RESET};
        border-top: 2px solid #AAAAAA;
        border-left: 2px solid #AAAAAA;
        border-bottom: 1px solid #BBBBBB;
        border-right: 1px solid #BBBBBB;
        padding-top: 13px;
        padding-left: 13px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_RESET};
        border-top: 2px solid #AAAAAA;
        border-left: 2px solid #AAAAAA;
        border-bottom: 1px solid #BBBBBB;
        border-right: 1px solid #BBBBBB;
        padding-top: 13px;
        padding-left: 13px;
    }}
"""

# configuration option labels
STYLE_CONFIG_LABELS = """
    font-family: Verdana, serif;
    font-weight: bold;
    font-size: 16px;
    color: #8B6662;
    word-spacing: 3px;
    """
# radio buttons
STYLE_RADIO_BTN = f"""
    QRadioButton {{
        font-family: Verdana, serif;
        color: {COLOR_DK_GRAY};
    }}
    QRadioButton::indicator {{
        width: 14px;
        height: 14px;
    }}
    QRadioButton::indicator:checked {{
        background-color: {COLOR_LT_ORANGE};
        border: 2px solid #A85920;
        border-radius: 7px;
    }}
    QRadioButton::indicator:unchecked {{
        background-color: {COLOR_ALMOND};
        border: 2px solid {COLOR_ALMOND};
        border-radius: 7px;
    }}
"""

# disclaimer + parameter button
STYLE_DISC_PARAM_BTN = f"""
    QPushButton {{
        background-color: {COLOR_ALMOND};
        font-size: 14px;
        font-weight: normal;
        color: {COLOR_TEXT};
        padding: 4px 8px;
        border: 1px solid #C2A9A9;
        border-radius: 4px;
        text-align: left;
        min-width: 110px;
    }}
    QPushButton:checked {{
        font-weight: bold;
        background-color: #C4B3B3;
        color: {COLOR_DK_GRAY};
        border: 1px solid #A79898;
    }}
    QPushButton:hover {{
        background-color: #C4B3B3;
        font-weight: bold;
        color: {COLOR_DK_GRAY};
        border: 1px solid #A79898;
    }}
"""
# this is the disclaimer and parameter box style setup
STYLE_DISC_PARAM_BOXES = f"""
    QTextEdit {{
        background-color: {COLOR_PORCELAIN};
        border: 1px solid #EC985A;
        border-radius: 5px;
        padding: 8px;
        font-size: 14px;
        color: {COLOR_TEXT};
    }}
    QScrollBar:vertical {{
        width: 12px;
        background: #f0f0f0;
        border-radius: 6px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_LT_ORANGE};
        border-radius: 6px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #bcaaa4;
    }}
  QScrollBar::sub-line:vertical {{
        background: #bcaaa4;
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }}
    QScrollBar::add-line:vertical {{
        background: #bcaaa4;
        height: 16px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }}
"""

STYLE_SPLITTER = """
    QSplitter::handle {
        background-color: #E9B38D;
    }
"""
