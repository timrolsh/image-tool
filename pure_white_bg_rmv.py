from PIL import Image
from pathlib import Path

folder = "input"
images = Path(folder).glob("*")
counter = 1
for i in images:
    img = Image.open(i)
    org_img = Image.open(
        i
    )  # this opens the highlighted image, and the original as a PIL image

    img = img.convert("RGBA")
    org_img = org_img.convert("RGBA")  # add the alpha color channel (transparency)
    datas = img.getdata()
    org_datas = org_img.getdata()
    # save every pixel in the images as an array of RGBA values into an array for both original and contoured
    # keep original to have the non green version

    newData = []

    for index, item in enumerate(datas):
        if (
            item[0] in range(250, 256)  # give a little leniency for more accuracy
            and item[1] in range(250, 256)  # green
            and item[2] in range(250, 256)
        ):
            newData.append(
                (255, 255, 255, 0)
            )  # if it's green save the original color from the original image
        else:
            newData.append(org_datas[index])  # transparent pixel

    img.putdata(newData)
    img.save("output/img_" + str(counter) + ".png", "PNG")
    counter += 1
