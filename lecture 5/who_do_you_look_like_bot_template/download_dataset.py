import kagglehub
from config import DATASET_PATH


path = kagglehub.dataset_download("abhikjha/imdb-wiki-faces-dataset", path=DATASET_PATH)
print("Path to dataset files:", path)
