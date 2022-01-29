import numpy as np
import matplotlib.pyplot as plt
import vsnap

fig=plt.figure();
ax=fig.add_subplot(211)
bx=fig.add_subplot(212)

nums=range(30)

dir_sc="A15H4"
dir_in="Bead"
for k in nums:
    fname="v"+str(k)+".out";
    fnin=dir_in+"/"+fname
    fnsc=dir_sc+"/"+fname
    print(fnin)
    print(fnsc)
    vin=vsnap.Vfld(dir_in+"/"+fname);
    vsc=vsnap.Vfld(dir_sc+"/"+fname);

    vsc.v1-=vin.v1
    vsc.v2-=vin.v2
    vin.draw1(ax)
    vsc.draw1(bx)
    
    fig.savefig("sc"+str(k)+".png",bbox_inches="tight")



