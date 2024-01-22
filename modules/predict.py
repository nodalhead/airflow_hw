import os
import dill
import pandas as pd
import glob
import json
from datetime import datetime

path = os.environ.get('PROJECT_PATH', '..')


def predict():
    with open(glob.glob(f'{path}/data/models/*.pkl')[-1], 'rb') as file:
        pipe = dill.load(file)

    test_data_df = pd.DataFrame()

    predictions_df = pd.DataFrame(columns=['id', 'pred'])

    for file in glob.glob(f'{path}/data/test/*.json'):
        with open(file, 'r') as json_file:
            test_data = json.load(json_file)
            test_data_tmp = pd.DataFrame([test_data])
            test_data_df = pd.concat([test_data_df, test_data_tmp], ignore_index=True)
            prediction = pipe.predict(test_data_tmp)
            file_name = os.path.splitext(os.path.basename(file))[0]
            predictions_tmp = pd.DataFrame({'id': [file_name], 'pred': prediction})
            predictions_df = pd.concat([predictions_df, predictions_tmp], ignore_index=True)

    predictions_df.to_csv(f'{path}/data/predictions/preds_{datetime.now().strftime("%Y%m%d%H%M")}.csv', index=False)


if __name__ == '__main__':
    predict()
