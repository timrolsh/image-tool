# 0. Preparation : Installing the packages
# RUN THE ABOVE CODE BLOCKS BEFORE RUNNING THIS
#!pip install pillow-avif-plugin
#!pip install opencv-python

import warnings

warnings.filterwarnings("ignore")

import pillow_avif
import pandas as pd
import numpy as np
import cv2
import re
import os

from PIL import Image


def CreateExcel():
    writer = pd.ExcelWriter("Input_setting.xlsx", engine="xlsxwriter")

    # 1. Setting Sheet
    input_setting = pd.DataFrame(
        index=[
            "1.Convert to PNG ONLY",
            "2.Background Removal (WIP)",
            "3.Crop to Content (WIP)",
            "4.Resize (Must do all images)",
            "5.Rename (Must do all images)",
        ],
        columns=["Check"],
    )
    input_setting.to_excel(writer, sheet_name="setting")

    workbook = writer.book
    worksheet = writer.sheets["setting"]

    cell_format = workbook.add_format()
    cell_format.set_bg_color("yellow")
    cell_format.set_align("center")

    cell_format2 = workbook.add_format()
    cell_format2.set_align("center")

    cell_format3 = workbook.add_format()
    cell_format3.set_bold()
    cell_format3.set_align("center")

    worksheet.data_validation("B2", {"validate": "list", "source": ["Y", " "]})
    worksheet.write("B2", "", cell_format)

    worksheet.data_validation("B3", {"validate": "list", "source": ["Y", " "]})
    worksheet.write("B3", "", cell_format)
    worksheet.write("C3", "2.1. Sensitivity(bg_threshold)", cell_format3)
    worksheet.data_validation(
        "D3",
        {
            "validate": "integer",
            "criteria": "between",
            "minimum": "1",
            "maximum": "255",
        },
    )
    worksheet.write("D3", 250, cell_format)

    worksheet.data_validation("B4", {"validate": "list", "source": ["Y", " "]})
    worksheet.write("B4", "", cell_format)
    worksheet.write("C4", "3.1. Sensitivity(k_size)", cell_format3)
    worksheet.data_validation(
        "D4",
        {"validate": "integer", "criteria": "between", "minimum": "1", "maximum": "20"},
    )
    worksheet.write("D4", 5, cell_format)

    worksheet.data_validation("B5", {"validate": "list", "source": ["Y", " "]})
    worksheet.write("B5", "", cell_format)

    worksheet.data_validation("B6", {"validate": "list", "source": ["Y", " "]})
    worksheet.write("B6", "", cell_format)

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 1, 10)
    worksheet.set_column(2, 2, 30)
    worksheet.set_column(3, 3, 10)

    # 2. Image List Sheet
    dir_list = os.listdir("input")

    name_list = list()
    height_list = list()
    width_list = list()

    for i in range(len(dir_list)):
        pattern = r"([A-Za-z0-9_-]+)."
        name = re.findall(pattern, dir_list[i])[0]
        im = Image.open("input/" + dir_list[i])
        width, height = im.size

        name_list.append(dir_list[i])
        height_list.append(height)
        width_list.append(width)

    image_df = pd.DataFrame(
        index=list(range(1, len(dir_list) + 1)),
        columns=["Current Name", "Height", "Width", "New Name", "Target Height"],
    )

    image_df["Current Name"] = name_list
    image_df["Height"] = height_list
    image_df["Width"] = width_list
    image_df.to_excel(writer, sheet_name="Images")

    worksheet = writer.sheets["Images"]
    for j in range(len(dir_list)):
        worksheet.write("E" + str(j + 2), "", cell_format)
        worksheet.write("F" + str(j + 2), "", cell_format)

    worksheet.set_column(0, 0, 10)
    worksheet.set_column(1, 1, 30)
    worksheet.set_column(2, 2, 10)
    worksheet.set_column(3, 3, 10)
    worksheet.set_column(4, 4, 30)
    worksheet.set_column(5, 5, 15)

    writer.close()
    workbook.close()

    print("Complete!")


def Setting():
    path = "input"
    d_path = "output"

    if not os.path.exists(path):
        os.makedirs(path)
        print("Please put all the images in the input folder and run this again!")

    else:
        if not os.path.exists(d_path):
            os.makedirs(d_path)
        CreateExcel()


def Run():
    df = pd.read_excel("Input_setting.xlsx", sheet_name=0)
    df2 = pd.read_excel("Input_setting.xlsx", sheet_name=1)
    jobs = list(np.where(df["Check"] == "Y", 1, 0))
    bg_threshold = df.loc[1]["Unnamed: 3"]
    k_size = int(df.loc[2]["Unnamed: 3"])

    # Crop to Contents >> source:https://youbidan.tistory.com/19 Note that there is some restriction on file format
    if jobs[2] == 1:
        for i in df2.index:
            pattern = r"([A-Za-z0-9_-]+)."
            name_before = re.findall(pattern, df2.loc[i]["Current Name"])[0]
            name_after = str(df2.loc[i]["New Name"])
            img = Image.open("input/" + df2.loc[i]["Current Name"])
            if jobs[4] == 1:
                img.save("output/" + name_after + ".png", format="png")
            else:
                img.save("output/" + name_before + ".png", format="png")

        for i in df2.index:
            pattern = r"([A-Za-z0-9_-]+)."
            name_before = re.findall(pattern, df2.loc[i]["Current Name"])[0]
            name_after = str(df2.loc[i]["New Name"])

            if jobs[4] == 1:
                image = cv2.imread("output/" + name_after + ".png")
                image_gray = cv2.imread(
                    "output/" + name_after + ".png", cv2.IMREAD_GRAYSCALE
                )
            else:
                image = cv2.imread("output/" + name_before + ".png")
                image_gray = cv2.imread(
                    "output/" + name_before + ".png", cv2.IMREAD_GRAYSCALE
                )

            b, g, r = cv2.split(image)
            image2 = cv2.merge([r, g, b])

            blur = cv2.GaussianBlur(image_gray, ksize=(k_size, k_size), sigmaX=0)
            ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
            edged = cv2.Canny(blur, 10, 250)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

            contours, _ = cv2.findContours(
                closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            total = 0

            contours_xy = np.array(contours)
            contours_xy.shape

            x_min, x_max = 0, 0
            value = list()
            for n in range(len(contours_xy)):
                for j in range(len(contours_xy[n])):
                    value.append(contours_xy[n][j][0][0])
                    x_min = min(value)
                    x_max = max(value)

            y_min, y_max = 0, 0
            value = list()
            for n in range(len(contours_xy)):
                for j in range(len(contours_xy[n])):
                    value.append(contours_xy[n][j][0][1])
                    y_min = min(value)
                    y_max = max(value)

            x = x_min
            y = y_min
            w = x_max - x_min
            h = y_max - y_min

            img_trim = image[y : y + h, x : x + w]

            if jobs[4] == 1:
                cv2.imwrite("output/" + name_after + ".png", img_trim)
            else:
                cv2.imwrite("output/" + name_before + ".png", img_trim)

    # All the other works
    for i in df2.index:
        pattern = r"([A-Za-z0-9_-]+)."
        name_before = re.findall(pattern, df2.loc[i]["Current Name"])[0]
        name_after = str(df2.loc[i]["New Name"])
        target_h = df2.loc[i]["Target Height"]

        if jobs[2] == 1:
            img = Image.open("output/" + name_after + ".png")
        else:
            img = Image.open("input/" + df2.loc[i]["Current Name"])

        # Background Removing
        if jobs[1] == 1:
            img = img.convert("RGBA")
            datas = img.getdata()
            newData = []
            for item in datas:
                if (
                    item[0] >= bg_threshold
                    and item[1] >= bg_threshold
                    and item[2] >= bg_threshold
                ):
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            img.putdata(newData)

        # Resizing
        if jobs[3] == 1:
            width, height = img.size
            new_width = int(width * target_h / height)
            img = img.resize((new_width, target_h))

        # Renaming & Converting to PNG
        if jobs[4] == 1:
            img.save("output/" + name_after + ".png", format="png")
        else:
            img.save("output/" + name_before + ".png", format="png")

    print("Complete!")


run = input()
if run.lower() == "setting" or "s":
    Setting()
elif run.lower() == "run" or "r":
    Run()
