import numpy as np

def auc_roc(X,Y, ncrit):
    """
    Returns the Area-Under-the-ROC-Curve 
    and the sensitivity (true  positive rate; X,Y>0)
    and specificity (1 - false positive rate; X,Y==0)
    for a range of criteria based on quantile thresholding
    -------------------------------------------------------------------------
    INPUTs:
    -X:      ground truth
    -Y:      estimated connectivity matrix (e.g., PDC)
    -ncrit:  number of criteria used (spacing from 0-1)
    """

    if (not np.isnan(Y[0]).any()) and (len(Y.shape) >2):
        dg = Y.shape[0]
        for ij in range(dg):
            X[ij,ij,:,:] = np.nan;
            Y[ij,ij,:,:] = np.nan;
    X = X[~np.isnan(X)]
    Y = Y[~np.isnan(Y)]
    qrange = np.linspace(0.001,1,ncrit)
    sens = np.zeros(ncrit)
    spec = np.zeros(ncrit)
    thre = np.quantile(Y,qrange)

    ids_great = X>0
    ids_eq = X==0
    for k in range(ncrit):
        sens[k] = np.nanmean(Y[ids_great]>=thre[k])
        spec[k] = np.nanmean(Y[ids_eq]<thre[k])
    auc = abs(np.trapz(sens,1-spec))    
    return spec,sens,auc

