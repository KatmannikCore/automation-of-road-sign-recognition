import easyocr
import os
dir_for_read = [r"D:\Urban\learning\100\img\GOPR0108 (18.04.2023 8-31-09)",
                r"D:\Urban\learning\100\img\GP010106 (18.04.2023 8-36-19)",
                r"D:\Urban\learning\100\img\GP010107 (18.04.2023 8-35-59)",
                r"D:\Urban\learning\100\img\GP010108 (18.04.2023 8-29-12)",
                r"D:\Urban\learning\100\img\GP020106 (18.04.2023 8-35-00)",
                r"D:\Urban\learning\100\img\GP020107 (18.04.2023 8-34-39)",
                r"D:\Urban\learning\100\img\GP020108 (18.04.2023 8-27-10)",
                r"D:\Urban\learning\100\img\GP030106 (18.04.2023 8-33-37)",
                r"D:\Urban\learning\100\img\GP030107 (18.04.2023 8-33-16)",
                r"D:\Urban\learning\100\img\GP030108 (18.04.2023 8-25-11)",
                r"D:\Urban\learning\100\img\GP040106 (18.04.2023 8-31-54)",
                r"D:\Urban\learning\100\img\GP040107 (18.04.2023 8-31-23)",
                r"D:\Urban\learning\100\img\GP040108 (18.04.2023 8-23-13)",
                ]

reader = easyocr.Reader(["ru"])
for dir in dir_for_read:
    imgList = os.listdir(dir)
    for img_path in imgList:
        path = rf"{dir}\{img_path}"
        result = reader.readtext(path,batch_size=32)
        print(path)
        #result[0][0] - box
        #result[0][1] - data
        #result[0][2] - actualy
        if result:
            print(0)
            if result[0][2] > 0.1:
                print("123")
                print(result)
            else:
                os.remove(path)
        else:
            os.remove(path)
