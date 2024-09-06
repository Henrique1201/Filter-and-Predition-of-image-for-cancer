import cv2
import pandas as pd
import numpy as np


def read_pgm_test(file_path):
    imagem = cv2.imread(f'{file_path}', cv2.IMREAD_UNCHANGED)
    df = pd.DataFrame(imagem)

    print(df.head(20))
    print(df.shape)

    cv2.imshow('Imagem PGM', imagem)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

