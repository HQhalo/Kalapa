from config import *
class EncodeLabelNan():

    def fit_transform(self,data):
        dataset = data.copy()
        unique_values = dataset.value_counts().index
        encode_values = list(range(1,len(unique_values)+1))

        dict_encode = dict(zip(unique_values,encode_values))

        dataset = dataset.apply(lambda x: dict_encode[x] if x in dict_encode else np.nan)
    
        return dataset 
            