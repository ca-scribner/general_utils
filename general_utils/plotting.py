import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def cmap_to_discrete(cmap, vmin=0., vmax=1., bin_increment=0.1, increments=None, increment_limit=20):
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
