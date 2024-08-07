#! /usr/bin/env python
# -*- coding: utf-8 -*-
PATH_TO_VIDEO = r"D:\Urban\vid\test\Testing\25,03,24-Быстрица\100GOPRO"
FRAME_STEP = 5
COUNT_PROCESSED_FRAMES = 0

INDEX_OF_FRAME = 0
INDEX_OF_VIDEO = 0
INDEX_OF_All_FRAME = INDEX_OF_FRAME + (63600 * INDEX_OF_VIDEO)
INDEX_OF_GPS = int(round(INDEX_OF_All_FRAME / 60,0))

INDEX_OF_SING = 0
PATH_TO_GEOJSON =  r"D:\Urban\vid\test\Testing\25,03,24-Быстрица\Быстрица.geojson"
PATH_TO_GPX = r"D:\Urban\vid\test\07,07,20211.gpx"
COUNT_FRAMES = 0

ClASSIFIER = {}
###63600
FEATURES = []

