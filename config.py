PATH_TO_VIDEO = r"D:\Urban\vid\test\GOPR0083"
FRAME_STEP = 5
INDEX_OF_FRAME = 19800 - 60
COUNT_PROCESSED_FRAMES = 0
INDEX_OF_All_FRAME =  + 63600 * 1 - 60
INDEX_OF_GPS = 330 + 1060 * 1 - 1
INDEX_OF_VIDEO = 1
INDEX_OF_SING = 0
PATH_TO_GEOJSON = "save/myfile.geojson"
PATH_TO_GPX = r"D:\Urban\vid\test\07,07,20211.gpx"
COUNT_FRAMES = 0

ClASSIFIER = {}
###63600
FEATURES = []
DEVIATION = { 0:{"h/w": 1.06, "w/h": 0.94, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
              1:{"h/w": 0.97, "w/h": 1.03, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
              2:{"h/w": 1.08, "w/h": 0.92, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
              3:{"h/w": 1.04, "w/h": 0.96, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
              4:{"h/w": 1.14, "w/h": 0.88, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
              5:{"h/w": 1.07, "w/h": 0.94, "deviation_h/w": 0.2, "deviation_w/h": 0.5},
              6:{"h/w": 0.46, "w/h": 2.19, "deviation_h/w": 0.2, "deviation_w/h": 0.5},
              7:{"h/w": 0.64, "w/h": 1.56, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
              8:{"h/w": 0.97, "w/h": 1.03, "deviation_h/w": 0.4, "deviation_w/h": 0.5},
              9:{"h/w": 1.12, "w/h": 0.89, "deviation_h/w": 0.4, "deviation_w/h": 0.5},
             10:{"h/w": 1.6,  "w/h": 0.63, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             11:{"h/w": 1.16, "w/h": 0.86, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             12:{"h/w": 1.04, "w/h": 0.96, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             13:{"h/w": 1.12, "w/h": 0.9,  "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             14:{"h/w": 1.42, "w/h": 0.71, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             15:{"h/w": 1.05, "w/h": 0.95, "deviation_h/w": 0.2, "deviation_w/h": 0.5},
             16:{"h/w": 1.7,  "w/h": 0.59, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             17:{"h/w": 0.56, "w/h": 1.78, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             18:{"h/w": 0.72, "w/h": 1.38, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             19:{"h/w": 1.1,  "w/h": 0.91, "deviation_h/w": 0.2, "deviation_w/h": 0.4},
             20:{"h/w": 0.99, "w/h": 1.01, "deviation_h/w": 0.2, "deviation_w/h": 0.4},
             21:{"h/w": 0.62, "w/h": 1.6,  "deviation_h/w": 0.2, "deviation_w/h": 0.8},
             22:{"h/w": 0.63, "w/h": 1.58, "deviation_h/w": 0.2, "deviation_w/h": 0.8},
             23:{"h/w": 0.31, "w/h": 3.23, "deviation_h/w": 0.2, "deviation_w/h": 0.8},
             24:{"h/w": 0.31, "w/h": 3.19, "deviation_h/w": 0.2, "deviation_w/h": 0.8},
             25:{"h/w": 0.3,  "w/h": 3.28, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             26:{"h/w": 0.31, "w/h": 3.2,  "deviation_h/w": 0.2, "deviation_w/h": 0.5},
             27:{"h/w": 1.12, "w/h": 0.89, "deviation_h/w": 0.2, "deviation_w/h": 0.2},
             28:{"h/w": 0.29, "w/h": 3.4,  "deviation_h/w": 0.2, "deviation_w/h": 0.5}
             }
DEVIATION_RANGE = {
            0: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            1: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            2: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            3: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            4: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            5: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            6: {'range_min_h': 0.25, 'range_max_h': 0.60, 'range_min_w': 1.69, 'range_max_w': 4.009},
            7: {'range_min_h': 0.3, 'range_max_h': 1.35, 'range_min_w': 0.7, 'range_max_w': 2.7},
            8: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            9: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            10: {'range_min_h': 0.85, 'range_max_h': 2.7, 'range_min_w': 0.4, 'range_max_w': 1.1},
            11: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            12: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            13: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            14: {'range_min_h': 0.9, 'range_max_h': 2.1, 'range_min_w': 0.5, 'range_max_w': 1.1},
            15: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            16: {'range_min_h': 1.2, 'range_max_h': 2, 'range_min_w': 0.39, 'range_max_w': 0.79},
            17: {'range_min_h': 0.36, 'range_max_h': 1, 'range_min_w': 1.2, 'range_max_w': 3},
            18: {'range_min_h': 0.52, 'range_max_h': 1.2, 'range_min_w': 1.1, 'range_max_w': 1.6},
            19: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            20: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            21: {'range_min_h': 0.4, 'range_max_h': 0.8, 'range_min_w': 0.8, 'range_max_w': 2.4},
            22: {'range_min_h': 0.43, 'range_max_h': 0.83, 'range_min_w': 0.78, 'range_max_w': 2.38},
            23: {'range_min_h': 0.11, 'range_max_h': 0.51, 'range_min_w': 2.43, 'range_max_w': 4.03},
            24: {'range_min_h': 0.11, 'range_max_h': 0.51, 'range_min_w': 2.39, 'range_max_w': 3.99},
            25: {'range_min_h': 0.1, 'range_max_h': 0.5, 'range_min_w': 3.08, 'range_max_w': 3.48},
            26: {'range_min_h': 0.11, 'range_max_h': 0.51, 'range_min_w': 2.7, 'range_max_w': 3.7},
            27: {'range_min_h': 0.57, 'range_max_h': 2, 'range_min_w': 0.63, 'range_max_w': 1.52},
            28: {'range_min_h': 0.09, 'range_max_h': 0.49, 'range_min_w': 2.9, 'range_max_w': 3.9}}

