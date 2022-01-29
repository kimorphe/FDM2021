import bscan
import numpy as np
import matplotlib.pyplot as plt



if __name__=="__main__":

    dir_sc="A15H4"
    dir_in="Bead"
    fname="rec0.out"
    fnin=dir_in+"/"+fname
    fnsc=dir_sc+"/"+fname



    #fig1,ax1=rec_in.bscan();
    #fig2,ax2=rec_sc.bscan();
    fig=plt.figure()
    ax1=fig.add_subplot(311)
    ax2=fig.add_subplot(312)
    ax3=fig.add_subplot(313)
    rec_in=bscan.REC(fnin)
    rec_sc=bscan.REC(fnsc)
    
    clr_map="pink"
    clr_map="ocean_r"
    clr_map="gray_r"
    #clr_map="jet"
    v1=-8.e-04
    v2= 8.e-04
    rec_in.bscan2(ax1,cmap=clr_map,v1=v1,v2=v2)
    rec_sc.bscan2(ax2,cmap=clr_map,v1=v1,v2=v2)
    rec_sc.dat-=rec_in.dat
    rec_sc.bscan2(ax3,cmap=clr_map,v1=v1,v2=v2)
    ax1.set_xlim([0,50])
    ax2.set_xlim([0,50])
    ax3.set_xlim([0,50])

    fig.savefig("dbscan.png",bbox_inches="tight")
    plt.show()


		
		
