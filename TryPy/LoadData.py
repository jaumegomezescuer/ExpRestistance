import os

import numpy as np
import pandas as pd
from nptdms import TdmsFile

MotColumnRenames = {
    'Time(s)': 'Time',
    'MC SW Overview - Actual Position(mm)': 'Position',
    'MC SW Force Control - Measured Force(N)': 'Force',
}

DQAColumnRenames = {
    'Input 0': 'Voltage',
    'Unnamed: 1': 'Time',
}


def LoadMotorFile(MotorFile):
    dfMOT = pd.read_csv(MotorFile,
                        header=0,
                        index_col=False,
                        delimiter=',',
                        decimal='.')
    # drop Non-defined columns
    dropcols = []
    for col in dfMOT.columns:
        if col not in MotColumnRenames.keys():
            dropcols.append(col)
    dfMOT = dfMOT.drop(columns=dropcols)
    # rename columns
    dfMOT = dfMOT.rename(columns=MotColumnRenames)
    return dfMOT


def LoadDAQFile(DaqFile):
    if DaqFile.endswith('.tdms'):
        tdms_file = TdmsFile.read(DaqFile)
        dfDAQ = tdms_file.as_dataframe(time_index=True,
                                       scaled_data=False)
        dfDAQ.reset_index(inplace=True)
        dfDAQ = dfDAQ.set_axis(['Time', 'Voltage'], axis=1)
        return dfDAQ
    elif DaqFile.endswith('.xlsx'):
        daqf = pd.ExcelFile(DaqFile)
        sheets = daqf.sheet_names
        dfDAQ = pd.read_excel(DaqFile,
                              sheet_name=sheets[1])
        # rename columns
        dfDAQ = dfDAQ.rename(columns=DQAColumnRenames)
        return dfDAQ
    else:
        print(f'File {DaqFile} not recognized')
        return None


def Loadfiles(ExpDef):
    r = ExpDef

    if not os.path.isfile(r.DaqFile):
        print(f'File {r.DaqFile} not found')
        return None
    if not os.path.isfile(r.MotorFile):
        print(f'File {r.MotorFile} not found')
        return None

        # Load DAQ file
    dfDAQ = LoadDAQFile(r.DaqFile)

    # Load Motor file
    dfMOT = LoadMotorFile(r.MotorFile)

    # Motor sampling Rate
    MotFs = 1 / dfMOT.Time.diff().mean()
    print(f'Motor sampling rate: {MotFs}')

    # DAQ sampling rate
    if 'Time' in dfDAQ.columns:
        DaqFs = 1 / dfDAQ.Time.diff().mean()
        print(f'Found DAQ sampling rate: {DaqFs}')
    else:
        nSamps = dfDAQ.Voltage.size
        DaqFs = nSamps / (1 / MotFs * dfMOT.Time.size)
        print(f'Calculated DAQ sampling rate: {DaqFs}')
        dfDAQ['Time'] = np.arange(0, nSamps) / DaqFs

    # Create interpolated data
    dfData = dfDAQ
    for col in dfMOT.columns:
        if col == 'Time':
            continue
        dfData[col] = np.interp(dfData.Time, dfMOT.Time, dfMOT[col])

    # Calculate Voltage, Current and Power
    dfData['VoltageAcq'] = dfData.Voltage
    dfData['Voltage'] = dfData.VoltageAcq / r.Gain
    dfData['Current'] = dfData.Voltage / r.Req
    dfData['Power'] = dfData.Current * dfData.Voltage

    return dfData
