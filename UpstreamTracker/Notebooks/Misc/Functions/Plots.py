#Make the change as the plot should be based on a variable parameter for the signal/pedestal, or such.

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc = {'figure.figsize':(15, 5)})

class overlappingPlots():
    def __init__(self,data1,data2,data3):
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
    def histogram(self):
        sns.histplot(self.data1['PedestalValue'],color='tab:red',alpha=0.5,bins=50)
        sns.histplot(self.data2['PedestalValue'],color='tab:blue',alpha=0.5,bins=50)
        sns.histplot(self.data3['PedestalValue'],color='tab:green',alpha=0.5,bins=50)
        plt.show()


    def correlation(self):
        corr_matrix1_2 = self.data1.select_dtypes(exclude='object').corrwith(self.data2.select_dtypes(exclude='object')).drop('ChannelID')
        corr_matrix1_3 = self.data1.select_dtypes(exclude='object').corrwith(self.data3.select_dtypes(exclude='object')).drop('ChannelID')
        corr_matrix2_3 = self.data2.select_dtypes(exclude='object').corrwith(self.data3.select_dtypes(exclude='object')).drop('ChannelID')

        sns.barplot(corr_matrix1_2,color='red',linewidth=2,edgecolor='r',label="Data1-2",alpha=0.2)
        sns.barplot(corr_matrix1_3,color='green',linewidth=2,edgecolor='g',label="Data1-3")
        sns.barplot(corr_matrix2_3,color='blue',linewidth=2,edgecolor='b',label="Data2-3",alpha=0.5)
        plt.legend()
        plt.show()


    def pedestal(self):
        self.data1['PedestalValue'].plot(kind='line')
        self.data2['PedestalValue'].plot(kind='line')
        self.data3['PedestalValue'].plot(kind='line')

class splitPlots:
    def __init__(self, data1, data2, data3):
        self.data1=data1
        self.data2=data2
        self.data3=data3

    def histogram(self):
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        sns.histplot(data=self.data1['PedestalValue'],color='tab:red',bins=25)
        plt.title(self.data1['RunNumber'].unique())

        plt.subplot(1, 3, 2)
        sns.histplot(data=self.data2['PedestalValue'],color='tab:blue',bins=25)
        plt.title(self.data2['RunNumber'].unique())

        plt.subplot(1, 3, 3)
        sns.histplot(data=self.data3['PedestalValue'],color='tab:green',bins=25)
        plt.title(self.data3['RunNumber'].unique())

        plt.tight_layout()
        plt.show()

    def boxplot(self):
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        sns.boxplot(data=self.data1['PedestalValue'],color='tab:red')
        plt.title(self.data1['RunNumber'].unique())

        plt.subplot(1, 3, 2)
        sns.boxplot(data=self.data2['PedestalValue'],color='tab:blue')
        plt.title(self.data2['RunNumber'].unique())

        plt.subplot(1, 3, 3)
        sns.boxplot(data=self.data3['PedestalValue'],color='tab:green')
        plt.title(self.data3['RunNumber'].unique())

        plt.tight_layout()
        plt.show()



import pandas as pd
def UTheatmap(data):
       plt.figure(figsize=(8, 6))
       data_=data[data['Plane']=="UTaX"][['Signal','PedestalValue',"Position","Module"]]
       data_['Position']=pd.to_numeric(data_['Position'])
       aggregated_data = data_.groupby(['Position','Module']).mean().reset_index()
       module_order=['M4T','S4T','S3T','M3T','S2T','S2WT', 'S2ET','M2T','S1T','S1WT','S1ET','M1T','M1WT','M1ET','M1B',
                        'M1WB', 'M1EB','S1B','S1WB', 'S1EB','M2B','S2B','S2WB', 'S2EB','M3B','S3B','S4B','M4B']
       
       aggregated_data['Module'] = pd.Categorical(aggregated_data['Module'], categories=module_order, ordered=True)
       aggregated_data_sorted = aggregated_data.sort_values(by=['Module','Position'])
       heatmap_data=aggregated_data_sorted.pivot(columns='Position', index='Module', values='PedestalValue')
       sns.heatmap(heatmap_data, cmap='PuBu', xticklabels=heatmap_data.columns, yticklabels=heatmap_data.index,linewidths=1)
       plt.xlabel('Stave')
       plt.ylabel('Y')
       plt.title('Pedestal Signals')
       plt.show()