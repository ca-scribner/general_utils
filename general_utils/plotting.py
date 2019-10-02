import numpy as np
import itertools
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Rectangle

from sklearn.metrics import confusion_matrix

from general_utils.pandas import get_zero_axes

NOT_SPECIFIED = 'NOT_SPECIFIED'


def cmap_to_discrete(cmap, vmin=0., vmax=1., bin_increment=0.1, increments=None, increment_limit=21):
    """
    Discretize a Matplotlib Colormap, returning a map that has discrete colors in bin_increment increments

    Args:
        cmap:
        vmin:
        vmax:
        bin_increment (float): Increment separating each bin (will be ignored if bins is not None)
        increments (int): Number of bins to use to segment cmap.  If set, will override bin_increment

    Returns:
        Dict of:
            cmap: mpl discrete colormap
            norm: mpl.colors.BoundaryNorm object
            sm: ScalarMappable of colormap (what fig.colorbar() uses)
    """
    # Define a discrete colormap based on a predefined one
    # (inspired by SO post: "Matplotlib Discrete Colorbar")
    if isinstance(cmap, str):
        # CMAP specified by string name.  Load actual CMAP
        cmap = plt.get_cmap(cmap)

    cmap_colors = [cmap(i) for i in range(cmap.N)]

    # Force bottom color to be different (so we know if something drops off the bottom)
    # cmap_colors[0] = (0.05, 0.05, 0.05, 1.0)

    cmap = mpl.colors.LinearSegmentedColormap.from_list('Discrete CMAP', cmap_colors, len(cmap_colors))

    if increment_limit is not None and increment_limit is not False:
        if increments > increment_limit or (vmax+bin_increment - vmin) / bin_increment > increment_limit:
            print(f"Warning: Too many bins detected.  Limiting number of increments to {increment_limit}")
            increments = increment_limit

    if increments is not None:
        bins = np.linspace(vmin, vmax, increments)
    else:
        # Round up the vmax so it is included
        bins = np.arange(vmin, vmax + bin_increment / 2, bin_increment)

    norm = mpl.colors.BoundaryNorm(bins, len(cmap_colors))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    return {'cmap': cmap, 'norm': norm, 'sm': sm}


def heatmap(data, xticklabels, yticklabels, xlabel="", ylabel="", textcolor="red", fontsize=None,
            cmap='Greys', number_fmt='.2f', fontweight_max='bold', fontweight_min='normal', ax=None, savefig=False):
    """
    Return a basic labelled heatmap of the numberic data, with data[0,0] placed in the upper left

    :param data: Numpy array of data to plot
    :param xticklabels (yticklabels): Labels corresponding to row (column) element of data
    :param textcolor: color designation passed to ax.text()
    :param fontsize: fontsize parameter passed to ax.text()
    :param fontweight_max: fontweight parameter passed to ax.text() for the maximum element in data (to
                           highlight the max cell in the heatmap set to 'bold' or 'heavy')
    :param fontweight_min: fontweight parameter passed to ax.text() for the minimum element in data (to
                           highlight the min cell in the heatmap set to 'bold' or 'heavy')
    :param fontsize: fontsize parameter passed to ax.text()
    :param cmap: cmap designation passed to imshow()
    :param number_fmt: Format string for the numbers printed in the heatmap
    :param savefig: If not False, save the figure generated here to savefig

    :return: tuple of (matplotlib figure, matplotlib axes)
    """
    print("WARNING: USING LOCAL VERSION OF PLOTTING SCRIPTS - SWITCH TO (GENERAL_UTILS.PLOTTING)")
    # Labels need to be padded by 1 element, as imshow will plot data starting centered at tick (1,1) but the
    # set_xticklabels/set_yticklabels sets labels starting at tick 0
    try:
        xticklabels = ("",) + tuple([f'{x:{number_fmt}}' for x in xticklabels])
    except TypeError:
        # Failsafe if number_fmt doesn't match the labels (eg if labels are tuples)
        xticklabels = ("",) + tuple([str(x) for x in xticklabels])
    try:
        yticklabels = ("",) + tuple([f'{x:{number_fmt}}' for x in yticklabels])
    except TypeError:
        # Failsafe if number_fmt doesn't match the labels (eg if labels are tuples)
        yticklabels = ("",) + tuple([str(x) for x in yticklabels])

    fig, ax = get_fig_ax(ax=ax)

    # Set fontweight dict to help with formatting
    fontweight = np.chararray(data.shape, itemsize=20, unicode=True)
    fontweight[:] = 'normal'
    # Set weight for max/min cells for highlighting
    fontweight[np.unravel_index(data.argmax(), data.shape)] = fontweight_max
    fontweight[np.unravel_index(data.argmin(), data.shape)] = fontweight_min

    for i, j in itertools.product(range(data.shape[0]), range(data.shape[1])):
        ax.text(j, i, format(data[i, j], number_fmt),
                horizontalalignment="center", verticalalignment='center',
                color=textcolor, fontsize=fontsize, fontweight=fontweight[i, j])
    ax.imshow(data, cmap=cmap)
    # Tried to force always having ticks for each box, but didn't work...
    # ax.set_xticks(np.arange(1, len(xticklabels)-1, 1))
    # ax.set_yticks(np.arange(1, len(yticklabels)-1, 1))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xticklabels(xticklabels)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if savefig:
        fig.savefig(savefig)

    return fig, ax


def heatmap_from_df(df, x_column, y_column, z_column, xlabel=None, ylabel=None, number_fmt='.3f', ax=None,
                    savefig=None):
    """
    Plot a heatmap of z_column from the DataFrame df, with x and y axes pulled from x_column and y_column

    This function assumes x_column and y_column are columns of discrete values, where all combinations exist.
    For example:
          x,  y
        [(1.0, 1.0),
         (1.0, 2.0),
         (1.0, 3.0),
         (2.0, 1.0),
         (2.0, 2.0),
         (2.0, 3.0),
         (3.0, 1.0),
         (3.0, 2.0),
         (3.0, 3.0),
         ]
    Function has not been tested for discrete with gaps, and likely wont work properly for continuous x,y data
    (eg if data is not naturally binned).

    Args:
        df (pandas.DataFrame): DataFrame to pull data from
        x_column (str): Name of the column in df to use for the x-axis
        y_column (str): Name of the column in df to use for the y-axis
        z_column (str): Name of the column in df who's values will be plotted in the heatmap
        xlabel (str): (OPTIONAL) Name to display on the x-axis (if omitted, will display x_column)
        ylabel (str): (OPTIONAL) Name to display on the y-axis (if omitted, will display y_column)
        ax (matplotlib.pyplot.axes): (OPTIONAL) Axes object to add heatmap to
        savefig (str): (OPTIONAL) If not none, save the figure to a file with the name savefig

    Return:
        (matplotlib.pyplot.axes): Axes with heatmap
    """
    if xlabel is None:
        xlabel = x_column
    if ylabel is None:
        ylabel = y_column

    x_all = df.loc[:, x_column].unique()
    y_all = df.loc[:, y_column].unique()
    toPlot = np.zeros((len(y_all), len(x_all)))
    for j, y in enumerate(y_all):
        for i, x in enumerate(x_all):
            toPlot[j, i] = df.loc[(df.loc[:, x_column] == x) & (df.loc[:, y_column] == y)].loc[:, z_column]
    fig, ax = heatmap(toPlot, x_all, y_all, xlabel=x_column, ylabel=y_column, number_fmt=number_fmt, ax=ax,
                      savefig=savefig)

    return ax


def get_fig_ax(fig=NOT_SPECIFIED, ax=NOT_SPECIFIED, fig_kwargs=None):
    """
    Convenience function to get the fig and ax objects associated with either a Matplotlib fig or axes

    Return:
        (tuple): matplotlib figure, matplotlib axes

        If input is figure, ax returned will be a list (can have multiple associated axes)
        if input is ax, fig and ax are both single objects
        If the input passed in (either figure or ax) is None, the figure and axes returned are new instances
        generated by this function
    """
    if fig_kwargs is None:
        fig_kwargs = {}
    if (fig is not NOT_SPECIFIED and ax is not NOT_SPECIFIED) or (fig is NOT_SPECIFIED and ax is NOT_SPECIFIED):
        raise ValueError("Must define exactly one of fig and ax, although the one specified can be None")
    elif fig is None or ax is None:
        fig, ax = plt.subplots(**fig_kwargs)
    elif fig is not NOT_SPECIFIED:
        ax = fig.get_axes()
    else:
        fig = ax.get_figure()

    return fig, ax


def plot_confusion_matrix(y_true, y_pred, class_name_map=None, classes_shown_on_x=None, classes_shown_on_y=None,
                          remove_if_better_than=False, remove_irrelevant_x=True, remove_irrelevant_y=True,
                          normalize=True, fontsize='small', figsize=None, cmap=plt.cm.Blues, savefig=None,
                          sort=True):
    """
    Returns a confusion matrix with integrated heatmap comparing two arrays of data

    Adapted from https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    Args:
        y_true (np.array or iterable): Iterable of truth data (to be shown on the y-axis)
        y_pred (np.array or iterable): Iterable of prediccted data (to be shown on the x-axis)
        class_name_map (dict or map): (OPTIONAL) Map to replace given class names.  For example, use to replace machine-
                                      readable class names with human-readable class names
        classes_shown_on_x[y] (list): Specifies which classes are shown on this axis.
                                      If None, all classes in y_true are shown
        normalize (bool): If True, matrix shows numbers normalized across the row (each row sums to 1).
        cmap: Colormap to use to plot heatmap (background color) for confusion matrix
        savefig (str): (OPTIONAL) Filename to save the figure to
        ax (Axes): (OPTIONAL) Axes to plot to

    Returns:
        matplotlib.axes
    """

    if classes_shown_on_y is None:
        unique_true = np.unique(y_true)
        pred_not_in_true = [x for x in np.unique(y_pred) if not (x in unique_true)]
        classes_shown_on_y = np.hstack((unique_true, pred_not_in_true))
    else:
        classes_shown_on_y = np.asarray(classes_shown_on_y)
    if classes_shown_on_x is None:
        unique_true = np.unique(y_true)
        pred_not_in_true = [x for x in np.unique(y_pred) if not (x in unique_true)]
        classes_shown_on_x = np.hstack((unique_true, pred_not_in_true))
    else:
        classes_shown_on_x = np.asarray(classes_shown_on_x)

    # Compute confusion matrix
    # Include all classes from both x and y initially
    all_classes = list(set(classes_shown_on_y) | set(classes_shown_on_x))
    cm = confusion_matrix(y_true, y_pred, labels=all_classes)
    cm_df = pd.DataFrame(cm, index=all_classes, columns=all_classes)

    if normalize:
        # Normalize by the count in each row.  If a row has no data, fudge the sum to get normalized values of 0 not nan
        row_sums = cm_df.sum(axis=1)
        row_sums[row_sums < 1] = 1
        cm_df = cm_df.div(row_sums, axis=0)
        # Threshold for printing on confusion matrix
        thresh_text = 0.005
    else:
        # Threshold for printing on confusion matrix
        thresh_text = 1

    if remove_if_better_than:
        # Grab the relevant subset
        cm_df = cm_df.loc[classes_shown_on_y, classes_shown_on_x]
        diag = cm_df.values.diagonal()
        to_remove = ~(diag >= remove_if_better_than)
        classes_shown_on_y = classes_shown_on_y[to_remove]
        # Reorder x labels so they follow the same order as y
        classes_shown_on_x = [c for c in classes_shown_on_y if c in classes_shown_on_x] + \
                             [c for c in classes_shown_on_x if c not in classes_shown_on_y]

    if sort:
        # Ensure all y labels are in x (sorting is done on the diagonal, which means all y must be in x)
        # Must be a vectorized version of this...
        for y in classes_shown_on_y:
            if y not in classes_shown_on_x:
                raise ValueError("All y labels must be included as x labels as well in order to sort results")

        # Grab the relevant subset
        cm_df = cm_df.loc[classes_shown_on_y, classes_shown_on_x]

        # Get indices of rows that have no true labels and thus should not be in the sorting
        # (put them after the sorted columns)
        _, integer_index_of_rows_without_true_labels = get_zero_axes(cm_df, return_sums=False, axis=1)

        cm = cm_df.values
        # Sort y labels in ascending order based on the diagonal (how well the classify properly)
        sorted_y_order = np.argsort(cm.diagonal())
        # classes_shown_on_y = classes_shown_on_y[sorted_y_order]
        classes_shown_on_y = [classes_shown_on_y[c] for c in sorted_y_order if c not in
                              integer_index_of_rows_without_true_labels] + \
                             [classes_shown_on_y[c] for c in integer_index_of_rows_without_true_labels]
        # Reorder x labels so they follow the same order as y
        classes_shown_on_x = [c for c in classes_shown_on_y if c in classes_shown_on_x] + \
                             [c for c in classes_shown_on_x if c not in classes_shown_on_y]

    if remove_irrelevant_x:
        to_remove = []
        for i, x in enumerate(classes_shown_on_x):
            if (x not in classes_shown_on_y) and (not (cm_df.loc[:, x].max() > 0)):
                to_remove.append(i)
        classes_shown_on_x = [classes_shown_on_x[i] for i in range(len(classes_shown_on_x)) if i not in to_remove]

    if remove_irrelevant_y:
        # Remove anything that has no truth (row-wise sum to 0) from the y axis
        # Find any rows without truth so we can remove them from y
        to_remove, _ = get_zero_axes(cm_df, axis=1, return_sums=False)
        classes_shown_on_y = [y for y in classes_shown_on_y if y not in to_remove]

    # Grab the relevant subset in its specified order
    cm_df = cm_df.loc[classes_shown_on_y, classes_shown_on_x]
    cm = cm_df.values

    if figsize is None:
        figsize = (min((len(classes_shown_on_x) + 6) / 2, 30), min((len(classes_shown_on_y) + 2) / 2, 22))
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)

    # We want to show all ticks...
    if class_name_map is not None:
        xticklabels = [class_name_map.get(c, c) for c in classes_shown_on_x]
        yticklabels = [class_name_map.get(c, c) for c in classes_shown_on_y]
    else:
        xticklabels = classes_shown_on_x
        yticklabels = classes_shown_on_y

    # Cache the xlim/ylim as they may get changed by the below call
    xlim_ = ax.get_xlim()
    ylim_ = ax.get_ylim()
    ax.set_xticks(np.arange(cm.shape[1]), )
    ax.set_yticks(np.arange(cm.shape[0]), )
    ax.set_xticklabels(xticklabels)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel('True label')
    ax.set_ylabel('Predicted label')
    ax.set_xticks(np.arange(cm.shape[1] - 1) + 0.5, minor=True)
    ax.set_yticks(np.arange(cm.shape[0] - 1) + 0.5, minor=True)
    ax.grid(which='minor', color='lightgrey', linestyle=':', linewidth=1)
    ax.set_axisbelow(True)  # Move the gridlines behind the data
    ax.set_xlim(xlim_)
    ax.set_ylim(ylim_)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh_color = cm.max() / 2.

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if cm[i, j] >= thresh_text:
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh_color else "black",
                        fontsize=fontsize)


    # Add highlighting around the primary diagonal
    for i, ylabel in enumerate(classes_shown_on_y):
        for j, xlabel in enumerate(classes_shown_on_x):
            if xlabel == ylabel:
                # print(xlabel, ylabel)
                y = i - 0.5
                x = j - 0.5
                # print(f"Adding patch at {x}, {y}")
                ax.add_patch(Rectangle((x, y), 1, 1, fill=False, edgecolor='g', lw=3))
                break

    fig.tight_layout()

    if savefig:
        fig.savefig(savefig + '.png')

    return ax
