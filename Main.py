import os
import sys

from PyQt5 import QtGui, QtWidgets

from function.function_rawpy import *
from window.Ui_Main import Ui_MainWindow
from window.Ui_About import Ui_Dialog_About
import qdarkstyle


os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"


# 加载并保存文件目录
class Filelist():
    def __init__(self):
        self.filelist_2 = []
        self.des = ""

    def fileAddToList(self):
        filelist = QtWidgets.QFileDialog.getOpenFileNames(
            None, None, directory="c://", filter="All Files (*)")

        # 判断是否导入文件，防止崩溃
        if not filelist == ([], ''):

            # 默认出来的列表格式不太对，拆开来重组一下
            filelist_1 = str(filelist[0]).replace("[", '').replace("]", '').replace(
                "\"", '').replace("'", '').replace(" ", '')
            self.filelist_2 = filelist_1.split(",")
            print(f'filelist: {self.filelist_2}')

            # TableWidgets 操作
            self.filelist_len = len(self.filelist_2)
            window.TableWidgets_update(self.filelist_len, self.filelist_2)

            msg = f'Input {self.filelist_len} Images.'
            window.TextBrower_info_update(msg)
            window.TextBrower_info_update(
                '-----------------------------------')

    def setDestination(self):
        self.des = QtWidgets.QFileDialog.getExistingDirectory(
            None, "选择文件保存目录", directory="c://")

        if not self.des == "":
            print(f'destination:{self.des}')
            window.TextBrowser_Destination_Update(self.des)

            msg = f'Set Destination: \n{self.des}'
            window.TextBrower_info_update(msg)
            window.TextBrower_info_update(
                '-----------------------------------')


newfilelist = Filelist()
RTF = RawToTiff()

# 转换图像，连接RawToTiff类


class StartConvert():
    def __init__(self):
        try:
            # 判断是否选择输入/输出
            if newfilelist.filelist_2 == [] or newfilelist.des == "":
                print("未选择目的地或者输入")
                QtWidgets.QMessageBox.warning(
                    None, "Warning", "You haven't chosen input or destination.")

            else:
                self._newfilelist = newfilelist.filelist_2
                _newdestination = newfilelist.des
                self.count = 0
                self.len = len(self._newfilelist)

                infolist = window.info_return()
                window.statusBar().showMessage('Running')
                window.TextBrower_info_update(f'Total: {self.len} Images.')
                for i in infolist:
                    window.TextBrower_info_update(i)
                window.TextBrower_info_update(
                    '-----------------------------------')

                for file in self._newfilelist:
                    RTF.run(file, _newdestination)
                    window.TableWidgets_Done(self.count)
                    self.percent = int(100*(self.count+1)/self.len)
                    window.pgb_update(self.percent)
                    self.count += 1

                window.TextBrower_info_update(f'{self.len} images Done.')
                window.TextBrower_info_update(
                    '-----------------------------------')
                window.statusBar().showMessage('Ready')
                QtWidgets.QMessageBox.information(None, "Tips", "All done.")


# 报错窗口
        except:
            print("转换出错")
            QtWidgets.QMessageBox.warning(
                None, "Warning", "There was a error while converting.")

# 图片预览模块


class imagePreviewDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        if not newfilelist.filelist_2 == []:
            preview_dialog = QtWidgets.QDialog()
            preview_dialog.setWindowIcon(QtGui.QIcon(
                f'{os.path.abspath("")}/Pic/logo-2.png'))
            preview_dialog.resize(900, 600)
            pic = QtWidgets.QLabel(preview_dialog)                                                                                                                                                                                                                                                                                                                                                                                                 
            pic.resize(900, 600)
            pic.setPixmap(QtGui.QPixmap(
                RTF.preview_image_run(newfilelist.filelist_2[self.row_get()])))
            pic.setScaledContents(True)
            preview_dialog.setWindowTitle("Preview")
            preview_dialog.show()
            preview_dialog.exec()
        else:
            QtWidgets.QMessageBox.warning(
                None, "Warning", "You haven't chosen input or destination.")

    def row_get(self):
        self.row = window.tableWidget.currentRow()
        print(self.row)
        return self.row


Preview = imagePreviewDialog


class DialogAboutWindow(QtWidgets.QDialog, Ui_Dialog_About):
    def __init__(self):
        super(DialogAboutWindow, self).__init__()
        self.setupUi(self)
        self.label_5.setText(
            '---Help : '
            '<a href="https://github.com/UltraBlur/UltraRawConverter">'
            '     Github</a>')
        self.label_5.setOpenExternalLinks(True)
        self.show()
        self.exec()


DialogAbout = DialogAboutWindow


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(f'{os.path.abspath("")}/Pic/logo.png'))
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.statusBar().showMessage('Ready')
# 初始化数值
        self.exp = 0

# 菜单栏初始化
        self.actionAdd_Source.triggered.connect(newfilelist.fileAddToList)
        self.actionDestination.triggered.connect(newfilelist.setDestination)
        self.actionAbout.triggered.connect(DialogAbout)


# 按钮初始化以及信号槽的选择
        self.toolButton_AddSource.clicked.connect(newfilelist.fileAddToList)
        self.Button_Start.clicked.connect(StartConvert)
        self.toolButton_Des.clicked.connect(newfilelist.setDestination)
        self.toolButton_Preview.clicked.connect(Preview)

# ComboBox 初始化
        self.comboBox_Bps.setCurrentIndex(0)
        self.comboBox_ColorSpace.setCurrentIndex(6)
        self.comboBox_Gamma.setCurrentIndex(0)
        self.comboBox_NoiseReduction.setCurrentIndex(0)
        self.comboBox_Format.setCurrentIndex(0)
        self.comboBox_Rolloff.setCurrentIndex(0)

# ComboBox 信号槽
        self.comboBox_Bps.currentIndexChanged.connect(self.RTF_Bps)
        self.comboBox_ColorSpace.currentIndexChanged.connect(
            self.RTF_ColorSpace)
        self.comboBox_Gamma.currentIndexChanged.connect(self.RTF_Gamma)
        self.comboBox_NoiseReduction.currentIndexChanged.connect(self.RTF_NR)
        self.comboBox_Format.currentIndexChanged.connect(self.RTF_Format)
        self.comboBox_Format.setToolTip(
            'PNG is not recommended because of the slow speed.')
        self.comboBox_Rolloff.currentIndexChanged.connect(self.RTF_RollOff)

# ChechBox 信号槽
        self.checkBox_UseCameraWB.setChecked(True)
        self.checkBox_AutoBright.stateChanged.connect(self.RTF_AutoBright)
        self.checkBox_UseCameraWB.stateChanged.connect(self.RTF_UseCameraWB)

# TableWidget 更新操作
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.resizeColumnsToContents()

# horizontalSlider 数据更新
        self.horizontalSlider_Expo.sliderReleased.connect(self.RTF_Exp)
        self.horizontalSlider_RollOff.sliderReleased.connect(
            self.RTF_RollOff_Slider)
        self.label_ExposureShift.setToolTip(
            'Turn on when "Auto Bright" is off.')
        self.label_RollOffReConstruct.setToolTip(
            'Turn on when using "ReConstruct" of Roll-Off" mode. ')
        self.label_RollOffReConstruct.setText(
            f' Highlight Roll-Off ReConstruct: Off')
        self.label_ExposureShift.setText(
            f' Exposure Shift:  0.0EV')

# textBrower_info 初始化
        self.textBrowser_info.append('-----------------------------------')

    def TableWidgets_update(self, rows_number, path_list):
        self.tableWidget.setRowCount(rows_number)
        self.count = 0
        for path in path_list:
            filename_list = path.split('/')
            self.filename = filename_list[-1]
            Ready = QtWidgets.QTableWidgetItem("Ready")
            Resolution = QtWidgets.QTableWidgetItem(RTF.metadata_sizes(path))

            self.tableWidget.setItem(self.count, 0, Ready)
            self.tableWidget.setItem(
                self.count, 1, QtWidgets.QTableWidgetItem(self.filename))
            self.tableWidget.setItem(self.count, 2, Resolution)
            self.tableWidget.resizeColumnsToContents()

            self.count += 1

    def TableWidgets_Done(self, rows_number):
        Done = QtWidgets.QTableWidgetItem("Done")
        Done.setForeground(QtGui.QBrush(QtGui.QColor(68, 180, 50)))
        self.tableWidget.setItem(rows_number, 0, Done)

# TextBrowser 显示导出目的地

    def TextBrowser_Destination_Update(self, des):
        self.textBrowser_Destination.clear()
        self.textBrowser_Destination.append(des)
        self.textBrowser_Destination.moveCursor(
            self.textBrowser_Destination.textCursor().Start)

# TextBrowser 日志更新
    def TextBrower_info_update(self, msg):
        self.textBrowser_info.append(msg)

# 进度条更新
    def pgb_update(self, i):
        self.i = i
        return self.progressBar.setValue(self.i)

# ComboBox 同步更新到RawToTiff

    def RTF_Gamma(self):
        gamma_dic = {
            "Linear": (1, 1),
            "BT.709": (2.222, 4.5),
            "sRGB": (2.222, 4.5)
        }
        gamma_index = gamma_dic.get(self.comboBox_Gamma.currentText())
        print(gamma_index)
        return RTF.change_gamma(new_gamma=gamma_index)

    def RTF_Bps(self):
        bps_index = int(self.comboBox_Bps.currentText())
        print(bps_index)
        return RTF.change_output_bps(new_output_bps=bps_index)

    def RTF_NR(self):
        NR_dic = {
            "off": 0,
            "Light": 1,
            "Full": 2
        }
        NR_index = int(NR_dic.get(self.comboBox_NoiseReduction.currentText()))
        print(NR_index)
        return RTF.change_fbdd_noise_Reduction(new_fbdd_noise_Reduction=NR_index)

    def RTF_ColorSpace(self):
        ColorSpace_dic = {
            "AdobeRGB": 2,
            "ProPhoto": 4,
            "Wide Color Gamut": 3,
            "XYZ": 5,
            "raw": 0,
            "sRGB": 1,
            "ACES": 6
        }
        colorspace_index = int(ColorSpace_dic.get(
            self.comboBox_ColorSpace.currentText()))
        print(colorspace_index)
        return RTF.change_ColorSpace(new_ColorSpace=colorspace_index)

    def RTF_AutoBright(self):
        if self.checkBox_AutoBright.checkState():
            AB_bool = False
        else:
            AB_bool = True
        print(AB_bool)
        return RTF.change_no_auto_bright(AB_bool)

    def RTF_UseCameraWB(self):
        if self.checkBox_UseCameraWB.checkState():
            UserWB_bool = True
        else:
            UserWB_bool = False
        print(UserWB_bool)
        return RTF.change_use_camera_wb(UserWB_bool)

    def RTF_Format(self):
        return RTF.change_format(self.comboBox_Format.currentText())

    def RTF_Exp(self):
        self.exp = self.horizontalSlider_Expo.value()/3
        self.label_ExposureShift.setText(
            f' Exposure Shift:  {round(self.exp,3)}EV')
        return RTF.change_exp(self.exp)

    def RTF_RollOff(self):
        RollOff_Dic = {
            'Clip': 0,
            'Ignore': 1,
            'Blend': 2,
            'ReConstruct': 5
        }
        if self.comboBox_Rolloff.currentText() == 'ReConstruct':
            self._RollOff = self.horizontalSlider_RollOff.value()
            self.label_RollOffReConstruct.setText(
                f' Highlight Roll-Off ReConstruct:  {self._RollOff}')

        else:
            self._RollOff = RollOff_Dic.get(
                self.comboBox_Rolloff.currentText())
            self.label_RollOffReConstruct.setText(
                ' Highlight Roll-Off ReConstruct: Off')
        return RTF.change_RollOff(self._RollOff)

    def RTF_RollOff_Slider(self):
        if self.comboBox_Rolloff.currentText() == "ReConstruct":
            self._RollOff = self.horizontalSlider_RollOff.value()
            self.label_RollOffReConstruct.setText(
                f' Highlight Roll-Off ReConstruct:  {self._RollOff}')
            return RTF.change_RollOff(self._RollOff)

# 转换后日志信息返回

    def info_return(self):
        msg = [f'Gamma: {self.comboBox_Gamma.currentText()}',
               f'Bit Depth: {self.comboBox_Bps.currentText()}',
               f'ColorSpace: {self.comboBox_ColorSpace.currentText()}',
               f'Noise Reduction: {self.comboBox_NoiseReduction.currentText()}',
               f'Format: {self.comboBox_Format.currentText()}',
               f'Exposure Shift: {round(self.exp,3)}',
               f'Roll-Off Mode: {self.comboBox_Rolloff.currentText()}']
        if self.checkBox_UseCameraWB.checkState():
            msg.append(f'Use Camera WB')
        else:
            msg.append(f'Use Auto WB')

        if self.checkBox_AutoBright.checkState():
            msg.append(f'Use Auto Bright')

        return msg


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
