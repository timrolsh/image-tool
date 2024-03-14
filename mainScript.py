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
    jobs = [False,False,False,False]
    

    if rembg:
        counter = 1
        for name in im_names:
            img = REMBG.rembg("input/" + name, kSize)  # current kSize is a good spot (7) MUST BE ODD
            if crop:
                img = CROP.crop_image("input/" + name, kSize)
                cv2.imwrite(f'output/{counter}.png', img)
                counter += 1
            else:
                img.save(f"output/{counter}.png")
                counter += 1

    df = pd.read_excel("Input_setting.xlsx", sheet_name="Images")

    for i in df.index:
        pattern = r"([A-Za-z0-9_-]+)."
        name_before = re.findall(pattern, df.loc[i]["Current Name"])[0]
        name_after = str(df.loc[i]["New Name"])
        target_h = df.loc[i]["Target Height"]

        # Resizing
        if resize:
            width, height = img.size
            new_width = int(width * target_h / height)
            img = img.resize((new_width, target_h))

        # Renaming & Converting to PNG
        if rename:
            img.save("output/" + name_after + ".png", format="png")
        else:
            img.save("output/" + name_before + ".png", format="png")

    return "Complete!"


# run = input()
# if run.lower() == "setting":
#     Setting()
# elif run.lower() == "run":
#     Run(True, True, False, False, 7)
