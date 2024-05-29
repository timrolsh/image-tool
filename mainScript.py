# 0. Preparation : Installing the packages
# RUN THE ABOVE CODE BLOCKS BEFORE RUNNING THIS
#!pip install pillow-avif-plugin
#!pip install opencv-python

from PIL import Image
import os
import re
import cv2
import numpy as np
import pandas as pd
import warnings

import removebg as REMBG
import crop as CROP
import create_excel as ce

warnings.filterwarnings("ignore")


def Setting():
    path = "input"
    d_path = "output"

    if not os.path.exists(path):
        os.makedirs(path)
        print("Please put all the images in the input folder and run this again!")

    else:
        if not os.path.exists(d_path):
            os.makedirs(d_path)


def Run(rembg, crop, resize, rename, kSize):
    im_names = os.listdir("input")
    jobs = [rembg, crop, resize, rename]
    i = 0
    for name in im_names:
        if jobs[1] and jobs[0]:
            img = CROP.crop_image(("input/"+name), kSize)
            cv2.imwrite("curr_image.png", img)
            img = REMBG.rembg("curr_image.png", kSize)
            img.save("curr_image.png")
        elif jobs[0]:
            img = REMBG.rembg("input/" + name, kSize)
            img.save("curr_image.png")
        elif jobs[1]:
            img = CROP.crop_image("input/" + name, kSize)
            cv2.imwrite("curr_image.png", img)
        if jobs[2] or jobs[3]:
            img = Image.open("curr_image.png")
            df = pd.read_excel("Input_setting.xlsx", sheet_name="Images")
            print(df)

            pattern = r"([A-Za-z0-9_-]+)."
            name_before = re.findall(pattern, df.loc[i]["Current Name"])[0]
            name_after = str(df.loc[i]["New Name"])
            target_h = df.loc[i]["Target Height"]

            # Resizing
            if jobs[2]:
                width, height = img.size
                new_width = int(width * target_h / height)
                img = img.resize((new_width, target_h))

            if jobs[3]:
                img.save("output/" + name_after + ".png", format="png")
        if not jobs[3]:
            img = Image.open("curr_image.png")
            img.save("output/"+name, format="png")
        os.remove("curr_image.png")
        i += 1
    return "Complete!"


# run = input()
# if run.lower() == "setting":
#     Setting()
# elif run.lower() == "run":
#     Run(True, True, False, False, 7)
