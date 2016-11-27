import io
import re
from bs4 import BeautifulSoup

RECIPES_FOLDER = 'D:/recipes'
SHINGLE_LENGTH = 4


def shingle():
    shingles = list()
    # open the recipes folder
    filename ="_81487.html"
    f = io.open(RECIPES_FOLDER + '/' + filename, 'r', encoding='utf-8')
    # set the scraper (using the lxml parser)
    soup = BeautifulSoup(f, 'lxml')

    # find the attributes and check them if are empty
    title = check_not_null(soup.find_all("h1", class_='content-title__text'))
    author = check_not_null(soup.find_all("a", class_='chef__link'))
    prepTime = check_not_null(soup.find_all("p", class_='recipe-metadata__prep-time'))
    cookTime = check_not_null(soup.find_all("p", class_='recipe-metadata__cook-time'))
    serving = check_not_null(soup.find_all("p", class_='recipe-metadata__serving'))
    dietary = check_not_null(soup.find_all("div", class_='recipe-metadata__dietary'))

    ingredients = check_not_null(soup.find_all("div", class_='recipe-ingredients-wrapper'))
    ingredients = re.sub('\s+', ' ', ingredients.strip().lstrip('Ingredients').lstrip())

    method = check_not_null(soup.find_all("div", class_='recipe-method-wrapper'))
    method = re.sub('\s+', ' ', method.strip().lstrip('Method').lstrip())

    shingles.append(get_shingle(title))
    shingles.append(get_shingle(author))
    shingles.append(get_shingle(prepTime))
    shingles.append(get_shingle(cookTime))
    shingles.append(get_shingle(serving))
    shingles.append(get_shingle(dietary))
    shingles.append(get_shingle(ingredients))
    shingles.append(get_shingle(method))

    f.close()

    print shingles


def get_shingle(string):
    shingles = list()
    for i in range(len(string) - SHINGLE_LENGTH + 1):
        print string[i:i + SHINGLE_LENGTH]
        shingles.append(string[i:i + SHINGLE_LENGTH])
    return shingles


def check_not_null(feature):
    if len(feature) > 0:
        return feature[0].text.strip()
    else:
        return u''

if __name__ == '__main__':
    shingle()