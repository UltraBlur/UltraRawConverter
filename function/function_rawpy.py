#   LibRaw功能模块，使用rawpy、imageio库
import imageio
import os
import rawpy
from PyQt5.QtCore import QObject, pyqtSignal


class RawToTiff:

    def __init__(self):

        #   默认参数 16bit linear ACES Tiff, 降噪关闭， 使用相机白平衡
        self._gamma = (1, 1)
        self._no_auto_bright = True
        self._output_bps = 16
        self._ColorSpace = 6
        self._fbdd_NoiseReduction = 0
        self._use_camera_wb = True
        self._format = "tiff"
        self._exp = 0
        self._RollOff = 0

# 开始转换
    def run(self, path, destination):
        filename_list = path.split('/')
        filename = filename_list[-1]
        with rawpy.imread(path) as raw:
            pic = raw.postprocess(gamma=self._gamma, no_auto_bright=self._no_auto_bright,
                                  output_bps=self._output_bps, output_color=rawpy.ColorSpace(
                                      self._ColorSpace),
                                  fbdd_noise_reduction=rawpy.FBDDNoiseReductionMode(
                                      self._fbdd_NoiseReduction),
                                  use_camera_wb=(self._use_camera_wb),
                                  exp_shift=self._exp, highlight_mode=self._RollOff)

            self.wb = raw.daylight_whitebalance
            size = raw.sizes
            tc = raw.tone_curve
            rawtype = raw.raw_type
            cwb = raw.camera_whitebalance
            print(f'daylight_whitebalance:{self.wb}')
            print(f'sizes；{size}')
            print(f'tone_curve；{tc}')
            print(f'raw_type:{rawtype}')
            print(f'camera_whitebalance:{cwb}')

            imageio.imsave(
                f'{destination}/{filename}_C-{self._ColorSpace}_G-{self._gamma}_Exp-{round(self._exp,3)}.{self._format}', pic)


#  Jpeg 预览图生成

    def preview_image_run(self, path):
        filename_list = path.split('/')
        filename = filename_list[-1]
        with rawpy.imread(path) as raw:
            preview_pic = raw.postprocess(gamma=self._gamma, no_auto_bright=self._no_auto_bright,
                                          output_bps=self._output_bps, output_color=rawpy.ColorSpace(
                                              self._ColorSpace),
                                          fbdd_noise_reduction=rawpy.FBDDNoiseReductionMode(
                                              self._fbdd_NoiseReduction),
                                          use_camera_wb=(self._use_camera_wb),
                                          exp_shift=self._exp, highlight_mode=self._RollOff, half_size=1)
            pre_des = f'{os.path.abspath("")}/Cache/{filename}_Preview.jpg'
            imageio.imsave(pre_des, preview_pic)
            return pre_des

# 导出参数修改
    def change_gamma(self, new_gamma):
        self._gamma = new_gamma

    def change_no_auto_bright(self, new_no_auto_bright):
        self._no_auto_bright = new_no_auto_bright

    def change_output_bps(self, new_output_bps):
        self._output_bps = new_output_bps

    def change_ColorSpace(self, new_ColorSpace):
        self._ColorSpace = new_ColorSpace

    def change_fbdd_noise_Reduction(self, new_fbdd_noise_Reduction):
        self._fbdd_NoiseReduction = new_fbdd_noise_Reduction

    def change_use_camera_wb(self, new_use_camera_wb):
        self._use_camera_wb = new_use_camera_wb

    def change_format(self, new_format):
        self._format = new_format

    def change_exp(self, new_exp):
        self._exp = new_exp

    def change_RollOff(self, new_RollOff):
        self._RollOff = new_RollOff
        # 元数据Return

    def metadata_sizes(self, path):
        with rawpy.imread(path) as raw:
            sizes = raw.raw_image_visible
            width = sizes.shape[1]
            height = sizes.shape[0]
            sizes_output = f'{width}x{height}'
        return sizes_output


# list = 'C:/Users/UltraBlur/Desktop/Coding/UltraRawConverter/Timelapse_Sample/S1HP01B2351.RW2'
# des = 'C:/Users/UltraBlur/Desktop/Coding/UltraRawConverter/Timelapse_Sample/220826_Output'
# RTF = RawToTiff
# RTF.run(path = list, destination = des)
