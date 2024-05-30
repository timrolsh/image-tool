# 0. Preparation : Installing the packages
# RUN THE ABOVE CODE BLOCKS BEFORE RUNNING THIS
#!pip install pillow-avif-plugin
#!pip install opencv-python

from PIL import Image
import os
import pandas as pd
import warnings

import removebg as REMBG
import crop as CROP

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
        img: Image = Image.open(f"input/{name}")
        if jobs[0]:
            img = REMBG.rembg("input/" + name, kSize)
        if jobs[1]:
            img = CROP.crop_image(img, kSize)
        if jobs[2] or jobs[3]:
            df = pd.read_excel("Input_setting.xlsx", sheet_name="Images")

            name_after = str(df.loc[i]["New Name"])
            target_h = df.loc[i]["Target Height"]

            # Resizing
            if jobs[2]:
                width, height = img.size
                new_width = int(width * target_h / height)
                img = img.resize((new_width, target_h))

            if jobs[3]:
                img.save("output/" + name_after + ".png", format="png")
                i += 1
                continue
        img.save("output/" + name, format="png")
        i += 1
    return "Complete!"
