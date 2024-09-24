from Functions.Filter_Image import apply_mean_filter, quantize_image, create_scm
from PIL import Image
import pandas as pd
import os


directory_path = r"images"
for filename in os.listdir(directory_path):

    paths = os.path.join(directory_path,filename)

    if os.path.isfile(paths):

        image = Image.open(paths)
        mean_filter = apply_mean_filter(image, 3)
        quantization = quantize_image(mean_filter, 8)
        result_image = Image.fromarray(quantization)
        result_image.save(f'{paths}_filtered')
        scm = create_scm(quantization, distances=[1], angles=[0])
        scm_df = pd.DataFrame(scm)
        scm_df.to_csv(f'/Dataset/{paths}.csv', index=False, header=False)

