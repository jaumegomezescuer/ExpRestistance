from matplotlib import pyplot as plt

VarColors = {
    'Voltage': 'r',
    'Current': 'b',
    'Position': 'k',
    'Force': 'g',
    'Power': 'purple'}


def GenFigure(dfData, xVar='Time', PlotColumns=None, ax=None, axisFactor=0.2, **kwargs):
    if PlotColumns is None:
        PlotColumns = VarColors

    if ax is None:
        fig, ax = plt.subplots(1, 1, **kwargs)

    axp = None
    AxsDict = {}
    ic = 0
    for col, color in PlotColumns.items():
        if col == xVar:
            continue
        if col not in dfData.columns:
            continue

        if axp is None:
            axp = ax
        else:
            axp = plt.twinx(ax)
        if ic > 1:
            axp.spines.right.set_position(("axes", 1 + (axisFactor * (ic - 1))))
        ic += 1
        axp.set_ylabel(col)
        axp.yaxis.label.set_color(color)
        axp.tick_params(axis='y', colors=color)
        AxsDict[col] = axp

    return AxsDict, PlotColumns

