from math import ceil

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns



VarColors = {
    'Voltage': {'LineKwarg': {'color': 'r',
                              },
                # 'Limits': (-180, 180),
                'Label': 'Voltage [V]'
                },
    'Current': {'LineKwarg': {'color': 'b',
                              },
                # 'Limits': (-15, 15),
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
    'Force': {'LineKwarg': {'color': 'g',
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
                     # 'Limits': (-20, 20),
                     'Label': 'Acceleration [m/s^2]'
                     },
    'Velocity': {'LineKwarg': {'color': 'brown',
                               'linestyle': 'dashed',
                               'linewidth': 0.5,
                               },
                 # 'Limits': (-0.3, 0.3),
                 'Label': 'Velocity [m/s]'
                 },
    'Power': {'LineKwarg': {'color': 'purple',
                            },
              'Factor': 1e6,
              # 'Limits': (0, 1000),
              'Label': 'Power [uW]'},
}

def GenFigure(dfData, xVar='Time', PlotColumns=None, ax=None, axisFactor=0.2, **kwargs):
    """
    Generate a figure from the given data and plot the specified columns.

    Parameters:
    dfData (DataFrame): The input data to be plotted.
    xVar (str): The variable to be plotted on the x-axis. Default is 'Time'.
    PlotColumns (dict): A dictionary of columns to be plotted, with colors as values. If None, default colors from VarColors are used.
    ax (AxesSubplot): The subplot to draw the plot onto. If None, a new figure and subplot is created.
    axisFactor (float): The factor to adjust the position of additional y-axes. Default is 0.2.
    **kwargs: Additional keyword arguments to be passed to plt.subplots if ax is None.

    Returns:
    AxsDict (dict): A dictionary of plotted columns and their corresponding axes.
    PlotColumns (dict): The dictionary of columns to be plotted with their colors.
    """
    if PlotColumns is None:
        PlotColumns = VarColors

    if ax is None:
        fig, ax = plt.subplots(1, 1, **kwargs)

    axp = None
    AxsDict = {}
    ic = 0
    for var, prop in PlotColumns.items():
        if var == xVar:
            continue
        if var not in dfData.columns:
            continue

        if axp is None:
            axp = ax
        else:
            axp = plt.twinx(ax)
        if ic > 1:
            axp.spines.right.set_position(("axes", 1 + (axisFactor * (ic - 1))))
        ic += 1
        if 'Label' in prop:
            axp.set_ylabel(prop['Label'])
        else:
            axp.set_ylabel(var)

        color = prop['LineKwarg']['color']
        axp.yaxis.label.set_color(color)
        axp.tick_params(axis='y', colors=color)

        if 'Limits' in prop:
            axp.set_ylim(prop['Limits'][0], prop['Limits'][1])

        AxsDict[var] = axp

    return AxsDict, PlotColumns

xLogVars = ('Req', )
yLogVars = ('PosEnergy', 'NegEnergy', )

def PlotScalarValues(dfData, PlotPars, xVar, hueVar, PltFunt=sns.scatterplot):
    """
    Generate subplots for scalar values based on the provided data and plot parameters.

    Parameters:
    - dfData: the input data frame
    - PlotPars: list of parameters to be plotted
    - xVar: the variable for the x-axis
    - hueVar: the variable for coloring the plot
    - PltFunt: the plotting function to be used (default is sns.scatterplot)

    Returns:
    - fig: the generated figure
    - axs: array of subplot axes
    """

    # create subplots
    nRows = int(np.sqrt(len(PlotPars)))
    nCols = ceil(len(PlotPars) / nRows)
    fig, ax = plt.subplots(nRows, nCols, figsize=(10, 8))
    axs = ax.flatten()

    for ic, par in enumerate(PlotPars):
        ax = axs[ic]
        PltFunt(data=dfData,
                x=xVar,
                y=par,
                hue=hueVar,
                ax=ax
                )
        if xVar in xLogVars:
            ax.set_xscale('log')
        if par in yLogVars:
            ax.set_yscale('log')
    fig.tight_layout()
    return fig, axs
