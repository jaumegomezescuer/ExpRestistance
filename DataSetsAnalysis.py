from math import ceil

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

VarColors = {
    'Voltage': 'r',
    'Current': 'b',
    'Position': 'k',
    'Force': 'g',
    'Power': 'purple'}

FileIn = './DataSets/Cycles.pkl'
dfData = pd.read_pickle(FileIn)

PlotPars = ('IMax',
            'PosIMax',
            'IMin',
            'PosIMin',
            'VMax',
            'VMin',
            'PosPMax',
            'NegPMax',
            'PosEnergy',
            'NegEnergy',)

nRows = int(np.sqrt(len(PlotPars)))
nCols = ceil(len(PlotPars) / nRows)
fig, ax = plt.subplots(nRows, nCols, figsize=(10, 8))
axs = ax.flatten()

for ic, par in enumerate(PlotPars):
    ax = axs[ic]
    sns.boxplot(data=dfData,
                  x='Req',
                  y=par,
                  hue='TribuId',
                  ax=ax
                  )
    ax.set_xscale('log')
fig.tight_layout()
