from math import ceil

import numpy as np
import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.integrate import simpson

plt.close('all')

from TryPy.PlotData import PlotScalarValues, GenFigure
# import imageio.v2 as imageio  # Importar la versión 2 de imageio para evitar el aviso de deprecación


# PDF = PdfPages('./Reports/DataSetsAnalysis.pdf')

# %% Load data

FileIn = './DataSets/Cycles-ExperimentsT1_0_T2_500CurvesR.pkl'
dfData = pd.read_pickle(FileIn)


# %% add new calculations example
for index, r in dfData.iterrows():
    cyData = r.Data
    dfData.loc[index, 'VoltageMax'] = cyData.Voltage.max()
    dfData.loc[index, 'VoltageMin'] = cyData.Voltage.min()
    dfData.loc[index, 'Energy'] = simpson(y=cyData.Power, x=cyData.Time)
    IndHalf = int(r.iTransition)
    dfData.loc[index, 'PositiveEnergy'] = simpson(y=cyData.Power[:IndHalf], x=cyData.Time[:IndHalf])
    dfData.loc[index, 'NegativeEnergy'] = simpson(y=cyData.Power[IndHalf:], x=cyData.Time[IndHalf:])


dfData.CurrentMax = dfData.CurrentMax * 1e6
dfData.CurrentMin = dfData.CurrentMin * 1e6



# %% Plot experiments comparison

# PlotPars = ('CurrentMax',
#             'CurrentMin',
#             'CurrentMaxPosition',
#             'CurrentMinPosition',)
#
# fig, axs = PlotScalarValues(dfData=dfData,
#                             PlotPars=PlotPars,
#                             xVar='Req',
#                             hueVar='Contact Time(ms)',
#                             PltFunt=sns.scatterplot)


# %% compare positive and negative peaks
# dSel = dfData
# fig, ax = plt.subplots()
# sns.lineplot(data=dSel,
#              x='Req',
#              y='PositiveEnergy',
#              ax=ax,
#              #hue='Contact Time(ms)',
#              label='PositiveEnergy')
# sns.lineplot(data=dSel,
#              x='Req',
#              y='NegativeEnergy',
#              ax=ax,
#              #hue='Contact Time(ms)',
#              label='NegativeEnergy')
# sns.lineplot(data=dSel,
#              x='Req',
#              y='Energy',
#              ax=ax,
#              #hue='Contact Time(ms)',
#              label='Energy')
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel('Load Resistance (Ohm)')
# ax.set_ylabel('Energy per cycle (J)')
# ax.legend()
# PDF.savefig(fig)



##########################################################################################
# Gráfica para Energia en función de T1 Y T2
# Obtener los nombres de los diferentes valores de ExpId
# Configurar el gráfico
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Contact Time Effect',
             fontsize=25)
# Trazar los puntos para Contact time en funcion de los req y la energia
sns.scatterplot(data=dfData, x='Req', y='Energy', ax=ax, hue='Contact Time(ms)')
ax.set_xscale('log')
ax.set_yscale('log')

ax.set_ylabel('Energy per cycle (J)',
              fontsize=25)
ax.set_xlabel('Load Resistance (Ohm)',
                fontsize=25)
ax.tick_params(axis='both', which='major', labelsize=20)
plt.setp(ax.get_legend().get_texts(), fontsize='18') # for legend text
plt.setp(ax.get_legend().get_title(), fontsize='18') # for legend title

plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para una mejor legibilidad
plt.tight_layout()
fig.savefig('images/ContactTimeEffectEnergy.png', dpi=600)
# PDF.savefig(fig)
##########################################################################################

fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Contact Time Effect',
             fontsize=25)
# Trazar los puntos para Contact time en funcion de los req y la energia
sns.scatterplot(data=dfData, x='Req', y='CurrentMax', ax=ax, hue='Contact Time(ms)')
ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_ylabel('Maximum Current (uA)',
              fontsize=25)
ax.set_xlabel('Load Resistance (Ohm)',
              fontsize=25)
ax.tick_params(axis='both', which='major', labelsize=20)
plt.setp(ax.get_legend().get_texts(), fontsize='18') # for legend text
plt.setp(ax.get_legend().get_title(), fontsize='18') # for legend title

# ax.legend()

plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para una mejor legibilidad
plt.tight_layout()
fig.savefig('images/ContactTimeEffectImax.png', dpi=600)
# PDF.savefig(fig)

##########################################################################################

fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Contact Time Effect',
             fontsize=25)
# Trazar los puntos para Contact time en funcion de los req y la energia
sns.scatterplot(data=dfData, x='Req', y='CurrentMin', ax=ax, hue='Contact Time(ms)')
ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_ylabel('Minimum Current (uA)',
              fontsize=25)
ax.set_xlabel('Load Resistance (Ohm)',
              fontsize=25)
ax.tick_params(axis='both', which='major', labelsize=20)
plt.setp(ax.get_legend().get_texts(), fontsize='18') # for legend text
plt.setp(ax.get_legend().get_title(), fontsize='18') # for legend title

plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para una mejor legibilidad
plt.tight_layout()
fig.savefig('images/ContactTimeEffectImin.png', dpi=600)
# PDF.savefig(fig)

# Crear el directorio "images" si no existe
# if not os.path.exists('images'):
#     os.makedirs('images')
# %% Plot experiment time traces
#
VarColors = {
    'Voltage': {'LineKwarg': {'color': 'r',
                              },
                'Limits': (-200, 180),
                'Label': 'Voltage [V]'
                },
    'Current': {'LineKwarg': {'color': 'b',
                              },
                'Limits': (-15, 15),
                'Factor': 1e6,
                'Label': 'Current [uA]'
                },
    'Position': {'LineKwarg': {'color': 'k',
                               'linestyle': 'dashed',
                               'linewidth': 0.5,
                               },
                 # 'Limits': (-5, 5),
                 'Label': 'Position [mm]'
                 },
}
""" 'Force': {'LineKwarg': {'color': 'g',
                            'linestyle': 'dashed',
                            'linewidth': 0.5,
                            },
              # 'Limits': (-5, 5),
              'Label': 'Force [N]'
              },
    'Acceleration': {'LineKwarg': {'color': 'orange',
                                   'linestyle': 'dashed',
                                   'linewidth': 0.5,
                                   },
                     'Limits': (-20, 20),
                     'Label': 'Acceleration [m/s^2]'
                     },
    'Velocity': {'LineKwarg': {'color': 'brown',
                               'linestyle': 'dashed',
                               'linewidth': 0.5,
                               },
                 'Limits': (-0.3, 0.3),
                 'Label': 'Velocity [m/s]'
                 },
    'Power': {'LineKwarg': {'color': 'purple',
                            },
              'Factor': 1e6,
              'Limits': (0, 1000),
              'Label': 'Power [uW]'},'

"""



dSel = dfData
#dSel = dfData.query("TribuId == 'SwTENG-RF2' ")

for ex, dExp in dSel.groupby('ExpId'):
    fig, (axtime, axpos) = plt.subplots(2, 1, figsize=(11, 7))
    for gn, df in dExp.groupby('RloadId'):
        # plot time traces
        AxsDict, _ = GenFigure(dfData=df.iloc[0].Data,
                               xVar='Time',
                               PlotColumns=VarColors,
                               axisFactor=0.15,
                               ax=axtime)
        for index, r in df.iterrows():
            Data = r.Data
            for var, ax in AxsDict.items():
                if 'Factor' in VarColors[var]:
                    ptdata = Data[var] * VarColors[var]['Factor']
                else:
                    ptdata = Data[var]
                ax.plot(Data['Time'], ptdata, **VarColors[var]['LineKwarg'])
                ax.axvline(x=r.tTransition, color='y')

        AxsDict['Voltage'].set_xlabel('Time (s)', fontsize=20)
        AxsDict['Voltage'].tick_params(axis='both', which='major', labelsize=18)
        for n, ax in AxsDict.items():
            plt.setp(ax.get_yaxis().get_label(), fontsize=20)
            plt.setp(ax.get_yaxis().get_ticklabels(), fontsize=18)



        # plot position traces
        AxsDict, _ = GenFigure(dfData=df.iloc[0].Data,
                               xVar='Position',
                               PlotColumns=VarColors,
                               axisFactor=0.15,
                               ax=axpos)
        AxsDict['Voltage'].set_xlabel('Position (mm)', fontsize=20)
        AxsDict['Voltage'].tick_params(axis='both', which='major', labelsize=18)
        for n, ax in AxsDict.items():
            plt.setp(ax.get_yaxis().get_label(), fontsize=20)
            plt.setp(ax.get_yaxis().get_ticklabels(), fontsize=18)




        for index, r in df.iterrows():
            Data = r.Data
            for var, ax in AxsDict.items():
                if 'Factor' in VarColors[var]:
                    ptdata = Data[var] * VarColors[var]['Factor']
                else:
                    ptdata = Data[var]
                ax.plot(Data['Position'], ptdata, **VarColors[var]['LineKwarg'])
            ax.set_xlabel('Position')
            ax.set_xlim(0, 2)

        fig.suptitle(f'Experiment: {r.ExpId}, Tribu: {r.TribuId}, Rload: {r.RloadId}, Req: {r.Req}')
        fig.tight_layout()
        plt.close(fig)
   # Guardar la figura como una imagen en la carpeta "images"
        image_file = f'./images/Experiment_{ex}_Rload_{gn}.png'
        fig.savefig(image_file, dpi=600)



# # Crear animación con las imágenes
# animation_file = 'animation.gif'
# with imageio.get_writer(animation_file, mode='I', fps=2) as writer:
#     for image_file in image_files:
#         image = imageio.imread(image_file)
#         writer.append_data(image)
#
# print(f'Animation saved as {animation_file}')




# #Imagen comparativa rGO solo y resistencia 10 k sola
# sns.lineplot(x='Time', y='Voltage', data=dfData.Data, ax=ax, hue='ExpLabel')
#
# ax.set_ylabel('Voltage (V)')
# ax.set_xlabel('Time (s)')
#
#
# PDF.close()
