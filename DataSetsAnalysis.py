from math import ceil

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from TryPy.PlotData import PlotScalarValues, GenFigure

PDF = PdfPages('./Reports/DataSetsAnalysis.pdf')

# %% Load data

FileIn = './DataSets/Cycles.pkl'
dfData = pd.read_pickle(FileIn)

# %% Plot experiments comparison

PlotPars = ('IMax',
            'VMax',
            'PosPMax',
            'PosEnergy',)

fig, axs = PlotScalarValues(dfData=dfData,
                            PlotPars=PlotPars,
                            xVar='Req',
                            hueVar='TribuId',
                            PltFunt=sns.scatterplot)
fig.suptitle('Tribu Comparison')
fig.tight_layout()
PDF.savefig(fig)

PlotPars = ('IMax',
            'PosIMax',
            'VMax',
            'PosPMax',
            'PosEnergy')
fig, axs = PlotScalarValues(dfData=dfData.query("TribuId == 'SwTENG'"),
                            PlotPars=PlotPars,
                            xVar='Req',
                            hueVar='Cycle',
                            PltFunt=sns.scatterplot)
fig.suptitle('Positive peak Data')
fig.tight_layout()
PDF.savefig(fig)

PlotPars = ('IMin',
            'PosIMin',
            'VMin',
            'NegPMax',
            'NegEnergy')

fig, axs = PlotScalarValues(dfData=dfData.query("TribuId == 'SwTENG'"),
                            PlotPars=PlotPars,
                            xVar='Req',
                            hueVar='Cycle',
                            PltFunt=sns.scatterplot)
fig.suptitle('Negative peak Data')
fig.tight_layout()
PDF.savefig(fig)

# %% compare positive and negative peaks

dSel = dfData.query("TribuId == 'SwTENG' ")
fig, ax = plt.subplots()
sns.lineplot(data=dSel,
             x='Req',
             y='PosEnergy',
             ax=ax,
             label='PosEnergy')
sns.lineplot(data=dSel,
             x='Req',
             y='NegEnergy',
             ax=ax,
             label='NegEnergy')
sns.lineplot(data=dSel,
             x='Req',
             y='Energy',
             ax=ax,
             label='Energy')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Load Resistance (Ohm)')
ax.set_ylabel('Energy (J)')
ax.legend()
PDF.savefig(fig)

# %% Plot experiment time traces

VarColors = {
    'Voltage': 'r',
    'Current': 'b',
    'Position': 'k',
    'Force': 'g',
    'Power': 'purple'}

dSel = dfData
# dSel = dfData.query("TribuId == 'SwTENG' ")

for ex, dExp in dSel.groupby('ExpId'):
    fig, (axtime, axpos) = plt.subplots(2, 1, figsize=(11, 7))
    for gn, df in dExp.groupby('RloadId'):
        # plot time traces
        AxsDict, _ = GenFigure(dfData=df.loc[0, 'Data'],
                               xVar='Time',
                               PlotColumns=VarColors,
                               axisFactor=0.15,
                               ax=axtime)
        for index, r in df.iterrows():
            Data = r.Data
            for col, ax in AxsDict.items():
                ax.plot(Data['Time'], Data[col], color=VarColors[col],
                        alpha=0.5)
                ax.axvline(x=r.tTransition, color='y')
                ax.set_xlabel('Time')

        # plot position traces
        AxsDict, _ = GenFigure(dfData=df.loc[0, 'Data'],
                               xVar='Position',
                               PlotColumns=VarColors,
                               axisFactor=0.15,
                               ax=axpos)
        for index, r in df.iterrows():
            Data = r.Data
            for col, ax in AxsDict.items():
                ax.plot(Data['Position'], Data[col], color=VarColors[col],
                        alpha=0.5)
                ax.set_xlabel('Position')
                ax.set_xlim(0, 2)

        fig.suptitle(f'Experiment: {r.ExpId}, Tribu: {r.TribuId}, Rload: {r.RloadId}, Req: {r.Req}')
        fig.tight_layout()
        PDF.savefig(fig)
        plt.close(fig)

PDF.close()
