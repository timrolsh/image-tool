from PIL import Image

def rembg(filename: str, any):
    dot_index: int = filename.rfind(".")
    slash_index: int = filename.rfind("/")
    file: str = filename[slash_index + 1:dot_index]
    return Image.open(f"../removeBgCache/{file}.png")
