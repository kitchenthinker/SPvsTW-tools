# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scott_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from singleImageGraphicsView import SingleImageGraphicsView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(903, 574)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.FRM_LEFT = QtWidgets.QFrame(self.centralwidget)
        self.FRM_LEFT.setGeometry(QtCore.QRect(10, 10, 421, 541))
        self.FRM_LEFT.setAutoFillBackground(True)
        self.FRM_LEFT.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.FRM_LEFT.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FRM_LEFT.setObjectName("FRM_LEFT")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.FRM_LEFT)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 340, 401, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_opn_img = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_opn_img.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_opn_img.setObjectName("btn_opn_img")
        self.verticalLayout.addWidget(self.btn_opn_img)
        self.btn_opn_fnt = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_opn_fnt.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_opn_fnt.setObjectName("btn_opn_fnt")
        self.verticalLayout.addWidget(self.btn_opn_fnt)
        self.btn_fnt_json = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_fnt_json.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_fnt_json.setObjectName("btn_fnt_json")
        self.verticalLayout.addWidget(self.btn_fnt_json)
        self.btn_fnt_raw = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_fnt_raw.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_fnt_raw.setObjectName("btn_fnt_raw")
        self.verticalLayout.addWidget(self.btn_fnt_raw)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.FRM_LEFT)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 269, 401, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Chars_Add = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Chars_Add.setMinimumSize(QtCore.QSize(10, 40))
        self.Chars_Add.setMaximumSize(QtCore.QSize(50, 16777215))
        self.Chars_Add.setObjectName("Chars_Add")
        self.horizontalLayout.addWidget(self.Chars_Add)
        self.Chars_Edit = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Chars_Edit.setMinimumSize(QtCore.QSize(10, 40))
        self.Chars_Edit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.Chars_Edit.setObjectName("Chars_Edit")
        self.horizontalLayout.addWidget(self.Chars_Edit)
        self.Chars_Del = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Chars_Del.setMinimumSize(QtCore.QSize(10, 40))
        self.Chars_Del.setMaximumSize(QtCore.QSize(50, 16777215))
        self.Chars_Del.setObjectName("Chars_Del")
        self.horizontalLayout.addWidget(self.Chars_Del)
        self.Chars_Save = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Chars_Save.setMinimumSize(QtCore.QSize(10, 40))
        self.Chars_Save.setMaximumSize(QtCore.QSize(50, 16777215))
        self.Chars_Save.setObjectName("Chars_Save")
        self.horizontalLayout.addWidget(self.Chars_Save)

        self.Chars_exportjson = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Chars_exportjson.setMinimumSize(QtCore.QSize(10, 40))
        self.Chars_exportjson.setMaximumSize(QtCore.QSize(50, 16777215))
        self.Chars_exportjson.setObjectName("Chars_ExportJson")
        self.horizontalLayout.addWidget(self.Chars_exportjson)

        self.Chars_importjson = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Chars_importjson.setMinimumSize(QtCore.QSize(10, 40))
        self.Chars_importjson.setMaximumSize(QtCore.QSize(50, 16777215))
        self.Chars_importjson.setObjectName("Chars_ImportJson")
        self.horizontalLayout.addWidget(self.Chars_importjson)

        self.CharsList = QtWidgets.QListWidget(self.FRM_LEFT)
        self.CharsList.setGeometry(QtCore.QRect(10, 11, 151, 251))
        self.CharsList.setFrameShape(QtWidgets.QFrame.Box)
        self.CharsList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.CharsList.setObjectName("CharsList")
        self.formLayoutWidget = QtWidgets.QWidget(self.FRM_LEFT)
        self.formLayoutWidget.setGeometry(QtCore.QRect(170, 10, 241, 256))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.Label_Xoffset = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_Xoffset.setObjectName("Label_Xoffset")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_Xoffset)
        self.Edit_Xoffset = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_Xoffset.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_Xoffset.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_Xoffset.setObjectName("Edit_Xoffset")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Edit_Xoffset)
        self.Label_Y_offset = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_Y_offset.setObjectName("Label_Y_offset")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_Y_offset)
        self.Edit_Yoffset = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_Yoffset.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_Yoffset.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_Yoffset.setObjectName("Edit_Yoffset")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Edit_Yoffset)
        self.Label_XAdvance = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_XAdvance.setObjectName("Label_XAdvance")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Label_XAdvance)
        self.Edit_XAdvance = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_XAdvance.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_XAdvance.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_XAdvance.setObjectName("Edit_XAdvance")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Edit_XAdvance)
        self.Label_ScaleX = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_ScaleX.setObjectName("Label_ScaleX")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Label_ScaleX)
        self.Edit_ScaleX = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_ScaleX.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_ScaleX.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_ScaleX.setObjectName("Edit_ScaleX")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.Edit_ScaleX)
        self.Label_ScaleY = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_ScaleY.setObjectName("Label_ScaleY")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.Label_ScaleY)
        self.Edit_ScaleY = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_ScaleY.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_ScaleY.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_ScaleY.setObjectName("Edit_ScaleY")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.Edit_ScaleY)
        self.Label_X = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_X.setObjectName("Label_X")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.Label_X)
        self.Edit_X = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_X.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_X.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_X.setObjectName("Edit_X")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.Edit_X)
        self.Label_Y = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_Y.setObjectName("Label_Y")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.Label_Y)
        self.Edit_Y = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_Y.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_Y.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_Y.setObjectName("Edit_Y")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.Edit_Y)
        self.Label_W = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_W.setObjectName("Label_W")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.Label_W)
        self.Edit_W = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_W.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_W.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_W.setObjectName("Edit_W")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.Edit_W)
        self.Label_H = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_H.setObjectName("Label_H")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.Label_H)
        self.Edit_H = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_H.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_H.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.Edit_H.setObjectName("Edit_H")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.Edit_H)
        self.Label_Char = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_Char.setObjectName("Label_Char")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_Char)
        self.Edit_Char = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.Edit_Char.setMaximumSize(QtCore.QSize(170, 16777215))
        self.Edit_Char.setObjectName("Edit_Char")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Edit_Char)
        self.FRM_RIGHT = QtWidgets.QFrame(self.centralwidget)
        self.FRM_RIGHT.setGeometry(QtCore.QRect(440, 10, 450, 540))
        self.FRM_RIGHT.setAutoFillBackground(False)
        self.FRM_RIGHT.setStyleSheet("background-color: rgb(216, 72, 216);")
        self.FRM_RIGHT.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.FRM_RIGHT.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FRM_RIGHT.setObjectName("FRM_RIGHT")
        self.FontImage = SingleImageGraphicsView(self.FRM_RIGHT)
        self.FontImage.setGeometry(QtCore.QRect(0, 0, 451, 541))
        self.FontImage.setObjectName("FontImage")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SCOTT FONT GUI"))
        self.btn_opn_img.setText(_translate("MainWindow", "Open Image"))
        self.btn_opn_fnt.setText(_translate("MainWindow", "Open Font"))
        self.btn_fnt_json.setText(_translate("MainWindow", "Save JSON"))
        self.btn_fnt_raw.setText(_translate("MainWindow", "Create FONT"))
        
        self.Chars_exportjson.setText(_translate("MainWindow", "Export"))
        self.Chars_importjson.setText(_translate("MainWindow", "Import"))
        self.Chars_Add.setText(_translate("MainWindow", "Add"))
        self.Chars_Edit.setText(_translate("MainWindow", "Edit"))
        self.Chars_Del.setText(_translate("MainWindow", "Del"))
        self.Chars_Save.setText(_translate("MainWindow", "Save"))
        self.Label_Xoffset.setText(_translate("MainWindow", "X-offset"))
        self.Label_Y_offset.setText(_translate("MainWindow", "Y-offset"))
        self.Label_XAdvance.setText(_translate("MainWindow", "XAdvance"))
        self.Label_ScaleX.setText(_translate("MainWindow", "Scale X"))
        self.Label_ScaleY.setText(_translate("MainWindow", "Scale Y"))
        self.Label_X.setText(_translate("MainWindow", "X"))
        self.Label_Y.setText(_translate("MainWindow", "Y"))
        self.Label_W.setText(_translate("MainWindow", "Width"))
        self.Label_H.setText(_translate("MainWindow", "Heigth"))
        self.Label_Char.setText(_translate("MainWindow", "Char"))

        self.Edit_Xoffset.setText(_translate("MainWindow", u"0"))
        self.Edit_Yoffset.setText(_translate("MainWindow", u"0"))
        self.Edit_XAdvance.setText(_translate("MainWindow", u"0"))
        self.Edit_ScaleX.setText(_translate("MainWindow", u"0"))
        self.Edit_ScaleY.setText(_translate("MainWindow", u"0"))
        self.Edit_X.setText(_translate("MainWindow", u"0"))
        self.Edit_Y.setText(_translate("MainWindow", u"0"))
        self.Edit_W.setText(_translate("MainWindow", u"0"))
        self.Edit_H.setText(_translate("MainWindow", u"0"))
