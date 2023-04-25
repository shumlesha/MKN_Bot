import io
from deep_translator import GoogleTranslator
import fitz
from PIL import Image
from io import BytesIO

def foo(x):
    if len(x) > 3:
        return x
    else:
        return None

def normalization(s):
    alphabet = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]
    symbols = list(range(97, 123)) + list(range(65, 91)) + [ord(str(i)) for i in range(10)] + [ord(' ')] + [ord(el) for el in alphabet] + [ord(el.upper()) for el in alphabet]
    p = ''
    for el in s:
        c = ord(el)
        if c in symbols:
            p += chr(c)
    s = p.lower()

    old = s.split(' ')
    full_info = [foo(el) for el in old]
    new = [el for el in old if len(el) > 3]
    t = ''

    for elem in new:
        t += elem + ' '

    leftpointer = len(full_info) - 1
    while leftpointer >= 0:
        if full_info[leftpointer] is None:
            break
        leftpointer -= 1

    if leftpointer + 1 != len(old):
        t = t[:-1]

    return t

def LevensteinDistance(s1, s2):
    DynamicProg = [[0] * (len(s2) + 1) for i in range(len(s1) + 1)]

    for i in range(len(s1) + 1):
        DynamicProg[i][0] = i

    for j in range(len(s2) + 1):
        DynamicProg[0][j] = j

    DynamicProg[0][0] = 0
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                DynamicProg[i][j] = DynamicProg[i - 1][j - 1]
            else:
                DynamicProg[i][j] = 1 + min(DynamicProg[i - 1][j], DynamicProg[i - 1][j - 1], DynamicProg[i][j - 1])

    return DynamicProg[len(s1)][len(s2)]

def TextCompare(text1, text2):
    ans = []
    s1, s2 = text1.split(), text2.split()
    kolvo = 0
    len1, len2 = len(s1), len(s2)

    for w1 in s1:
        for w2 in s2:
            l1, l2 = len(w1), len(w2)
            h = c = 0
            while h < l1 - 1 and h < l2 - 1:
                c += (w1[h] + w1[h + 1] == w2[h] + w2[h + 1])
                h += 1
            if (c / (l1 + l2 - c)) > 0.45:
                kolvo += 1
    res = (kolvo / (len1 + len2 - kolvo))
    if res > 0.25:
        ans.append(1)
    else:
        ans.append(res)
    return ans


def finder(InputText):
    distances = {}
    NormilzedInput = normalization(InputText)
    for ind in range(len(text)):
        TranslatedVersion = GoogleTranslator(source='auto', target='ru').translate(text[ind])
        TextToStr = ''.join(TranslatedVersion.split('\n'))
        NormalizedVersion = normalization(TextToStr)
        #print(TextToStr)
        print(NormalizedVersion)
        #print(InputText)
        print('======\n'*3)
        distances[ind] = (LevensteinDistance(NormalizedVersion, NormilzedInput), TextCompare(NormalizedVersion, NormilzedInput))
    print(distances)
    return min(distances, key = lambda x: distances[x])




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

#TranslatedText = GoogleTranslator(source='auto', target='ru').translate(text[1]) # Переводим текст

#print(text[1])
#print('==========\n'*2)
#print(TranslatedText)

s = input()

print(f'Скорее всего, вы имели ввиду страницу с номером {finder(s)}')
