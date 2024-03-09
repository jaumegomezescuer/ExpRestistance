import numpy as np
from scipy.integrate import simpson


def ExtractCycles(dfData, ContactPosition=8, ContactForce=None, Latency=10e-3, CurrentTh=1e-3):
    """
    Extracts cycles from dfData based on ContactForce and Latency, and calculates various parameters for each cycle.

    Parameters:
    - dfData: DataFrame, the input data
    - ContactForce: float, the threshold force for contact
    - Latency: float, the time delay for identifying the start and end of cycles (default=10e-3)
    - CurrentTh: float, the threshold current for identifying transition time (default=1e-3)

    Returns:
    - CyclesList: list, a list of dictionaries containing information about each cycle
    """

    # Calculate Contact Position
    if ContactPosition is not None:
        dt = dfData.Time[dfData['Position'] < ContactPosition].diff()
        StartInds = np.where(dt > Latency)[0]
        StartInds = np.hstack((0, StartInds))
        Indexs = dt.index.values
        StartIndexs = Indexs[StartInds]
        EndIndexs = Indexs[StartInds - 1][1:]
        EndIndexs = np.hstack((EndIndexs, Indexs[-1]))
    elif ContactForce is not None:
        dt = dfData.Time[dfData['Force'] > ContactForce].diff()
        StartInds = np.where(dt > Latency)[0]
        StartInds = np.hstack((0, StartInds))
        Indexs = dt.index.values
        StartIndexs = Indexs[StartInds]
        EndIndexs = Indexs[StartInds - 1][1:]
        EndIndexs = np.hstack((EndIndexs, Indexs[-1]))
    else:
        print('Please specify ContactForce or ContactPosition')
        return None

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
        if ed > dfData.shape[0]:
            ed = dfData.shape[0]-1
        data = dfData[st:ed].copy()
        data.reset_index(inplace=True, drop=True)
        data.loc[:, 'Time'] = data.Time.values - data.Time[0]
        # Calculate sign transition time
        hindexes = data[data.Current > CurrentTh].index
        if len(hindexes) == 0:
            print('No Current Threshold crossed')
            IndHalf = int(data.shape[0] / 2)
        else:
            IndHalf = hindexes[-1]
        print(f'Time Transition {data.Time[IndHalf]} {IndHalf}')
        imax = data.Current.idxmax()
        imin = data.Current.idxmin()
        Cycle = {'Data': data,  # Dataframe with recorded data
                 'Cycle': ic,  # Cycle number
                 'tStart': dfData.Time[st],  # Cycle Start time
                 'PosStart': dfData.Position[st],  # Cycle Start position
                 'tEnd': dfData.Time[ed],  # Cycle End time
                 'PosEnd': dfData.Position[ed],  # Cycle End position
                 'IMax': data.Current[imax],  # Max current
                 'PosIMax': dfData.Position[imax],  # Position of max current
                 'IMin': data.Current[imin],  # Min current
                 'PosIMin': dfData.Position[imin],  # Position of min current
                 'VMax': data.Voltage.max(),  # Max voltage
                 'VMin': data.Voltage.min(),  # Min voltage
                 'tTransition': data.Time[IndHalf],  # Transition time between positive and negative current
                 'PosPMax': dfData.Power[:IndHalf].max(),  # Max positive power
                 'NegPMax': dfData.Power[IndHalf:].max(),  # Max negative power
                 'PosEnergy': simpson(y=data.Power[:IndHalf], x=data.Time[:IndHalf]),  # Positive energy
                 'NegEnergy': simpson(y=data.Power[IndHalf:], x=data.Time[IndHalf:]),  # Negative energy
                 }
        CyclesList.append(Cycle)

    return CyclesList
