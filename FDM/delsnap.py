#!  /home/kazushi/anaconda3/bin/python
import numpy as np
import matplotlib.pyplot as plt

class Vfld:
	def __init__(self,fname):
		fp=open(fname,"r");
		self.tstmp=fp.readline();

		fp.readline();
		tmp=fp.readline().lstrip().split(" ");
		self.xlim=list(map(float,tmp));

		fp.readline();
		tmp=fp.readline().lstrip().split(" ");
		self.ylim=list(map(float,tmp));

		fp.readline();
		tmp=fp.readline().lstrip().split(" ");
		self.Ng=list(map(int,tmp));
		ndat=self.Ng[0]*self.Ng[1]
		fp.readline();

		dat=fp.readlines();

		self.v1=[];
		self.v2=[];
		#for row in dat:
		for k in range(ndat):
			row=dat[k]
			item=row.lstrip().split(" ");
			self.v1.append(float(item[0]))
			self.v2.append(float(item[1]))

		fp.close()

		self.v1=np.array(self.v1)
		self.v2=np.array(self.v2)

		ndim=(self.Ng[0],self.Ng[1]);
		self.v1=np.reshape(self.v1,ndim)
		self.v2=np.reshape(self.v2,ndim)
	
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

		indx=np.arange(self.Ng[1],0,-1)-1;
		for k in range(self.Ng[0]):
			self.v1[k]=self.v1[k][indx];
			self.v2[k]=self.v2[k][indx];

		self.v1=np.transpose(self.v1)
		self.v2=np.transpose(self.v2)

		rng=[self.xlim[0],self.xlim[1],self.ylim[0], self.ylim[1]];
		V=np.sqrt(self.v1*self.v1+self.v2*self.v2);
		cax1=ax.imshow(V,extent=rng,vmin=0.0,vmax=0.005,cmap="jet");

		ax.set_xlabel("x")
		ax.set_ylabel("y")
		ax.set_title("|v|")


if __name__=="__main__":
    nfile=10;
    inc=1;

    fig=plt.figure();
    ax=fig.add_subplot(1,1,1)

    for k in range(0,nfile,inc):
        fname="w"+str(k)+".out";
        print(fname)
        vf=Vfld(fname);
        #vf.draw0();
        vf.draw1(ax);
        #if k==1:
        #	plt.colorbar(cax1,orientation='horizontal')
        fig.savefig("w"+str(k)+".png",bbox_inches="tight")
        plt.pause(0.1)
        #raw_input("press enter to continue");
