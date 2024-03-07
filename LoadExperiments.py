import pandas as pd
import os

DataDir = './Data/'
ExpDef = './Data/Experiments.ods'
LoadsDef = './Data/LoadsDescription.ods'


dfExps = pd.read_excel(ExpDef)
dfLoads = pd.read_excel(LoadsDef)

#%% Add Loads Fields
LoadsFields = ('Req', 'Gain')
for lf in LoadsFields:
    dfExps.insert(1,lf, None)

for index, r in dfExps.iterrows():
    if r.RloadId in dfLoads.RloadId.values:
        for lf in LoadsFields:
            dfExps.loc[index, lf] = dfLoads.loc[dfLoads.RloadId == r.RloadId, lf].values

#%% load data files

# create abs path
# TODO check for repetion
for index, r in dfExps.iterrows():
    dfExps.loc[index, 'DaqFile'] = os.path.join(DataDir, r.DaqFile)
    dfExps.loc[index, 'MotorFile'] = os.path.join(DataDir, r.MotorFile)






