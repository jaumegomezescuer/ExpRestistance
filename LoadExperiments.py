import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_pdf import PdfPages

from TryPy.PlotData import GenFigure

MotColumnRenames = {
    'Time(s)': 'Time',
    'MC SW Overview - Actual Position(mm)': 'Position',
    'MC SW Force Control - Measured Force(N)': 'Force',
}

DQAColumnRenames = {
    'Input 0': 'Voltage',
    'Unnamed: 1': 'Time',
}

mpl.use("Qt5Agg")

DataDir = './Data/'
ExpDef = './Data/Experiments.ods'
LoadsDef = './Data/LoadsDescription.ods'

PDF = PdfPages('LoadReport.pdf')

dfExps = pd.read_excel(ExpDef)
dfLoads = pd.read_excel(LoadsDef)

# %% Add Loads Fields
LoadsFields = ('Req', 'Gain')
for lf in LoadsFields:
    dfExps.insert(1, lf, None)

for index, r in dfExps.iterrows():
    if r.RloadId in dfLoads.RloadId.values:
        for lf in LoadsFields:
            dfExps.loc[index, lf] = dfLoads.loc[dfLoads.RloadId == r.RloadId, lf].values

# %% load data files

# create abs path
for index, r in dfExps.iterrows():
    dfExps.loc[index, 'DaqFile'] = os.path.join(DataDir, r.DaqFile)
    dfExps.loc[index, 'MotorFile'] = os.path.join(DataDir, r.MotorFile)

plt.ioff()
for index, r in dfExps.iterrows():
    if not os.path.isfile(r.DaqFile):
        print(f'File {r.DaqFile} not found')
    if not os.path.isfile(r.MotorFile):
        print(f'File {r.MotorFile} not found')

    daqf = pd.ExcelFile(r.DaqFile)
    sheets = daqf.sheet_names
    dfDAQ = pd.read_excel(r.DaqFile,
                          sheet_name=sheets[1])

    # rename columns
    dfDAQ = dfDAQ.rename(columns=DQAColumnRenames)

    dfMOT = pd.read_csv(r.MotorFile,
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
        if col is 'Time':
            continue

        dfData[col] = np.interp(dfData.Time, dfMOT.Time, dfMOT[col])

    # Calculate Voltage, Current and Power
    dfData['VoltageAcq'] = dfData.Voltage
    dfData['Voltage'] = dfData.VoltageAcq / r.Gain
    dfData['Current'] = dfData.Voltage / r.Req
    dfData['Power'] = dfData.Current * dfData.Voltage

    # Calculate Contact Position
    ContactForce = -5
    dt = dfData.Time[dfData['Force'] < ContactForce].diff()
    CycleInds = dt[dt > 5e-4].index
    ContactPos = dfData.Position[CycleInds].mean()
    MaxPos = dfData.Position.max()
    MinPos = dfData.Position.min()

    XVar = 'Time'
    AxsDict, PlotCols = GenFigure(dfData, xVar=XVar, figsize=(12, 5))
    for col, ax in AxsDict.items():
        ax.set_xlabel(XVar)
        ax.plot(dfData[XVar], dfData[col], PlotCols[col])
    fig = ax.get_figure()
    fig.suptitle(r.ExpId)
    fig.tight_layout()
    PDF.savefig(fig)

    XVar = 'Position'
    AxsDict, PlotCols = GenFigure(dfData, xVar=XVar, figsize=(10, 5))
    for col, ax in AxsDict.items():
        ax.set_xlabel(XVar)
        ax.set_xlim(MinPos, ContactPos)
        ax.plot(dfData[XVar], dfData[col], PlotCols[col])
    fig = ax.get_figure()
    fig.suptitle(r.ExpId)
    fig.tight_layout()
    PDF.savefig(fig)

    plt.close('all')

plt.ion()
PDF.close()
