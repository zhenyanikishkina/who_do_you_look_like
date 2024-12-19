import os
import numpy as np
from PIL import Image

import scipy.io
import pandas as pd
from datetime import datetime, timedelta

import asyncio
from tqdm.asyncio import tqdm

import faiss

from utils.database import CelebDatabase
from config import LMDB_PATH_MALE, LMDB_PATH_FEMALE, FAISS_PATH_MALE, FAISS_PATH_FEMALE, DATASET_PATH
from utils.face_embedding import preprocess, get_face_embedding


async def get_best_images():
    mat_data = scipy.io.loadmat(os.path.join(DATASET_PATH, 'imdb_crop/imdb.mat'))
    dt = mat_data['imdb'][0, 0]
    keys_s = ('gender', 'dob', 'photo_taken',
              'face_score', 'second_face_score', 'celeb_id')
    values = {k: dt[k].squeeze() for k in keys_s}
    keys_n = ('full_path', 'name')
    for k in keys_n:
        values[k] = np.array([x if not x else x[0] for x in dt[k][0]])
    values['face_location'] =\
        [tuple(x[0].tolist()) for x in dt['face_location'].squeeze()]
    set_nrows = {len(v) for _, v in values.items()}

    assert len(set_nrows) == 1

    df_values = pd.DataFrame(values)
    matlab_origin = datetime(1, 1, 1)
    days_offset = timedelta(days=366)

    def matlab_datenum_to_datetime(datenum):
        try:
            if datenum > 0 and datenum < 3652059:
                return matlab_origin + timedelta(days=datenum) - days_offset
            else:
                return pd.NaT
        except OverflowError:
            return pd.NaT

    df_values['dob'] = df_values['dob'].apply(matlab_datenum_to_datetime)
    filtered_df = df_values[(df_values['face_score'] > 0) & (df_values['second_face_score'].isna())]

    best_images = (
        filtered_df.sort_values(by=['face_score', 'photo_taken'], ascending=[False, False])
        .groupby('celeb_id')
        .first()
        .reset_index()
    )
    best_images = best_images.drop(columns=['second_face_score', 'celeb_id'])

    return (
        best_images[best_images['gender'] == 0]['full_path'].values,
        best_images[best_images['gender'] == 0]['name'].values,
        best_images[best_images['gender'] == 1]['full_path'].values,
        best_images[best_images['gender'] == 1]['name'].values
    )


async def process_image(key, path, name, lmdb_db, all_embeddings):
    # YOUR_CODE_HERE

    try:
        # YOUR_CODE_HERE
    except Exception as e:
        # YOUR_CODE_HERE


async def build():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Celebrity dataset directory '{DATASET_PATH}' not found.")

    if not os.path.exists(LMDB_PATH_FEMALE):
        os.makedirs(LMDB_PATH_FEMALE)
    female_lmdb_db = CelebDatabase(LMDB_PATH_FEMALE)
    if not os.path.exists(LMDB_PATH_MALE):
        os.makedirs(LMDB_PATH_MALE)
    male_lmdb_db = CelebDatabase(LMDB_PATH_MALE)

    # YOUR_CODE_HERE


if __name__ == "__main__":
    asyncio.run(build())