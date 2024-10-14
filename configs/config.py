#! /usr/bin/env python
# -*- coding: utf-8 -*-
PATH_TO_VIDEO = r"E:\Urban\vid\test\GOPR0064"  #"./"
VIDEOS = []
FRAME_STEP = 5
COUNT_PROCESSED_FRAMES = 0

INDEX_OF_FRAME = 0
INDEX_OF_VIDEO = 0
INDEX_OF_All_FRAME = INDEX_OF_FRAME + (63600 * INDEX_OF_VIDEO)
INDEX_OF_GPS = int(round(INDEX_OF_All_FRAME / 60, 0))

INDEX_OF_SING = 0
PATH_TO_GEOJSON = r"E:\Urban\vid\20,06,24-Вишевичи+\20,04,24-Вишевичи.geojson"#r"D:\Urban\vid\test\city3.geojson"  #"./"
PATH_TO_GPX = r"E:\Urban\vid\20,06,24-Вишевичи+\20,04,24-Вишевичи.gpx"#r"D:\Urban\vid\test\07,07,20211.gpx"  #"./"#
COUNT_FRAMES = 0

ClASSIFIER = {}
###63600
FEATURES = []


SECONDES_ALL_VIDEO = 0

#print( 628161 // 63600)
