import numpy as np
from scipy.integrate import simpson


def ExtractCycles(dfData, ContactForce, Latency=10e-3, CurrentTh=1e-3):
    # Calculate Contact Position
    dt = dfData.Time[dfData['Force'] > ContactForce].diff()
    StartInds = np.where(dt > Latency)[0]
    StartInds = np.hstack((0, StartInds))
    Indexs = dt.index.values
    StartIndexs = Indexs[StartInds]
    EndIndexs = Indexs[StartInds - 1][1:]
    EndIndexs = np.hstack((EndIndexs, Indexs[-1]))

    # Calculate Duration
    Duration = dfData.Time[EndIndexs].values - dfData.Time[StartIndexs].values
    nSampsCycle = EndIndexs - StartIndexs
    print('Cycles Duration')
    print(Duration)
    print('Cycles Samples')
    print(nSampsCycle)
    nSampsCycle = np.max(nSampsCycle)

    CyclesList = []
    for ic, st in enumerate(StartIndexs):
        ed = st + nSampsCycle
        data = dfData[st:ed].copy()
        data.reset_index(inplace=True, drop=True)
        data.loc[:, 'Time'] = data.Time.values - data.Time[0]
        # Calculate sign transition time
        IndHalf = data[data.Current > CurrentTh].index[-1]
        print(f'Time Transition {data.Time[IndHalf]} {IndHalf}')
        imax = data.Current.idxmax()
        imin = data.Current.idxmin()
        Cycle = {'Data': data,
                 'Cycle': ic,
                 'tStart': dfData.Time[st],
                 'PosStart': dfData.Position[st],
                 'tEnd': dfData.Time[ed],
                 'PosEnd': dfData.Position[ed],
                 'IMax': data.Current[imax],
                 'PosIMax': dfData.Position[imax],
                 'IMin': data.Current[imin],
                 'PosIMin': dfData.Position[imin],
                 'VMax': data.Voltage.max(),
                 'VMin': data.Voltage.min(),
                 'tTransition': data.Time[IndHalf],
                 'PosPMax': dfData.Power[:IndHalf].max(),
                 'NegPMax': dfData.Power[IndHalf:].max(),
                 'PosEnergy': simpson(y=data.Current[:IndHalf], x=data.Time[:IndHalf]),
                 'NegEnergy': simpson(y=data.Current[IndHalf:], x=data.Time[IndHalf:]),
                 }
        CyclesList.append(Cycle)

    return CyclesList