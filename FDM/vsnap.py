#!  /home/kazushi/anaconda3/bin/python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Vfld:
	def __init__(self,fname):
		fp=open(fname,"r");
		self.tstmp=fp.readline();
		txt=self.tstmp.split("=")
		self.time=float(txt[1])

		fp.readline();
		tmp=fp.readline().lstrip().split(" ");
		self.xlim=list(map(float,tmp));

		fp.readline();
		tmp=fp.readline().lstrip().split(" ");
		self.ylim=list(map(float,tmp));

		fp.readline();
		tmp=fp.readline().lstrip().split(" ");
		self.Ng=list(map(int,tmp));

		fp.readline();

		dat=fp.readlines();

		ndat=self.Ng[0]*self.Ng[1];
		self.v1=np.zeros(ndat);
		self.v2=np.zeros(ndat);
		ndat=0
		for row in dat:
			item=row.lstrip().split(" ");
			self.v1[ndat]=float(item[0])
			self.v2[ndat]=float(item[1])
			ndat+=1

		fp.close()
		self.v1=np.reshape(self.v1,[self.Ng[0],self.Ng[1]])
		self.v2=np.reshape(self.v2,[self.Ng[0],self.Ng[1]])
		self.v1=np.transpose(self.v1)
		self.v2=np.transpose(self.v2)
		self.v=np.sqrt(self.v1*self.v1+self.v2*self.v2);
	def draw0(self):
		fig=plt.figure();
		indx=np.arange(self.Ng[1],0,-1)-1;
		for k in range(self.Ng[0]):
			self.v1[k]=self.v1[k][indx];
			self.v2[k]=self.v2[k][indx];
		self.v1=np.transpose(self.v1)
		self.v2=np.transpose(self.v2)

		rng=[self.xlim[0],self.xlim[1],self.ylim[0], self.ylim[1]];
		ax1=fig.add_subplot(1,2,1)
		cax1=ax1.imshow(self.v1,extent=rng,vmin=-0.6,vmax=0.6,cmap="jet");
		plt.colorbar(cax1,orientation='horizontal')

		ax2=fig.add_subplot(1,2,2)
		cax2=ax2.imshow(self.v2,extent=rng,vmin=-0.1,vmax=0.1,cmap="jet");
		plt.colorbar(cax2,orientation='horizontal')

		ax1.set_xlabel("x")
		ax2.set_xlabel("x")
		ax1.set_ylabel("y")
		ax1.set_title("v1")
		ax2.set_title("v2")
	def draw1(self,ax):
		rng=[self.xlim[0],self.xlim[1],self.ylim[0], self.ylim[1]];
		V=np.sqrt(self.v1*self.v1+self.v2*self.v2);
		img=ax.imshow(V,extent=rng,vmin=0,vmax=0.01,cmap="jet",origin="lower",rasterized=True);

		ax.set_xlabel("x[mm]",fontsize=12)
		ax.set_ylabel("y[mm]",fontsize=12)
		return(img)


if __name__=="__main__":

    nfile=50;
    inc=1;
    n1=1

    fig=plt.figure();
    ax=fig.add_subplot(1,1,1)

    #pdf=PdfPages("figs.pdf")

    isum=0
    for k in range(n1,nfile,inc):
        fname="v"+str(k)+".out";
        print(fname)
        vf=Vfld(fname);
        if isum==0:
            img=vf.draw1(ax);
            #plt.colorbar(cax1,orientation='horizontal')
        else:
            img.set_data(vf.v)
        isum+=1
        #ax.text(30,10,"t={:.2f}".format(vf.time)+"$\mu$sec",color="w")
        ax.set_title("t={:.2f}".format(vf.time)+"$\mu$sec",color="k")

        fig.savefig(str(k)+".png",bbox_inches="tight",dpi=300)
        #fig.savefig(str(k)+".pdf",bbox_inches="tight",dpi=300)
        #pdf.savefig(fig,dpi=400)
        #ax.clear()
        #plt.pause(0.1)
        #raw_input("press enter to continue");
    #pdf.close()
