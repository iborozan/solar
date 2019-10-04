def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    """A function for saving figures in a prespecified direcotry"""
    IMAGES_PATH = '/home/iborozan/work/Data-Science/Insight/project/presentations/week4/'
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", path)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

    
def corr_heat_map(df, title, size):
    """
    This function plots a correlation heatmap for a dataframe 
    """
    corrs = df.corr()
    
    # set figure size
    fig, ax = plt.subplots(figsize = size)
    
    # generate a mask for the upper triagle 
    mask = np.zeros_like(corrs, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    
    #plot heatmap
    ax = sns.heatmap(corrs, mask=mask, annot = True, cbar=False)
    
    #resize labels
    ax.set_xticklabels(ax.xaxis.get_ticklabels(), fontsize=12, rotation=90)
    ax.set_yticklabels(ax.yaxis.get_ticklabels(), fontsize=12, rotation=45)
    ax.set_title(title, fontsize=14)
    fig.tight_layout()
    #https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
    plt.subplots_adjust(bottom = 0.33)
    #save_fig("heatmap_corr")
    #plt.show()
