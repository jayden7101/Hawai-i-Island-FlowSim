"""
Dark volcanic theme stylesheet.
Designed to feel cool, modern, and volcanic.
"""

# =========================
# Core Palette
# =========================

# Main app / pane background
COLOR_CHARCOAL_SLATE = "#11181C"

# Slightly lifted panel / control surface
COLOR_BASALT_STEEL = "#404854"

# Inner cards, text boxes, overlay list, radio group surfaces
COLOR_COOLED_LAVA = "#4A525E"

# Primary readable text
COLOR_ASH_WHITE = "#F1F3EE"

# Secondary text, soft highlights, hover outlines
COLOR_SMOKE_MIST = "#CAD2C5"

# Standard borders / muted separators
COLOR_VOLCANIC_STONE = "#5C5C5C"

# Primary accent
COLOR_LAVA_RED = "#C82D32"

# Pressed / deeper accent state
COLOR_MAGMA_RED = "#A61E22"

# Stronger dark edge for pressed / active controls
COLOR_OBSIDIAN = "#1F252B"

# Slightly brighter dark surface for hover states
COLOR_GRAPHITE_RISE = "#56606D"

# Neutral reset button tones
COLOR_STEEL_FOG = "#7A848F"
COLOR_STEEL_MIST = "#8F98A3"

# Scrollbar track
COLOR_DEEP_VENT = "#2F363D"

# Overlay state indicators
OVERLAY_ON = "🟢"
OVERLAY_OFF = "🔴"


# =========================
# Container / Pane Styles
# =========================

STYLE_PANES = f"""
    background-color: {COLOR_CHARCOAL_SLATE};
"""

STYLE_SPLITTER = f"""
    QSplitter::handle {{
        background-color: {COLOR_VOLCANIC_STONE};
    }}
"""


# =========================
# Status / Information
# =========================

STYLE_STATUS_BUBBLE = f"""
    background-color: {COLOR_BASALT_STEEL};
    font-family: Verdana, serif;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid {COLOR_LAVA_RED};
    font-size: 14px;
    color: {COLOR_ASH_WHITE};
"""

STYLE_INFO_BTN = f"""
    border-radius: 15px;
    border: 1px solid {COLOR_LAVA_RED};
    background-color: {COLOR_BASALT_STEEL};
    color: {COLOR_ASH_WHITE};
    font-size: 14px;
    font-family: Verdana, serif;
"""

STYLE_SOURCE_BTN = f"""
    border-radius: 15px;
    border: 1px solid {COLOR_LAVA_RED};
    background-color: {COLOR_BASALT_STEEL};
    color: {COLOR_ASH_WHITE};
    font-size: 14px;
    font-family: Verdana, serif;
"""


# =========================
# Labels / Section Headers
# =========================

STYLE_CONFIG_LABELS = f"""
    font-family: Verdana, serif;
    font-weight: bold;
    font-size: 16px;
    color: {COLOR_SMOKE_MIST};
    word-spacing: 3px;
"""


# =========================
# Radio Groups / Options
# =========================

STYLE_RADIO_BOXES = f"""
    QWidget {{
        background-color: {COLOR_COOLED_LAVA};
        border: none
        border-radius: 6px;
    }}
"""

STYLE_RADIO_BTN = f"""
    QRadioButton {{
        font-family: Verdana, serif;
        color: {COLOR_ASH_WHITE};
        background: transparent;
    }}
    QRadioButton::indicator {{
        width: 14px;
        height: 14px;
    }}
    QRadioButton::indicator:checked {{
        background-color: {COLOR_LAVA_RED};
        border: 2px solid {COLOR_SMOKE_MIST};
        border-radius: 7px;
    }}
    QRadioButton::indicator:unchecked {{
        background-color: {COLOR_BASALT_STEEL};
        border: 2px solid {COLOR_VOLCANIC_STONE};
        border-radius: 7px;
    }}
"""


# =========================
# Main Action Buttons
# =========================

STYLE_RUN_PAUSE_BTN = f"""
    QPushButton {{
        background-color: {COLOR_LAVA_RED};
        font-family: Verdana, serif;
        font-weight: bold;
        font-size: 14px;
        color: {COLOR_ASH_WHITE};
        padding: 12px;
        border-radius: 8px;
        border-top: 1px solid {COLOR_SMOKE_MIST};
        border-left: 1px solid {COLOR_SMOKE_MIST};
        border-bottom: 2px solid {COLOR_MAGMA_RED};
        border-right: 2px solid {COLOR_MAGMA_RED};
    }}
    QPushButton:pressed {{
        color: {COLOR_ASH_WHITE};
        background-color: {COLOR_MAGMA_RED};
        border-top: 2px solid {COLOR_OBSIDIAN};
        border-left: 2px solid {COLOR_OBSIDIAN};
        border-bottom: 1px solid {COLOR_SMOKE_MIST};
        border-right: 1px solid {COLOR_SMOKE_MIST};
        padding-top: 13px;
        padding-left: 13px;
    }}
    QPushButton:hover {{
        color: {COLOR_ASH_WHITE};
        background-color: {COLOR_MAGMA_RED};
        border-top: 2px solid {COLOR_OBSIDIAN};
        border-left: 2px solid {COLOR_OBSIDIAN};
        border-bottom: 1px solid {COLOR_SMOKE_MIST};
        border-right: 1px solid {COLOR_SMOKE_MIST};
        padding-top: 13px;
        padding-left: 13px;
    }}
"""

STYLE_RESET_BTN = f"""
    QPushButton {{
        color: {COLOR_ASH_WHITE};
        background-color: {COLOR_BASALT_STEEL};
        font-family: Verdana, serif;
        font-weight: bold;
        font-size: 14px;
        padding: 12px;
        border-radius: 8px;
        border-top: 1px solid {COLOR_STEEL_MIST};
        border-left: 1px solid {COLOR_STEEL_MIST};
        border-bottom: 2px solid {COLOR_STEEL_FOG};
        border-right: 2px solid {COLOR_STEEL_FOG};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_GRAPHITE_RISE};
        color: {COLOR_ASH_WHITE};
        border-top: 2px solid {COLOR_STEEL_FOG};
        border-left: 2px solid {COLOR_STEEL_FOG};
        border-bottom: 1px solid {COLOR_STEEL_MIST};
        border-right: 1px solid {COLOR_STEEL_MIST};
        padding-top: 13px;
        padding-left: 13px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_GRAPHITE_RISE};
        color: {COLOR_ASH_WHITE};
        border-top: 2px solid {COLOR_STEEL_FOG};
        border-left: 2px solid {COLOR_STEEL_FOG};
        border-bottom: 1px solid {COLOR_STEEL_MIST};
        border-right: 1px solid {COLOR_STEEL_MIST};
        padding-top: 13px;
        padding-left: 13px;
    }}
"""


# =========================
# Toggle / Secondary Buttons
# =========================

STYLE_DISC_PARAM_BTN = f"""
    QPushButton {{
        background-color: {COLOR_BASALT_STEEL};
        font-size: 14px;
        font-weight: normal;
        color: {COLOR_ASH_WHITE};
        padding: 4px 8px;
        border: 1px solid {COLOR_VOLCANIC_STONE};
        border-radius: 4px;
        text-align: left;
        min-width: 110px;
    }}
    QPushButton:checked {{
        font-weight: bold;
        background-color: {COLOR_GRAPHITE_RISE};
        color: {COLOR_ASH_WHITE};
        border: 1px solid {COLOR_SMOKE_MIST};
    }}
    QPushButton:hover {{
        background-color: {COLOR_GRAPHITE_RISE};
        font-weight: bold;
        color: {COLOR_ASH_WHITE};
        border: 1px solid {COLOR_SMOKE_MIST};
    }}
"""

STYLE_OL_DROPDOWN_BTN = f"""
    QPushButton {{
        background-color: {COLOR_BASALT_STEEL};
        font-size: 14px;
        font-weight: normal;
        color: {COLOR_ASH_WHITE};
        padding: 4px 8px;
        border: 1px solid {COLOR_VOLCANIC_STONE};
        border-radius: 4px;
        text-align: left;
        min-width: 110px;
    }}
    QPushButton:checked {{
        font-weight: bold;
        background-color: {COLOR_GRAPHITE_RISE};
        color: {COLOR_ASH_WHITE};
        border: 1px solid {COLOR_SMOKE_MIST};
    }}
    QPushButton:hover {{
        background-color: {COLOR_GRAPHITE_RISE};
        font-weight: bold;
        color: {COLOR_ASH_WHITE};
        border: 1px solid {COLOR_SMOKE_MIST};
    }}
"""

STYLE_CLEAR_BTN = f"""
    QPushButton {{
        background-color: {COLOR_LAVA_RED};
        color: {COLOR_ASH_WHITE};
        font-family: Verdana, serif;
        font-size: 13px;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 5px;
        border: 1px solid {COLOR_MAGMA_RED};
        text-align: left;
    }}
    QPushButton:hover {{
        background-color: {COLOR_MAGMA_RED};
        border: 1px solid {COLOR_SMOKE_MIST};
    }}
"""


# =========================
# Text Boxes
# =========================

STYLE_DISC_PARAM_BOXES = f"""
    QTextEdit {{
        background-color: {COLOR_COOLED_LAVA};
        border: 1px solid {COLOR_VOLCANIC_STONE};
        border-radius: 5px;
        padding: 8px;
        font-size: 14px;
        color: {COLOR_ASH_WHITE};
    }}
    QScrollBar:vertical {{
        width: 12px;
        background: {COLOR_DEEP_VENT};
        border-radius: 6px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_LAVA_RED};
        border-radius: 6px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLOR_MAGMA_RED};
    }}
    QScrollBar::sub-line:vertical {{
        background: {COLOR_VOLCANIC_STONE};
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }}
    QScrollBar::add-line:vertical {{
        background: {COLOR_VOLCANIC_STONE};
        height: 16px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }}
"""


# =========================
# Overlay List
# =========================

STYLE_OVERLAY_LIST = f"""
    QListWidget {{
        background-color: {COLOR_COOLED_LAVA};
        border: 1px solid {COLOR_VOLCANIC_STONE};
        border-radius: 4px;
        font-family: Verdana, serif;
        font-size: 13px;
        color: {COLOR_ASH_WHITE};
        padding: 2px;
        outline: 0;
    }}
    QListWidget::item {{
        padding: 5px 8px;
        border-radius: 3px;
    }}
    QListWidget::item:hover {{
        background-color: {COLOR_GRAPHITE_RISE};
    }}
    QScrollBar:vertical {{
        width: 10px;
        background: {COLOR_DEEP_VENT};
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_LAVA_RED};
        border-radius: 5px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLOR_MAGMA_RED};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""
#=================
# Theme Button
#=================
STYLE_THEME_CIRCLE_BTN = f"""
    QPushButton {{
        background-color: {COLOR_BASALT_STEEL};
        color: {COLOR_ASH_WHITE};
        border: 1px solid {COLOR_VOLCANIC_STONE};
        border-radius: 15px;
        font-family: Verdana, serif;
        font-size: 16px;
        font-weight: bold;
        padding: 0px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_GRAPHITE_RISE};
        border: 1px solid {COLOR_SMOKE_MIST};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_GRAPHITE_RISE};
        border: 1px solid {COLOR_LAVA_RED};
    }}
"""

#========================
# Scrubber Buttons
#========================
STYLE_SCRUBBER_SLIDER = f"""
    QSlider::groove:horizontal {{
        height: 6px;
        background: {COLOR_DEEP_VENT};
        border-radius: 3px;
    }}
    QSlider::sub-page:horizontal {{
        background: {COLOR_LAVA_RED};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {COLOR_BASALT_STEEL};
        border: 1px solid {COLOR_SMOKE_MIST};
        width: 14px;
        height: 14px;
        margin: -4px 0;
        border-radius: 7px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {COLOR_GRAPHITE_RISE};
        border: 1px solid {COLOR_LAVA_RED};
    }}
"""

STYLE_SCRUBBER_LABEL = f"""
    font-family: Verdana, serif;
    font-size: 11px;
    color: {COLOR_ASH_WHITE};
    background: transparent;
"""

STYLE_SCRUBBER_BTN = f"""
    QPushButton {{
        background-color: {COLOR_BASALT_STEEL};
        color: {COLOR_ASH_WHITE};
        font-size: 14px;
        border: 1px solid {COLOR_VOLCANIC_STONE};
        border-radius: 4px;
        padding: 2px 6px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_GRAPHITE_RISE};
        border: 1px solid {COLOR_LAVA_RED};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_OBSIDIAN};
        border: 1px solid {COLOR_MAGMA_RED};
    }}
    QPushButton:disabled {{
        color: {COLOR_STEEL_MIST};
        background-color: {COLOR_DEEP_VENT};
        border: 1px solid {COLOR_VOLCANIC_STONE};
    }}
"""