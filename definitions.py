import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is the Project Root

RECIPES_FOLDER = os.path.join(ROOT_DIR, 'recipes')  # Directory to recipes
FILE_DIR = os.path.join(ROOT_DIR, 'files')  # Directory of stored files

HASHED_SHINGLES_FILE = os.path.join(FILE_DIR, 'hashed_shingles.p')
SHINGLES_FILE = os.path.join(FILE_DIR, 'shingles.p')

SIGNATURES_FILE = os.path.join(FILE_DIR, 'signatures.p')
