import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from qtpy import QtGui
from CoordinateCalculation import CoordinateCalculation
from View import View
from configs import config
from player import MainWindow
from threading import Thread
import time

from ErrorCorrector import ErrorCorrector


class PlayerHandler(MainWindow):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.treatment, daemon=True)
        self.finalHandler = None
        self.errorCorrector = ErrorCorrector()
        self.viewTrack = None

    def start_processing(self):
        self.set_default_values_configs()
        self.toggle_button_activity()
        self.is_brake = False
        self.thread.start()

    def toggle_button_activity(self):
        self.button_corrector.setEnabled(not self.button_corrector.isEnabled())
        self.button_viewTrack.setEnabled(not self.button_viewTrack.isEnabled())
        self.button_choose_dir.setEnabled(not self.button_choose_dir.isEnabled())
        self.button_choose_GPX.setEnabled(not self.button_choose_GPX.isEnabled())
        self.button_choose_geojson.setEnabled(not self.button_choose_geojson.isEnabled())
        self.button_treatment.setEnabled(not self.button_treatment.isEnabled())
        self.button_end.setEnabled(not self.button_end.isEnabled())

    def set_default_values_configs(self):
        config.VIDEOS = []
        config.FRAME_STEP = 5
        config.COUNT_PROCESSED_FRAMES = 0
        config.INDEX_OF_FRAME = 5000
        config.INDEX_OF_VIDEO = 0
        config.INDEX_OF_All_FRAME = config.INDEX_OF_FRAME + (63600 * config.INDEX_OF_VIDEO)
        config.INDEX_OF_GPS = int(round(config.INDEX_OF_All_FRAME / 60, 0))
        config.INDEX_OF_SING = 0

    def finish_processing(self):
        self.toggle_button_activity()
        self.finalHandler.save_result(self.view.sign_handler.result_signs, self.view.sign_handler.side_signs,
                                      self.view.sign_handler.turns)
        self.errorCorrector.create_image_with_errors()
        self.view.cap.release()
        self.is_brake = True
        self.thread.join()
        self.thread = Thread(target=self.treatment, daemon=True)

    def treatment(self):
        self.calculation = CoordinateCalculation()
        self.view = View()
        self.view.count_frames()
        count_gpx = self.Reader.get_count_dot()
        start_time = time.time()

        while self.view.cap.isOpened():
            if self.is_brake:
                break
            speed = self.Reader.get_speed(config.INDEX_OF_GPS)
            config.FRAME_STEP = round(self.k * speed + self.b, 0)
            ret, frame = self.view.cap.read()
            if ret:
                if config.INDEX_OF_All_FRAME + 100 > config.COUNT_FRAMES:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print('Elapsed time: ', elapsed_time / 60)
                    self.finish_processing()
                    break
                self.label.setPixmap(self.convert_cv_qt(frame))
                config.COUNT_PROCESSED_FRAMES += 1
                if round(speed, 0) != 0:
                    retangles = self.view.draw_rectangles(frame)
                    self.label.setPixmap(self.convert_cv_qt(frame))
                    if not retangles:
                        self.count_empty += 1
                    else:
                        self.count_empty = 0
            self.switch_frame()
            if self.view.switch_video():
                break
            while self.is_wait:
                pass
        #except Exception as e:
        #    print("error", e)
        #    print('frame', config.INDEX_OF_FRAME)
        print("end")

    def switch_frame(self):
        config.INDEX_OF_FRAME += config.FRAME_STEP
        config.INDEX_OF_All_FRAME += config.FRAME_STEP

        count_frame_for_gps = config.INDEX_OF_All_FRAME - (config.INDEX_OF_GPS * 60)
        if count_frame_for_gps > 60:
            config.INDEX_OF_GPS += 1
        self.view.cap.set(cv2.CAP_PROP_POS_FRAMES, config.INDEX_OF_FRAME)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(960, 540, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
