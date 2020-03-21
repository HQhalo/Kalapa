from config import *


def load_train_dataset(path = PATH,filename = FILENAME_TRAIN):
    pathfile = os.path.join(path,filename)
    return pd.read_csv(pathfile,na_values = NA_VALUE)

def load_test_dataset(path = PATH,filename = FILENAME_TEST):
    pathfile = os.path.join(path,filename)
    return pd.read_csv(pathfile,na_values = NA_VALUE)

    
        