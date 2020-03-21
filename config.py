import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer


PATH = "data"
FILENAME_TRAIN = "train.csv"
FILENAME_TEST = "test.csv"

NA_VALUE = ["None","na","[]","",-1]
HIGHT = ["TN","DK","DT","CN","HN","TS","HS"]
LOW = ["HC","CH"]