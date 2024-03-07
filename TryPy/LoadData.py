import pandas as pd


def LoadData(DaqFile, MotorFile):
    daqf = pd.ExcelFile(DaqFile)
    sheets = daqf.sheet_names
    dfDAQ = pd.read_excel(DaqFile,
                          names=['Current', 'Time'],
                          sheet_name=sheets[1])

    dfMOT = pd.read_csv(MotorFile,
                        names=['Time', 'Voltage', 'Force', 'Current', 'Position'],
                        header=0,
                        index_col=False,
                        delimiter=',',
                        decimal='.')

    # Create interpolated data
    for col in ('Position', 'Force'):
        dfDAQ[col] = np.interp(dfDAQ.Time, dfMOT.Time, dfMOT[col])

    return dfDAQ