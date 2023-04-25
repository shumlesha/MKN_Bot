import io

import fitz
from PIL import Image
from io import BytesIO

curfile = open('AllSolutions\InclassQuestions\MIT6_042JS15_cp1_solutions.pdf')

file = fitz.open('AllSolutions\InclassQuestions\MIT6_042JS15_cp1_solutions.pdf')

text = {}

for indx in range(len(file)):
    page = file[indx]
    textonpage = page.get_text() # Получаем текст решений (не нормализованный)
    images = page.get_images()

    # Получаем изображение из файла (рисунки решений)
    '''for imindx, img in enumerate(images, start=1):
        xref = img[0]

        base = file.extract_image(xref)
        bytes = base["image"]

        image = Image.open(io.BytesIO(bytes))

        image.show()'''
    text[indx] = textonpage

