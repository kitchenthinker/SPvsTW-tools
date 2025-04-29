import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPen, QPainter
from PyQt5.QtCore import Qt, QRectF, QPointF
import gui_designer  # Это наш конвертированный файл дизайна
from PIL import ImageTk, Image as PILImage
import json

def getPointFromUVmapping(UVLeft: float, UVTop: float, UVRight: float, UVBottom: float, WidthImg: int, HeightImg: int):
    x = UVLeft * WidthImg
    y = UVTop * HeightImg
    width = (UVRight * WidthImg) - x
    height = (UVBottom * HeightImg) - y
    return (x, y, width, height)

def getUVmappingFromPoint(x, y, width, height: float, WidthImg, HeightImg: int):

    UVLeft = x / WidthImg
    UVTop = y / HeightImg
    UVRight = (x + width) / WidthImg
    UVBottom = (y + height) / HeightImg
    return (UVLeft, UVTop, UVRight, UVBottom)

class ExampleApp(QtWidgets.QMainWindow, gui_designer.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.font_file = None
        self.current_selection = None
        self.poss = 100

        # Binds
        self.btn_opn_img.clicked.connect(self.btn_open_image)
        self.btn_opn_fnt.clicked.connect(self.btn_open_font)
        self.btn_fnt_json.clicked.connect(self.btn_save_json)
        self.CharsList.clicked.connect(self.chars_showinfo)
        self.CharsList.clicked.connect(self.char_draw_rectangle)

        self.Chars_Add.clicked.connect(self.char_add)
        self.Chars_Edit.clicked.connect(self.char_edit)
        self.Chars_Del.clicked.connect(self.char_delete)
        self.Chars_exportjson.clicked.connect(self.char_export)
        self.Chars_importjson.clicked.connect(self.char_import)
        # self.Chars_Save.clicked.connect(self.char_save)

    def chars_add_edit(self):
        ascii = self.Edit_Char.text()

        if self.FontImage._p.width() == 0 or self.FontImage._p.height() == 0 or ascii == "" or self.font_file is None:
            return

        uv_points = getUVmappingFromPoint(float(self.Edit_X.text()), float(self.Edit_Y.text()), 
                                          float(self.Edit_W.text()), float(self.Edit_H.text()),
                                          self.FontImage._p.width(), self.FontImage._p.height())
        self.font_file['chars'][str(ord(ascii))] = {
                        "id": ord(ascii),
                        "ascii": ascii,
                        "page": 0,
                        "uv_left":uv_points[0],
                        "uv_top": uv_points[1],
                        "uv_right": uv_points[2],
                        "uv_bottom": uv_points[3],
                        "offset_x": int(self.Edit_Xoffset.text()),
                        "offset_y": int(self.Edit_Yoffset.text()),
                        "scale_x": int(self.Edit_ScaleX.text()),
                        "scale_y": int(self.Edit_ScaleY.text()),
                        "xAdvance": [
                            0,
                            int(self.Edit_XAdvance.text()),
                        ],
                        "kernels": [
                            0,
                            0,
                            0
                        ]
                        } 
        self.CharsList.clear()
        for k, v in self.font_file['chars'].items():
            self.CharsList.addItem(f'{k} [{v["ascii"]}]') 

    def char_add(self):
        self.chars_add_edit()  

    def char_edit(self):
        self.chars_add_edit()

    def char_delete(self):
        cur_item = self.CharsList.takeItem(self.CharsList.currentRow()).text()
        del self.font_file['chars'][cur_item.split(" ")[0]]


    def char_draw_rectangle(self):
        pass

    def chars_showinfo(self):
        if self.CharsList.count() > 0:
            cur_item = self.CharsList.currentItem().text()
            current_info = self.font_file['chars'][cur_item.split(" ")[0]]

            coordinats = getPointFromUVmapping(current_info['uv_left'], current_info['uv_top'], current_info['uv_right'], current_info['uv_bottom'],
                                       self.FontImage._p.width(), self.FontImage._p.height())
            
            self.Edit_Char.setText(current_info['ascii'])
            self.Edit_Xoffset.setText(str(current_info['offset_x']))
            self.Edit_Yoffset.setText(str(current_info['offset_y']))
            self.Edit_XAdvance.setText(str(current_info['xAdvance'][1]))
            self.Edit_ScaleX.setText(str(current_info['scale_x']))
            self.Edit_ScaleY.setText(str(current_info['scale_y']))
            self.Edit_X.setText(str(coordinats[0]))
            self.Edit_Y.setText(str(coordinats[1]))
            self.Edit_W.setText(str(coordinats[2]))
            self.Edit_H.setText(str(coordinats[3]))

            self.current_x, self.current_y, self.current_w, self.current_h = coordinats
            if self.current_w < 0:
                self.current_x -= abs(self.current_w)

            if self.current_selection is not None:
                self.FontImage._scene.removeItem(self.current_selection)
            self.poss += 10
            self.current_selection = QtWidgets.QGraphicsRectItem()
            # self.current_selection.setPen(Qt.yellow)
            self.FontImage._scene.addItem(self.current_selection)
            self.current_selection.setRect(QRectF(QPointF(self.current_x, self.current_y), QPointF(self.current_x + abs(self.current_w), self.current_y + self.current_h)))


    def btn_open_image(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption="Выберите файл изображения", filter='*.dds;;*.ddsz;;*.png')
        if filepath != "":
            if self.current_selection is not None:
                self.FontImage._scene.removeItem(self.current_selection)
            with PILImage.open(filepath) as imagePIL:
                imagePIL.load()
            imagePIL.save('tmp.png')
            self.FontImage.setFilename('tmp.png')

    def btn_open_font(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption="Выберите файл шрифта", filter='*.font;;')
        if filepath != "":
            with open(filepath, mode='r', encoding='utf16' ) as FF:
                self.font_file = json.load(FF)
            self.filepath = filepath.split('\\')[-1].split('.')[0]
            self.CharsList.clear()
            for k, v in self.font_file['chars'].items():
                self.CharsList.addItem(f'{k} [{v["ascii"]}]')

    def btn_save_json(self):
        if self.font_file is None or len(self.font_file) == 0: return
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, directory=self.filepath)
        if filepath != "":
            with open(filepath, mode='w', encoding='utf16' ) as FF:
                json.dump(self.font_file, FF, indent=2, ensure_ascii=False)

    def char_import(self):
        if self.font_file is None or len(self.font_file) == 0: return
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption="Выберите файл шрифта", filter='*.json;;')
        if filepath != "":
            with open(filepath, mode='r', encoding='utf16' ) as FF:
                temp_json = json.load(FF)

            for k, v in self.font_file['chars'].items():
                
                temp_item = temp_json['chars'][k]

                uv_points = getUVmappingFromPoint(float(temp_item['x']), 
                                                  float(temp_item['y']),
                                                  float(temp_item['w']), 
                                                  float(temp_item['h']),
                                                  self.FontImage._p.width(), 
                                                  self.FontImage._p.height())
                self.font_file['chars'][k].update(
                    {
                        "uv_left": uv_points[0],
                        "uv_top": uv_points[1],
                        "uv_right": uv_points[2],
                        "uv_bottom": uv_points[3],
                    }
                    )

    def char_export(self):
        if self.font_file is None or len(self.font_file) == 0: return
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, directory=f'{self.filepath}_expt.json')
        if filepath != "":
            
            for key, item in self.font_file['chars'].items():
                coordinats = getPointFromUVmapping(item['uv_left'], 
                                                   item['uv_top'], 
                                                   item['uv_right'], 
                                                   item['uv_bottom'], 
                                                   self.FontImage._p.width(), 
                                                   self.FontImage._p.height())
                
                current_x, current_y, current_w, current_h = coordinats
                if current_w < 0:
                    current_x -= abs(current_w)

                self.font_file['chars'][key].update(
                    {
                        'x': current_x,
                        'y': current_y,
                        'w': current_w,
                        'h': current_h,
                    }
                )

            with open(filepath, mode='w', encoding='utf16') as FF:
                json.dump(self.font_file, FF, indent=2, ensure_ascii=False)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()