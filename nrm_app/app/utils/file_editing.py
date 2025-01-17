from PIL import Image

def crop_to_square(input_path, output_path):
    print("ans: ", input_path)
    with Image.open(input_path) as img:
        width, height = img.size
        if width > height:
            left = (width - height) / 2
            top = 0
            right = (width + height) / 2
            bottom = height
        else:
            left = 0
            top = (height - width) / 2
            right = width
            bottom = (height + width) / 2

        # Przytnij obrazek do kwadratu
        img_cropped = img.crop((left, top, right, bottom))

        # Zapisz obrazek w nowym pliku
        img_cropped.save(output_path)

crop_to_square("/app/app/static/images/avatars/moje.png",
               "/app/app/static/images/avatars/logo.png")
