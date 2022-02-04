#!  /home/kazushi/anaconda3/bin/python
import numpy as np
import matplotlib.pyplot as plt
import bscan

class Vfld:
	def __init__(self,fname):
		fp=open(fname,"r");
		self.tstmp=fp.readline().strip();
		print(self.tstmp)
		txt=self.tstmp.split("=");
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

		#self.v1=[];
		#self.v2=[];
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
		self.v=np.sqrt(self.v1**2+self.v2**2)

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
		img=ax.imshow(V,extent=rng,vmin=0,vmax=0.01,cmap="jet",origin="lower");

		ax.set_xlabel("x")
		ax.set_ylabel("y")
		#ax.set_title("|v|")
		return(img)


if __name__=="__main__":

    dir_name="L4A0"
    dir_name+="/"
    fnrec="rec0.out"
    rec=bscan.REC(dir_name+fnrec)

    nfile=15;
    inc=1;
    n1=1

    fig=plt.figure();
    ax=fig.add_subplot(211)
    bx=fig.add_subplot(212)
    rec.bscan2(bx)

    iplt=0
    for k in range(n1,nfile,inc):
        fname="v"+str(k)+".out";
        fname=dir_name+fname
        print(fname)
        vf=Vfld(fname);
        if iplt==0:
            line,=bx.plot([vf.time,vf.time],rec.ylim)
            img=vf.draw1(ax);
        else:
            line.set_xdata([vf.time,vf.time])
            line.set_ydata([rec.ylim])
            img.set_data(vf.v)
        #if k==1:
        #	plt.colorbar(cax1,orientation='horizontal')
        fig.savefig(str(k)+".png",bbox_inches="tight")
        #plt.pause(0.1)
        iplt+=1
