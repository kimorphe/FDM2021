import numpy as np
import matplotlib.pyplot as plt


class Crv:
    def __init__(self, fname):
        fp=open(fname,"r")
        xx=[]
        yy=[]
        for row in fp:
            dat=row.strip().split(",")
            xx.append(float(dat[0]))
            yy.append(float(dat[1]))
        
        xx.append(xx[0])
        yy.append(yy[0])

        self.xx=np.array(xx)
        self.yy=np.array(yy)
        fp.close()
    def draw(self,ax,clr="k",lw=1):
        ax.plot(self.xx,self.yy,"-"+clr,linewidth=lw)

if __name__=="__main__":
    crv=Crv("L4A0/bnd.out")
    fig=plt.figure()
    ax=fig.add_subplot(111)
    crv.draw(ax)
    ax.set_aspect(1.0)

    plt.show()
