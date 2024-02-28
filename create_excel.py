import pandas as pd
import re
import os
from PIL import Image
import pillow_avif
import warnings

def create_excel():
    warnings.filterwarnings("ignore")

    writer = pd.ExcelWriter("Input_setting.xlsx", engine="xlsxwriter")


    # Image List Sheet
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

    workbook = writer.book
    cell_format = workbook.add_format()
    cell_format.set_bg_color("yellow")
    cell_format.set_align("center")

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
