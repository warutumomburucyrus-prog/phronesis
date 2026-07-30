from PIL import Image, ImageTk



def load_icon(path, size=(24,24)):

    image = Image.open(path)

    image = image.resize(
        size,
        Image.LANCZOS
    )

    return ImageTk.PhotoImage(image)