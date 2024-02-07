# from pgmagick import Image

# image = Image("input/3077207647.jpeg")

# if background is None:
#     background = pgmagick.Image(image.size(), "white")
# elif isinstance(background, pgmagick.Image):
#     blob = pgmagick.Blob()
#     background.write(blob)
#     background = pgmagick.Image(blob, image.size())
# else:
#     background = pgmagick.Image(image.size(), background)
# background.composite(image, 0, 0, pgmagick.CompositeOperator.DifferenceCompositeOp)
# background.threshold(25)
# blob = pgmagick.Blob()
# image.write(blob)
# image = pgmagick.Image(blob, image.size())
# image.composite(background, 0, 0, pgmagick.CompositeOperator.CopyOpacityCompositeOp)
# return image
