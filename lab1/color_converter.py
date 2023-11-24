# баг QT из-за чего прыгают ползунки на маке. Шрфт не моноширенный, из-за этого дрожание во время движения ползунков.
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from generated_ui import Ui_MainWindow
from PyQt5.QtGui import QColor, QPalette, QFontDatabase, QFont

fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
fixedFont.setStyleHint(QFont.Monospace)
class ColorConverterApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.color = QColor(255, 0, 0)

        self.connect_ui_elements()
        self.update_all()

    def connect_ui_elements(self):
        # Connect all the UI elements to their respective update methods
        self.redSlider.valueChanged.connect(self.update_rgb)
        self.greenSlider.valueChanged.connect(self.update_rgb)
        self.blueSlider.valueChanged.connect(self.update_rgb)

        self.CSlider.valueChanged.connect(self.update_cmyk)
        self.MSlider.valueChanged.connect(self.update_cmyk)
        self.YSlider.valueChanged.connect(self.update_cmyk)
        self.KSlider.valueChanged.connect(self.update_cmyk)

        self.HSlider.valueChanged.connect(self.update_hls)
        self.LSlider.valueChanged.connect(self.update_hls)
        self.SSlider.valueChanged.connect(self.update_hls)

        self.RdoubleSpinBox.valueChanged.connect(self.update_rgb_double)
        self.GdoubleSpinBox.valueChanged.connect(self.update_rgb_double)
        self.BdoubleSpinBox.valueChanged.connect(self.update_rgb_double)
        self.RdoubleSpinBox.setFont(fixedFont)
        self.GdoubleSpinBox.setFont(fixedFont)
        self.BdoubleSpinBox.setFont(fixedFont)

        self.CdoubleSpinBox.valueChanged.connect(self.update_cmyk_double)
        self.MdoubleSpinBox.valueChanged.connect(self.update_cmyk_double)
        self.YdoubleSpinBox.valueChanged.connect(self.update_cmyk_double)
        self.KdoubleSpinBox.valueChanged.connect(self.update_cmyk_double)
        self.CdoubleSpinBox.setFont(fixedFont)
        self.MdoubleSpinBox.setFont(fixedFont)
        self.YdoubleSpinBox.setFont(fixedFont)
        self.KdoubleSpinBox.setFont(fixedFont)

        self.HdoubleSpinBox.valueChanged.connect(self.update_hls_double)
        self.LdoubleSpinBox.valueChanged.connect(self.update_hls_double)
        self.SdoubleSpinBox.valueChanged.connect(self.update_hls_double)
        self.HdoubleSpinBox.setFont(fixedFont)
        self.LdoubleSpinBox.setFont(fixedFont)
        self.SdoubleSpinBox.setFont(fixedFont)

        self.colorButton.clicked.connect(self.open_color_dialog)

    def update_rgb(self):
        self.update_color(QColor.fromRgbF(
            self.redSlider.value() / 255,
            self.greenSlider.value() / 255,
            self.blueSlider.value() / 255
        ))

    def update_cmyk(self):
        self.update_color(QColor.fromCmykF(
            self.CSlider.value() / 100,
            self.MSlider.value() / 100,
            self.YSlider.value() / 100,
            self.KSlider.value() / 100
        ))

    def update_hls(self):
        self.update_color(QColor.fromHslF(
            self.HSlider.value() / 360,
            self.SSlider.value() / 100,
            self.LSlider.value() / 100
        ))

    def update_rgb_double(self):
        self.update_color(QColor.fromRgbF(
            self.RdoubleSpinBox.value() / 255,
            self.GdoubleSpinBox.value() / 255,
            self.BdoubleSpinBox.value() / 255
        ))

    def update_cmyk_double(self):
        self.update_color(QColor.fromCmykF(
            self.CdoubleSpinBox.value() / 100,
            self.MdoubleSpinBox.value() / 100,
            self.YdoubleSpinBox.value() / 100,
            self.KdoubleSpinBox.value() / 100
        ))

    def update_hls_double(self):
        self.update_color(QColor.fromHslF(
            self.HdoubleSpinBox.value() / 360,
            self.SdoubleSpinBox.value() / 100,
            self.LdoubleSpinBox.value() / 100
        ))

    def update_color(self, new_color):
        self.color = new_color
        self.update_all()

    def update_all(self):
        components = [
            (self.redSlider, self.RdoubleSpinBox, 255, self.color.redF()),
            (self.greenSlider, self.GdoubleSpinBox, 255, self.color.greenF()),
            (self.blueSlider, self.BdoubleSpinBox, 255, self.color.blueF()),
            (self.CSlider, self.CdoubleSpinBox, 100, self.color.getCmykF()[0]),
            (self.MSlider, self.MdoubleSpinBox, 100, self.color.getCmykF()[1]),
            (self.YSlider, self.YdoubleSpinBox, 100, self.color.getCmykF()[2]),
            (self.KSlider, self.KdoubleSpinBox, 100, self.color.getCmykF()[3]),
            (self.HSlider, self.HdoubleSpinBox, 360, self.color.getHslF()[0]),
            (self.LSlider, self.LdoubleSpinBox, 100, self.color.getHslF()[2]),
            (self.SSlider, self.SdoubleSpinBox, 100, self.color.getHslF()[1]),
        ]

        for slider, double_spinbox, factor, norm_value in components:
            value = norm_value * factor
            self.update_slider(slider, value)
            self.update_double_spinbox(double_spinbox, value)

        self.update_labels()
        self.update_palette()

    def update_slider(self, slider, value):
        slider.blockSignals(True)
        slider.setValue(int(value))
        slider.blockSignals(False)

    def update_double_spinbox(self, double_spinbox, value):
        double_spinbox.blockSignals(True)
        double_spinbox.setValue(value)
        double_spinbox.blockSignals(False)

    def update_labels(self):
        r, g, b, _ = self.color.getRgbF()
        c, m, y, k, _ = self.color.getCmykF()
        h, s, l, _ = self.color.getHslF()
        self.cmykLabel.setText(f"CMYK: {round(c * 100, 2)}%, {round(m * 100, 2)}%, {round(y * 100, 2)}%, {round(k * 100, 2)}%")
        self.hlsLabel.setText(f"HSL: {round(h * 360, 2)}°, {round(s * 100, 2)}%, {round(l * 100, 2)}%")
        self.rgbLabel.setText(f"RGB: {round(r * 255, 2)}, {round(g * 255, 2)}, {round(b * 255, 2)}")

    def update_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, self.color)
        self.gridLayoutWidget.setPalette(palette)

    def open_color_dialog(self):
        color = QColorDialog.getColor(self.color, self, "Choose a color")
        if color.isValid():
            self.update_color(color)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorConverterApp()
    window.show()
    sys.exit(app.exec_())