import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def show_cmap(cmap_name, title=False):
    # Create a gradient image
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    # Plot the gradient image using the 'viridis' colormap
    _, ax = plt.subplots(figsize=(6, .5))
    ax.imshow(gradient, aspect='auto', cmap=cmap_name)
    if title:
        ax.set_title(cmap_name, fontsize=12)
    ax.set_axis_off();