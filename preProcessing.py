from config import *
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
        if age1 == 0:
            if age2 == 0:
                return np.nan # all ages are null
            else:
                return age2
        else:
            if age2 == 0:
                return age1
            else: 
                return int((age1+age2)/2)

    def processing_age(self,BIN_AGE = 5):
        age1 = dataset.age_source1.fillna(0)
        age2 = dataset.age_source2.fillna(0)

        age = []
        
        for a1,a2 in zip(age1,age2):
            age.append(combine_age(a1,a2))
        self.dataset = self.dataset.drop(["age_source1","age_source2"],axis = 1)
        
        self.dataset["age"] = pd.cut(age,bins= list(range(0,101,BIN_AGE)),labels=list(range(0,int(100/BIN_AGE))))    
        
    def processing_province(self):
        self.dataset.province = self.dataset.province.map(lambda x: str(x).lower())
        self.dataset.replace(to_replace = "Tỉnh Hoà Bình",value = "Tỉnh Hòa Bình")
        
    def processing_district(self):
        self.dataset.district = self.dataset.district.map(lambda x: str(x).lower())

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

        self.dataset["FIELD_3"] = pd.cut(self.dataset.FIELD_3,bins= bins_F3,labels=list(range(0,len(bins_F3)-1)))  
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
        self.dataset["FIELD_11"] = pd.cut(self.dataset.FIELD_11,bins= bins_degree,labels= label_degree)
    
    def cl_FIELD_12(self):

        data_12 = self.dataset.FIELD_12
        data_12 = data_12.replace(to_replace=["0.0","0"],value=0)
        data_12 = data_12.replace(to_replace=["1.0","1"],value=1)
        data_12 = data_12.replace(to_replace=["TN","HT"],value=np.nan)

        self.dataset["FIELD_12"] = data_12
    def country_FIELD_39(self):
        country_code = self.dataset.FIELD_39
        country_code = country_code.fillna("NAA")
        country_code = country_code.map(lambda x: x if (x == "NAA" or x == "VN") else "FoR")
        country_code = country_code.map(lambda x: x if x != "NAA" else np.nan)  
        
        self.dataset["FIELD_39"] = country_code

    def cl_FIELD_40(self):
        F40 = self.dataset.FIELD_40.replace(to_replace=["05 08 11 02"],value="02 05 08 11")
        F40 = F40.replace(to_replace = ["08 02","4"],value = np.nan)

        self.dataset["FIELD_40"] = F40

    def fit(self,dataset):
        self.dataset = dataset
    
    