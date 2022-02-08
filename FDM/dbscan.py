import bscan
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker

if __name__=="__main__":


    # DATA FOLDERS 
    dir_sc="L4A10"  # scatterd field (example)
    dir_in="None"   # incident field (mandatory)
    fname="rec0.out" # Bscan data file
    dir_sc=input("Type Data Folder Name:")# select scattered wave data folder 
    fnin=dir_in+"/"+fname   # incident field 
    fnsc=dir_sc+"/"+fname   # scattered wave field
    fnout=dir_sc+".png" # output file name

    # Figure & Axes
    fig=plt.figure(figsize=[6,7])
    ax1=fig.add_subplot(311)
    ax2=fig.add_subplot(312)
    ax3=fig.add_subplot(313)
    rec_in=bscan.REC(fnin)
    rec_sc=bscan.REC(fnsc)
    
    clr_map="pink"
    clr_map="ocean_r"
    clr_map="gray"
    clr_map="gray_r"

    fmt=matplotlib.ticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0,0))


    v1=-2.e-03
    v2= 2.e-03

    v1=-5.e-04
    v2= 5.e-04
    rec_in.bscan2(ax1,cmap=clr_map,v1=v1,v2=v2)
    rec_sc.bscan2(ax2,cmap=clr_map,v1=v1,v2=v2)
    rec_sc.dat-=rec_in.dat
    im=rec_sc.bscan2(ax3,cmap=clr_map,v1=v1,v2=v2)

    fsz=12; Fsz=14
    ax1.tick_params(labelbottom=False)
    ax2.tick_params(labelbottom=False)
    #ax3.tick_params(labelsize=fsz)
    ax3.set_xlabel("time[$\mu$sec]",fontsize=fsz)
    ax2.set_ylabel("x [mm]",fontsize=fsz)

    ax1.text(0,40,"(a)",fontsize=Fsz)
    ax2.text(0,40,"(b)",fontsize=Fsz)
    ax3.text(0,40,"(c)",fontsize=Fsz)

    plt.subplots_adjust(left=0.1,right=0.9, bottom=0.2, top=0.9)
    cax=plt.axes([0.1,0.08,0.8,0.04]) # (left,bottom),(right,top)
    cb=plt.colorbar(im,cax=cax,orientation="horizontal",format=fmt)

    fig.savefig(fnout,bbox_inches="tight")
    plt.show()


		
		
