from config import *
from encodeLabelNan import *
NO_NULL = 47
class PreProcessing:

    def drop_null_row(self):
        data_null = self.dataset.loc[np.sum(self.dataset.isnull(),axis=1) < 47]
        data_null_47 = self.dataset.loc[np.sum(self.dataset.isnull(),axis=1) == 47]
        data_null_48 = self.dataset.loc[np.sum(self.dataset.isnull(),axis=1) == 48]
        data_null_52 = self.dataset.loc[np.sum(self.dataset.isnull(),axis=1) == 52]
        
        data_null_47 = data_null_47.loc[data_null_47.iloc[:,1:-1].duplicated().map(lambda x: not x)]
        data_null_48 = data_null_48.loc[data_null_48.iloc[:,1:-1].duplicated().map(lambda x: not x)]
        data_null_52 = data_null_52.loc[data_null_52.iloc[:,1:-1].duplicated().map(lambda x: not x)]

        self.dataset = data_null.append(data_null_47).append(data_null_48).append(data_null_52)
    def combine_age(self,age1,age2):
        # if age1 == 0:
        #     if age2 == 0:
        #         return np.nan # all ages are null
        #     else:
        #         return age2
        # else:
        #     if age2 == 0:
        #         return age1
        #     else: 
        #         return int((age1+age2)/2)

        if age1 == age2:
            return age1
        else:
            return -999

    def processing_age(self):
        age1 = self.dataset.age_source1.fillna(-999)
        age2 = self.dataset.age_source2.fillna(-999)

        age = []
        
        for a1,a2 in zip(age1,age2):
            age.append(self.combine_age(a1,a2))
        self.dataset = self.dataset.drop(["age_source1","age_source2"],axis = 1)
        
        self.dataset["age"] = age
        # list(pd.cut(age,bins= list(range(0,101,BIN_AGE)),labels=list(range(0,int(100/BIN_AGE)))) )
    def encode_label(self):
        encode_cols = ["province","district","FIELD_8","FIELD_10","FIELD_11","FIELD_12","FIELD_13","FIELD_17","FIELD_24","FIELD_39",
        "FIELD_40","FIELD_41","FIELD_42","FIELD_44"]  
        encode_df = self.dataset[encode_cols]
        # temp = encode_df.astype("str") 
        encode_df = encode_df.apply(EncodeLabelNan().fit_transform)

        # encode_cols = temp.where(~encode_df.isnull(),np.nan)
        
        df_drop = self.dataset.drop(encode_cols,axis = 1)
        self.dataset = pd.concat([encode_df,df_drop],axis=1)    

    def encode_bool(self):
        encode_cols = ["FIELD_18","FIELD_19","FIELD_20","FIELD_23","FIELD_25","FIELD_26","FIELD_27","FIELD_28","FIELD_29",
        "FIELD_30","FIELD_31","FIELD_36","FIELD_37","FIELD_38"]

        encode_df = self.dataset[encode_cols]
        encode_df = encode_df.apply(EncodeLabelNan().fit_transform)
        
        df_drop = self.dataset.drop(encode_cols,axis = 1)
        self.dataset = pd.concat([encode_df,df_drop],axis=1) 
        
    def one_hot_encode(self):
        encode_cols = ["FIELD_8","FIELD_10"]  
    def processing_province(self):
        province = self.dataset.province.replace(to_replace = "Tỉnh Hoà Bình",value = "Tỉnh Hòa Bình")
        # self.dataset["province"] = province.map(lambda x: str(x).lower()).where(province.notnull(),province)

    def processing_district(self):
        district = self.dataset.district
        self.dataset["district"] = district.map(lambda x: str(x).lower()).where(district.notnull(),district)
        
    def drop_maCv(self):
        self.dataset = self.dataset.drop("maCv",axis = 1)

    def cutFIELD_3(self):
        F3_unique = self.dataset.FIELD_3.unique()
        F3_unique_sorted = np.sort(F3_unique)

        bins_F3 = []

        bins_F3+=[F3_unique_sorted[0]]

        for idx in range(1,len(F3_unique_sorted)):
            if F3_unique_sorted[idx] - F3_unique_sorted[idx -1] > 100:
                bins_F3 += [F3_unique_sorted[idx]]
        
        bins_F3 = np.array(bins_F3)
        bins_F3 -= 1

        self.dataset["FIELD_3"] = list(pd.cut(self.dataset.FIELD_3,bins= bins_F3,labels=list(range(0,len(bins_F3)-1))))
    def isHight(self,token):
        
        for i in token:
            if i in HIGHT:
                return True
        return False
    def isLow(self,token):
        for i in token:
            if i in LOW:
                return True
        
        return False
    def isNormal(self,token):
        return not (self.isHight(token) or self.isLow(token))

    def healthIsr_FIELD_7_9(self):
        
        HI_hight = [False for i in range(len(self.dataset))]
        HI_low = [False for i in range(len(self.dataset))]
        HI_normal = [False for i in range(len(self.dataset))]
        HI_none = [False for i in range(len(self.dataset))]

        idx = 0
        for i,j in zip(self.dataset.FIELD_7,self.dataset.FIELD_9):
            token = str(i)[2:-2].split("', '")
            token += [j]

            token = set(token)

            if len(token) == 0:
                HI_none[idx] = True
            if self.isHight(token):
                HI_hight[idx] = True
            if self.isLow(token):
                HI_low[idx] = True
            if self.isNormal(token):
                HI_normal[idx] = True
            idx +=1
        self.dataset = self.dataset.drop(["FIELD_7","FIELD_9"],axis = 1)
        self.dataset["HI_hight"] = HI_hight
        self.dataset["HI_low"] = HI_low
        self.dataset["HI_normal"] = HI_normal
        self.dataset["HI_none"] = HI_none
    

    def degree_FIELD_11(self):
        bins_degree = [-1,0,9,12,np.inf]
        label_degree = list(range(0,len(bins_degree)-1))
        self.dataset["FIELD_11"] = list(pd.cut(self.dataset.FIELD_11,bins= bins_degree,labels= label_degree))
        
    
    def cl_FIELD_12(self):

        data_12 = self.dataset.FIELD_12
        data_12 = data_12.replace(to_replace=["0.0","0"],value=0)
        data_12 = data_12.replace(to_replace=["1.0","1"],value=1)
        data_12 = data_12.where((data_12== 1) | (data_12 == 0),np.nan )

        self.dataset["FIELD_12"] = data_12
    def convert_field_35(self,val):
        if val == "Zero":
            return 0    
        elif val == "One":
            return 1     
        elif val == "Four":
            return 4    
        elif val == "Two":
            return 2     
        elif val == "Three":
            return 3
        return np.nan 
    def convert_field_43(self,val):
        if val == "A":
            return 0
        elif val == "B":
            return 1
        elif val == "C":
            return 2
        elif val == "D":
            return 3
        else:
            return np.nan
    
    def cl_FIELD_43(self):
        self.dataset["FIELD_43"] = self.dataset["FIELD_43"].apply(self.convert_field_43)


    def cl_FIELD_35(self):
        self.dataset["FIELD_35"] = self.dataset["FIELD_35"].apply(self.convert_field_35)

    def country_FIELD_39(self):
        country_code = self.dataset.FIELD_39
        country_code = country_code.fillna("NAA")
        country_code = country_code.map(lambda x: x if (x == "NAA" or x == "VN") else "FoR")
         
        self.dataset["FIELD_39"] = country_code
        
    def cl_FIELD_40(self):
        F40 = self.dataset.FIELD_40.replace(to_replace=["05 08 11 02"],value="02 05 08 11")
        F40 = F40.replace(to_replace = ["08 02","4"],value = np.nan)

        self.dataset["FIELD_40"] = F40

    def transform(self):
        if self.dropNa == True:
            self.drop_null_row()
        self.processing_age()       
        self.processing_province()
        self.processing_district()
        self.cutFIELD_3()
        self.healthIsr_FIELD_7_9()
        self.drop_maCv()
        self.degree_FIELD_11()
        self.cl_FIELD_12()
        self.cl_FIELD_35()
        self.cl_FIELD_40()
        self.cl_FIELD_43()
        self.country_FIELD_39()
        
        self.encode_label()
        self.encode_bool()

        return self.dataset

    def fit(self,dataset,dropNa = False):
        self.dataset = dataset.copy()
        self.dropNa = dropNa
    
    