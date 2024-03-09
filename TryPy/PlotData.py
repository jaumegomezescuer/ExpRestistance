from matplotlib import pyplot as plt

VarColors = {
    'Voltage': 'r',
    'Current': 'b',
    'Position': 'k',
    'Force': 'g',
    'Power': 'purple'}


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

