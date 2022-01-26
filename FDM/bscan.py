#! /home/kazushi/anaconda3/bin/python
import numpy as np
import matplotlib.pyplot as plt


class REC:
    def __init__(self,fname):
        fp=open(fname,"r");
        fp.readline();
        tmp=fp.readline().lstrip().split(" ");
        self.dt=float(tmp[0]);
        self.Nt=int(tmp[1]);
        fp.readline();
        tmp=fp.readline().lstrip().split(" ");
        self.Ng=int(tmp[0]);
        self.ityp=int(tmp[1]);
        fp.readline();
        self.xsrc=[];
        self.ysrc=[];
        for k in range(self.Ng):
            self.xsrc.append(0.);
            self.ysrc.append(0.);
            (self.xsrc[k],self.ysrc[k])=fp.readline().lstrip().split(" ");
        self.xsrc=list(map(float,self.xsrc));
        self.ysrc=list(map(float,self.ysrc));
        self.xsrc=np.array(self.xsrc);
        self.ysrc=np.array(self.ysrc);
        fp.readline();
        dat=fp.readlines();
        dat=np.array(list(map(float,dat)))
        print(np.shape(dat))
        print(self.Nt*self.Ng);
        self.dat=np.reshape(dat,(self.Ng,self.Nt))
    def bscan(self):
        fig=plt.figure();
        ax=fig.add_subplot(1,1,1);

        x1=self.ysrc[0];
        x2=self.ysrc[-1];
        x1=self.xsrc[0];
        x2=self.xsrc[-1];
        t1=0.;
        t2=self.dt*self.Nt;
        #im=ax.imshow(self.dat,extent=[t1,t2,x2,x1],cmap="jet",aspect="auto",vmin=-0.01,vmax=0.01);
        im=ax.imshow(self.dat,extent=[t1,t2,x2,x1],cmap="jet",aspect="auto",vmin=-0.005,vmax=0.005,interpolation="bicubic");
        #plt.colorbar(im,orientation="horizontal")
        return fig,ax;

rec=REC("rec0.out")

fig,ax=rec.bscan();
plt.show()


		
		
