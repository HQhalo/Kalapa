from config import *
NO_NULL = 47
class PreProcessing:

    def drop_null_row(self):
        data_null = self.df.loc[np.sum(self.df.isnull(),axis=1) < 47]
        data_null_47 = self.df.loc[np.sum(self.df.isnull(),axis=1) == 47]
        data_null_48 = self.df.loc[np.sum(self.df.isnull(),axis=1) == 48]
        data_null_52 = self.df.loc[np.sum(self.df.isnull(),axis=1) == 52]
        
        data_null_47 = data_null_47.loc[data_null_47.iloc[:,1:-1].duplicated().map(lambda x: not x)]
        data_null_48 = data_null_48.loc[data_null_48.iloc[:,1:-1].duplicated().map(lambda x: not x)]
        data_null_52 = data_null_52.loc[data_null_52.iloc[:,1:-1].duplicated().map(lambda x: not x)]

        self.df = data_null.append(data_null_47).append(data_null_48).append(data_null_52)
    def combine_age(self,age1,age2):
        if abs(age1 - age2) <= 5:
            return int((age1+age2)/2)
        else:
            return -999
    def fillna(self):
        self.df = self.df.fillna(-999)
    def processing_age(self):
        age = []
        for a1,a2 in zip(self.df.age_source1,self.df.age_source2):
            age.append(self.combine_age(a1,a2))
        self.df = self.df.drop(["age_source1","age_source2"],axis = 1)
        
        self.df["age"] = age
        # list(pd.cut(age,bins= list(range(0,101,BIN_AGE)),labels=list(range(0,int(100/BIN_AGE)))) )
    def catagorical_fields(self):
        cat_cols = ["province","district","FIELD_8","FIELD_10","FIELD_11","FIELD_12","FIELD_13","FIELD_17","FIELD_24","FIELD_39",
        "FIELD_40","FIELD_41","FIELD_42","FIELD_44"]  
        
        

    def encode_bool(self):
        encode_cols = ["1","2","12","14","15","32","33","34","42","46"]
        
        
        
    def one_hot_encode(self):
        encode_cols = ["FIELD_8","FIELD_10"]  
    def processing_province(self):
        province = self.df.province.replace(to_replace = "Tỉnh Hoà Bình",value = "Tỉnh Hòa Bình")
        self.df["province"] = province.map(lambda x: str(x).lower()).where(province.notnull(),province)

    def processing_district(self):
        district = self.df.district
        self.df["district"] = district.map(lambda x: str(x).lower()).where(district.notnull(),district)
        
    def drop_maCv(self):
        self.df = self.df.drop("maCv",axis = 1)

    # def cutFIELD_3(self):
    #     F3_unique = self.df.FIELD_3.unique()
    #     F3_unique_sorted = np.sort(F3_unique)

    #     bins_F3 = []

    #     bins_F3+=[F3_unique_sorted[0]]

    #     for idx in range(1,len(F3_unique_sorted)):
    #         if F3_unique_sorted[idx] - F3_unique_sorted[idx -1] > 100:
    #             bins_F3 += [F3_unique_sorted[idx]]
        
    #     bins_F3 = np.array(bins_F3)
    #     bins_F3 -= 1

    #     self.df["FIELD_3"] = list(pd.cut(self.df.FIELD_3,bins= bins_F3,labels=list(range(0,len(bins_F3)-1))))
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
        
        HI_hight = [False for i in range(len(self.df))]
        HI_low = [False for i in range(len(self.df))]
        HI_normal = [False for i in range(len(self.df))]
        HI_none = [False for i in range(len(self.df))]

        idx = 0
        for i,j in zip(self.df.FIELD_7,self.df.FIELD_9):
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
        self.df = self.df.drop(["FIELD_7","FIELD_9"],axis = 1)
        self.df["HI_hight"] = HI_hight
        self.df["HI_low"] = HI_low
        self.df["HI_normal"] = HI_normal
        self.df["HI_none"] = HI_none
    

    def degree_FIELD_11(self):
        bins_degree = [-1,0,9,12,np.inf]
        label_degree = list(range(0,len(bins_degree)-1))
        degree_cut = np.array(pd.cut(self.df.FIELD_11,bins= bins_degree,labels= label_degree))
        for i in label_degree:
            self.df["degree_"+str(i)] = (degree_cut == i)
        self.df = self.df.drop("FIELD_11",axis = 1)
    
    def cl_FIELD_12(self):

        data_12 = self.df.FIELD_12
        data_12 = data_12.replace(to_replace=["0.0","0"],value=0)
        data_12 = data_12.replace(to_replace=["1.0","1"],value=1)
        data_12 = data_12.where((data_12== 1) | (data_12 == 0),np.nan )

        self.df["FIELD_12"] = data_12
  
    
    def cl_FIELD_43(self):
        self.df["FIELD_43"] = self.df["FIELD_43"].replace(to_replace = ["5","0"],value= np.nan)


    def country_FIELD_39(self):
        country_code = self.df.FIELD_39
        country_code = country_code.fillna("NAA")
        self.df["FIELD_39_VN"] = country_code == "VN"
        self.df["FIELD_39_FoR"] = (country_code != "VN") & (country_code != -999) & (country_code != "NAA") 
        
        self.df = self.df.drop("FIELD_39",axis = 1)
        
    def cl_FIELD_40(self):
        F40 = self.df.FIELD_40.replace(to_replace=["05 08 11 02"],value="02 05 08 11")
        F40 = F40.replace(to_replace = ["08 02","4"],value = np.nan)

        self.df["FIELD_40"] = F40

    def transform(self):
        if self.dropNa == True:
            self.drop_null_row()
        self.processing_age()       
        self.processing_province()
        self.processing_district()
        self.healthIsr_FIELD_7_9()
        self.drop_maCv()
        self.degree_FIELD_11()
        self.cl_FIELD_12()
        self.country_FIELD_39()
        self.cl_FIELD_40()
        self.cl_FIELD_43()
        self.fillna()
        
        
        return self.df

    def fit(self,df,dropNa = False):
        self.df = df.copy()
        self.dropNa = dropNa
    
    