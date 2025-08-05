from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QPushButton, QWidget, QDoubleSpinBox, QSpinBox, QGroupBox
)
from PySide6.QtCore import Qt
import sys


class StrategyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Strategies Configuration")
        self.mainlayout = QVBoxLayout()
   

        #Take Profit
        self.takeProfit_checkBox = QCheckBox()
        self.takeProfit_input = QDoubleSpinBox()
        self.takeProfit_input.setRange(0.1, 1000.0)
        self.takeProfit_input.setSingleStep(0.1)
        self.takeProfit_input.setDecimals(2)
        self.takeProfit_input.setSuffix(" %")
        self.takeProfit_input.setEnabled(False)

        # self.takeProfit_checkBox.stateChanged.connect(lambda s: self.takeProfit_input.setEnabled(s == Qt.Checked))

        self.takeProfit_layout = QHBoxLayout()
        self.takeProfit_layout.addWidget(self.takeProfit_checkBox)
        self.takeProfit_layout.addWidget(QLabel("When"))
        self.takeProfit_layout.addWidget(self.takeProfit_input)
        self.takeProfit_layout.addWidget(QLabel("%  profit is achieved, sell all."))
        self.takeProfit_layout.addStretch()
        self.mainlayout.addLayout(self.takeProfit_layout)


        #Stop Loss
        self.stopLoss_checkBox = QCheckBox()
        self.stopLoss_spinBox = QDoubleSpinBox()
        self.stopLoss_spinBox.setRange(0.1, 1000.0)  # % loss range
        self.stopLoss_spinBox.setSingleStep(0.1)
        self.stopLoss_spinBox.setDecimals(2)
        self.stopLoss_spinBox.setSuffix(" %")
        self.stopLoss_spinBox.setEnabled(False)

        # self.stopLoss_checkBox.stateChanged.connect(lambda s: self.stopLoss_spinBox.setEnabled(s == Qt.Checked))

        self.stopLoss_layout = QHBoxLayout()
        self.stopLoss_layout.addWidget(self.stopLoss_checkBox)
        self.stopLoss_layout.addWidget(QLabel("When"))
        self.stopLoss_layout.addWidget(self.stopLoss_spinBox)
        self.stopLoss_layout.addWidget(QLabel("% loss is reached, sell all."))
        self.stopLoss_layout.addStretch()
        self.mainlayout.addLayout(self.stopLoss_layout)
        

        #Dollar Cost Averaging
        self.dollarCost_CheckBox = QCheckBox()
        self.dollarCost_amount_spinBox = QDoubleSpinBox()
        self.dollarCost_amount_spinBox.setRange(1, 1000000)
        self.dollarCost_amount_spinBox.setSingleStep(1)
        self.dollarCost_amount_spinBox.setDecimals(2)
        self.dollarCost_amount_spinBox.setPrefix("£ ")
        self.dollarCost_amount_spinBox.setEnabled(False)

        self.dollarCost_frequency_spinBox = QSpinBox()
        self.dollarCost_frequency_spinBox.setRange(1, 365)
        self.dollarCost_frequency_spinBox.setSingleStep(1)
        self.dollarCost_frequency_spinBox.setEnabled(False)

        # self.dollarCost_CheckBox.stateChanged.connect(
        #     lambda s: [w.setEnabled(s == Qt.Checked) for w in (self.dollarCost_amount_spinBox, self.dollarCost_frequency_spinBox)]
        # )

        self.dollarCost_layout = QHBoxLayout()
        self.dollarCost_layout.addWidget(self.dollarCost_CheckBox)
        self.dollarCost_layout.addWidget(QLabel("Invest"))
        self.dollarCost_layout.addWidget(self.dollarCost_amount_spinBox)
        self.dollarCost_layout.addWidget(QLabel("every"))
        self.dollarCost_layout.addWidget(self.dollarCost_frequency_spinBox)
        self.dollarCost_layout.addWidget(QLabel("days."))
        self.dollarCost_layout.addStretch()
        self.mainlayout.addLayout(self.dollarCost_layout)
        

        #Buttons
        self.btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Ok")
        self.cancel_btn = QPushButton("CANCEL")
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.ok_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.mainlayout.addLayout(self.btn_layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)


        self.setLayout(self.mainlayout)

    def toggle_all(self, state):
        checked = (state == Qt.CheckState.Checked)
        for cb in [self.takeProfit_checkBox, self.stopLoss_checkBox, self.dollarCost_CheckBox]:
            cb.setChecked(checked)

    def get_inputs(self):
        data = {}
        if self.takeProfit_checkBox.isChecked():
            data['take_profit'] = self.takeProfit_input.value()
        if self.stopLoss_checkBox.isChecked():
            data['stop_loss'] = self.stopLoss_spinBox.value()
        if self.dollarCost_CheckBox.isChecked():
            data['dca_amount'] = self.dollarCost_amount_spinBox.value()
            data['dca_frequency_days'] = self.dollarCost_frequency_spinBox.value()
        return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = StrategyDialog()
    if dlg.exec() == QDialog.DialogCode.Accepted:
        inputs = dlg.get_inputs()
        print("User inputs:", inputs)
    sys.exit(app.exec())
