"""
style sheet for the ui. can change colors as desired. comments will indicate what each
color goes to.
"""
# Theme Colors --> theme can always change if needed or swap out
# parameter, disclaimer, overlays, run buttons & radio off bg
COLOR_ALMOND = "#ddc5c4" 
# borders around info, disclaimer btns, status bar, selected radio btn
COLOR_DRK_ORANGE = "#b56831"
# info/disclaimer buttons, status bar, selected radio button bg, splitter
COLOR_LT_ORANGE = "#e9b38d"
# left, right panes
COLOR_PANES = "#f0e9e0"
# disclaimer/parameter/overlay text boxes, configuration toggle background
COLOR_PORCELAIN = "#fffbf5" 
# text for status bubble, radio button, and overlay/param/disc,
# run/reset/pause (no hover/click)
COLOR_TEXT = "#594b59"
# text on status bubble, radio button, overlay/disclaimer/parameter, run/reset
# and pause text when hover/pushed
COLOR_DK_GRAY = "#382b2b" 
# light border for reset animation btn
COLOR_RESET_LT_GRAY = "#aaa"
# dark border for reset animation btn
COLOR_RESET_DRK_GRAY = "#bbb"
# reset button 
COLOR_RESET = "#e0e0e0" 
# light border color for run/pause animation btn
COLOR_LT_RUN_BORDER = "#ffb3b3"
# dark border color for run/pause animation btn
COLOR_DRK_RUN_BORDER = "#b07070"
# run/pause btn when press/hover, scrollbar hover in text boxes
# border of overlay/disclaimer/parameter text boxes
COLOR_DUSTY_BEIGE = "#bcaaa4"
# text for labels
COLOR_LABELS = "#8b6662"
# border for param/disclaimer/overlay buttons when clicked/hovering
COLOR_GRAY_BRWN = "#a79898"
# parameter/disclaimer/overlay button when hovering/clicked
COLOR_LT_GRAY_BRWN = "#c4b3b3"
# scroll bar backdrop color
COLOR_COOL_LT_GRAY = "#f0f0f0"
# clear overlay btn
COLOR_SALMON_RED = "#ea605d"
# clear overlay btn border
COLOR_CLR_OL_BORDER = "#b71c1c"
# clear overlay btn hover
COLOR_CLR_OL_HOVER = "#e74c49"
# clear overlay btn hover border
COLOR_DRK_RED = "#5b1615"

# left and right panes
STYLE_PANES = f"""
    background-color: {COLOR_PANES};
    """

# status bubble
STYLE_STATUS_BUBBLE = f"""
    background-color: {COLOR_LT_ORANGE};
    font-family: Verdana, serif;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid {COLOR_DRK_ORANGE};
    font-size: 14px;
    color: {COLOR_DK_GRAY};
    """

# info button
STYLE_INFO_BTN = f"""
    border-radius: 15px;
    border: 1px solid {COLOR_DRK_ORANGE};
    background-color: {COLOR_LT_ORANGE};
    font-size: 14px;
    font-family: Verdana, serif;
    """

# sources button
STYLE_SOURCE_BTN = f"""
    border-radius: 15px;
    border: 1px solid {COLOR_DRK_ORANGE};
    background-color: {COLOR_LT_ORANGE};
    font-size: 14px;
    font-family: Verdana, serif;
"""

# spaces for radio buttons/flow config options
STYLE_RADIO_BOXES = f"""
    QWidget {{
        background-color: {COLOR_PORCELAIN};
        border-radius: 6px;
            }}
"""

# run & pause button
STYLE_RUN_PAUSE_BTN = f"""
    QPushButton {{
        background-color: {COLOR_ALMOND};
        font-family: Verdana, serif;
        font-weight: bold;
        font-size: 14px;
        color: {COLOR_TEXT};
        padding: 12px;
        border-radius: 8px;
        border-top: 1px solid {COLOR_LT_RUN_BORDER};
        border-left: 1px solid {COLOR_LT_RUN_BORDER};
        border-bottom: 2px solid {COLOR_DRK_RUN_BORDER};
        border-right: 2px solid {COLOR_DRK_RUN_BORDER};
    }}
    QPushButton:pressed {{
        color: {COLOR_DK_GRAY};
        background-color: {COLOR_DUSTY_BEIGE};
        border-top: 2px solid {COLOR_DRK_RUN_BORDER};
        border-left: 2px solid {COLOR_DRK_RUN_BORDER};
        border-bottom: 1px solid {COLOR_LT_RUN_BORDER};
        border-right: 1px solid {COLOR_LT_RUN_BORDER};
        padding-top: 13px;
        padding-left: 13px;
    }}
    QPushButton:hover {{
        color: {COLOR_DK_GRAY};
        background-color: {COLOR_DUSTY_BEIGE};
        border-top: 2px solid {COLOR_DRK_RUN_BORDER};
        border-left: 2px solid {COLOR_DRK_RUN_BORDER};
        border-bottom: 1px solid {COLOR_LT_RUN_BORDER};
        border-right: 1px solid {COLOR_LT_RUN_BORDER};
        padding-top: 13px;
        padding-left: 13px;
    }}
"""

# reset button
STYLE_RESET_BTN = f"""
    QPushButton {{
        color: {COLOR_TEXT};
        background-color: {COLOR_RESET};
        font-family: Verdana, serif;
        font-weight: bold;
        font-size: 14px;
        padding: 12px;
        border-radius: 8px;
        border-top: 1px solid {COLOR_RESET_DRK_GRAY};
        border-left: 1px solid {COLOR_RESET_DRK_GRAY};
        border-bottom: 2px solid {COLOR_RESET_LT_GRAY};
        border-right: 2px solid {COLOR_RESET_LT_GRAY};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_RESET};
        color: {COLOR_DK_GRAY};
        border-top: 2px solid {COLOR_RESET_LT_GRAY};
        border-left: 2px solid {COLOR_RESET_LT_GRAY};
        border-bottom: 1px solid {COLOR_RESET_DRK_GRAY};
        border-right: 1px solid {COLOR_RESET_DRK_GRAY};
        padding-top: 13px;
        padding-left: 13px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_RESET};
        color: {COLOR_DK_GRAY};
        border-top: 2px solid {COLOR_RESET_LT_GRAY};
        border-left: 2px solid {COLOR_RESET_LT_GRAY};
        border-bottom: 1px solid {COLOR_RESET_DRK_GRAY};
        border-right: 1px solid {COLOR_RESET_DRK_GRAY};
        padding-top: 13px;
        padding-left: 13px;
    }}
"""

# configuration options, map overlay header
STYLE_CONFIG_LABELS = f"""   
    font-family: Verdana, serif;
    font-weight: bold;
    font-size: 16px;
    color: {COLOR_LABELS};
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
        border: 2px solid {COLOR_DRK_ORANGE};
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
        border: 1px solid {COLOR_DUSTY_BEIGE};
        border-radius: 4px;
        text-align: left;
        min-width: 110px;
    }}
    QPushButton:checked {{
        font-weight: bold;
        background-color: {COLOR_LT_GRAY_BRWN};
        color: {COLOR_DK_GRAY};
        border: 1px solid {COLOR_GRAY_BRWN};
    }}
    QPushButton:hover {{
        background-color: {COLOR_LT_GRAY_BRWN};
        font-weight: bold;
        color: {COLOR_DK_GRAY};
        border: 1px solid {COLOR_GRAY_BRWN};
    }}
"""

# this is the disclaimer and parameter text box style setup
STYLE_DISC_PARAM_BOXES = f"""
    QTextEdit {{
        background-color: {COLOR_PORCELAIN};
        border: 1px solid {COLOR_DUSTY_BEIGE};
        border-radius: 5px;
        padding: 8px;
        font-size: 14px;
        color: {COLOR_TEXT};
    }}
    QScrollBar:vertical {{
        width: 12px;
        background: {COLOR_COOL_LT_GRAY};
        border-radius: 6px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_LT_ORANGE};
        border-radius: 6px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLOR_DUSTY_BEIGE};
    }}
  QScrollBar::sub-line:vertical {{
        background: {COLOR_DUSTY_BEIGE};
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }}
    QScrollBar::add-line:vertical {{
        background: {COLOR_DUSTY_BEIGE};
        height: 16px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }}
"""
# splitter
STYLE_SPLITTER = f"""
    QSplitter::handle {{
        background-color: {COLOR_LT_ORANGE};
    }}
"""

# clear button
STYLE_CLEAR_BTN = f"""
    QPushButton{{
        background-color: {COLOR_SALMON_RED};
        color: #fff;
        font-family: Verdana, serif;
        font-size: 13px;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 5px;
        border: 1px solid {COLOR_CLR_OL_BORDER};
        text-align: left;
    }}
    QPushButton:hover {{
        background-color: {COLOR_CLR_OL_HOVER};
        border: 1px solid {COLOR_DRK_RED};
    }}
"""

# lil dots next to overlay selections
OVERLAY_ON  = "🟢" # green
OVERLAY_OFF = "🔴" # red

# dropdown button
STYLE_OL_DROPDOWN_BTN = f"""
    QPushButton {{
        background-color: {COLOR_ALMOND};
        font-size: 14px;
        font-weight: normal;
        color: {COLOR_TEXT};
        padding: 4px 8px;
        border: 1px solid {COLOR_DUSTY_BEIGE};
        border-radius: 4px;
        text-align: left;
        min-width: 110px;
    }}
    QPushButton:checked {{
        font-weight: bold;
        background-color: {COLOR_LT_GRAY_BRWN};
        color: {COLOR_DK_GRAY};
        border: 1px solid {COLOR_GRAY_BRWN};
    }}
    QPushButton:hover {{
        background-color: {COLOR_LT_GRAY_BRWN};
        font-weight: bold;
        color: {COLOR_DK_GRAY};
        border: 1px solid {COLOR_GRAY_BRWN};
    }}
"""

# dropdown list
STYLE_OVERLAY_LIST = f"""
    QListWidget {{
        background-color: {COLOR_PORCELAIN};
        border: 1px solid {COLOR_DUSTY_BEIGE};
        border-radius: 4px;
        font-family: Verdana, serif;
        font-size: 13px;
        color: {COLOR_DK_GRAY};
        padding: 2px;
        outline: 0;
    }}
    QListWidget::item {{
        padding: 5px 8px;
        border-radius: 3px;
    }}
    QListWidget::item:hover {{
        background-color: {COLOR_ALMOND};
    }}
    QScrollBar:vertical{{
        width: 10px;
        background: {COLOR_COOL_LT_GRAY};
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_LT_ORANGE};
        border-radius: 5px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLOR_DUSTY_BEIGE};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""
