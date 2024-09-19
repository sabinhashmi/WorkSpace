import pandas as pd

#Importing Pickles
translator_=pd.read_pickle('/Users/sabinhashmi/Drive/Projects/Upstream Tracker Calibration/UTCalibrationMaterials/translator.pkl')
map_ = pd.read_pickle('/Users/sabinhashmi/Drive/Projects/Upstream Tracker Calibration/UTCalibrationMaterials/universal_map.pkl')

#Translator - Pickle to DataFrames
data_dict=pd.read_pickle('/Users/sabinhashmi/Drive/Projects/Upstream Tracker Calibration/UTCalibrationMaterials/translator.pkl')
translator_=pd.DataFrame.from_dict(data_dict,orient='index').reset_index()
translator_.columns=['ChannelID','ChipID']


#UniversalMapping - Pickeles to DataFrame
data_dict=pd.read_pickle('/Users/sabinhashmi/Drive/Projects/Upstream Tracker Calibration/UTCalibrationMaterials/universal_map.pkl')
universal_map_=pd.DataFrame.from_dict(data_dict,orient='index').reset_index()[['index','sensor_type']]
universal_map_.columns=['ChipID','SensorType']
universal_map_[['Sector','ChipID']]=universal_map_['ChipID'].str.rsplit('.',n=1,expand=True)
# universal_map_


class dataProd():
    def __init__(self):
        pass
    
    
    def singleRun(self,file):
        cms=pd.read_csv(r'/Users/sabinhashmi/Drive/Projects/Upstream Tracker Calibration/UTData/UTData3/CMS_noise_0000{}.csv'.format(file),names=['ChannelID','Signal','CMSubstracted','Int']).drop(['Int'],axis=1)
        cm=pd.read_csv(r'/Users/sabinhashmi/Drive/Projects/Upstream Tracker Calibration/UTData/UTData3/commonMode_0000{}.csv'.format(file),names=['ChipID','ChipMean','ChipSigma','Int']).drop(['Int'],axis=1)
        pedastals=pd.read_csv(r'/Users/sabinhashmi/Drive/Projects/Upstream Tracker Calibration/UTData/UTData3/pedestals_0000{}.csv'.format(file),names=['ChannelID','PedestalValue','Int']).drop(['Int'],axis=1)
        


        data_=cms.merge(translator_,how='right')
        data_[['Sector','ChipID','ChannelNumber']]=data_['ChipID'].str.split('.',expand=True)


        cm[['Sector','ChipID']]=cm['ChipID'].str.rsplit('_', n=1, expand=True)
        cm['ChipID']=cm['ChipID'].map({'0':'Chip0','1':'Chip1','2':'Chip2','3':'Chip3'})
        data_=data_.merge(cm,on=['Sector','ChipID'],how='left').merge(pedastals,on='ChannelID',how='left')
        data_=data_.merge(universal_map_)
        data_['RunNumber']=file
        data_[['Plane','Y','Stave']]=data_['Sector'].str.split('_',expand=True)
        data_[["Position","Side","T/B"]]=data_['Y'].str.split('',expand=True)[[1,2,3]]

        data_['Module']=data_["Stave"]+data_['T/B']
        #final data
        data_=data_[['ChannelID', 'PedestalValue','Signal', 'CMSubstracted', 'ChipID','ChannelNumber', 'ChipMean', 'ChipSigma', 
                     'RunNumber', 'Plane','Position', 'Side','Module']]
        
        data_['ChipID']=pd.to_numeric(data_['ChipID'].str.replace('Chip',''))
        data_['ChannelNumber']=pd.to_numeric(data_['ChannelNumber'].str.replace('Ch',''))
        data_['Position']=pd.to_numeric(data_['Position'])

        return data_
    
    def multipleRun(self, *runNumber):
        data = [self.singleRun(file) for file in runNumber]
        return pd.concat(data,axis=1,keys=runNumber)