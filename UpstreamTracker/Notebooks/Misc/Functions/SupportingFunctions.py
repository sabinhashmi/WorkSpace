#outlier counter
def outlierCounter(data):
    q1=data['PedestalValue'].quantile(0.25)
    q3=data['PedestalValue'].quantile(0.75)
    iqr=q3-q1
    lw_=q1-(1.5*iqr)
    uw_=q1+(1.5*iqr)
    outliers=data[(data['PedestalValue']<lw_) | (data['PedestalValue']>uw_)]
    print(f"Run Number : ",data['RunNumber'].unique()[0])
    print(f"Total Number of Outliers :",outliers.shape[0])
    print(f"Ratio of Outliers :",round(outliers.shape[0]/data.shape[0]*100,2),"%")
