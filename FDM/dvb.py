#!  /home/kazushi/anaconda3/bin/python
import numpy as np
import matplotlib.pyplot as plt
import bscan
import bnd

class Vfld:
	def __init__(self,fname):
		fp=open(fname,"r");
		self.tstmp=fp.readline().strip();
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
	def draw1(self,ax,vmax=0.01):
		rng=[self.xlim[0],self.xlim[1],self.ylim[0], self.ylim[1]];
		V=np.sqrt(self.v1*self.v1+self.v2*self.v2);
		img=ax.imshow(V,extent=rng,vmin=0,vmax=vmax,cmap="jet",origin="lower",aspect="equal");
		return(img)

if __name__=="__main__":

    dir_name="L4A15"
    dir_name+="/"
    fnrec="rec0.out"
    rec=bscan.REC(dir_name+fnrec)

    rec2=bscan.REC("None/"+fnrec)
    rec.dat-=rec2.dat

    nfile=100;
    inc=1;
    n1=1

    fig=plt.figure(figsize=[9,6]);
    ax=fig.add_subplot(221) # incident field
    bx=fig.add_subplot(223) # scattered field
    cx=fig.add_subplot(122) # Bscan
    rec.bscan3(cx,v1=-0.0002,v2=0.0002,cmap="gray_r")

    geom=bnd.Crv(dir_name+"bnd.out")
    geom1=bnd.Crv("None/bnd.out")

    iplt=0
    for k in range(n1,nfile,inc):
        fname="v"+str(k)+".out";
        print(fname)
        vf=Vfld(dir_name+fname);
        vf2=Vfld("None/"+fname);
        vf.v1-=vf2.v1
        vf.v2-=vf2.v2
        vmax=0.003
        if iplt==0:
            #line,=cx.plot([vf.time,vf.time],rec.ylim)
            line,=cx.plot(rec.ylim,[vf.time,vf.time],"r",linewidth=1)
            img=vf.draw1(bx,vmax=vmax);
            img2=vf2.draw1(ax,vmax=vmax);
            ax.set_ylabel("y [mm]")
            bx.set_ylabel("y [mm]")
            bx.set_xlabel("x [mm]")
            cx.set_xlabel("x [mm]")
            cx.set_ylabel("time [micro sec]",rotation=90)
            cx.set_title("travel time plot")

            bx.plot(rec.ylim,rec.ysrc[0:2],"r",linewidth=2)
            #txt=ax.text(20,30,"t="+str(vf.time),size=12,color="w")
            #cax=plt.axes([0.15,0.5, 0.3,0.04]) # for Plate 
            cax=plt.axes([0.15,0.5, 0.3,0.03]) 
            cb1=plt.colorbar(img,cax=cax,orientation="horizontal")
            ax.set_xlim(vf.xlim)
            bx.set_xlim(vf.xlim)
            ax.set_ylim(vf.ylim)
            bx.set_ylim(vf.ylim)
            geom1.draw(ax,"w",lw=1.0)
            geom.draw(bx,"w",lw=1.0)
        else:
            #line.set_xdata([vf.time,vf.time])
            #line.set_ydata([rec.ylim])
            line.set_xdata([rec.ylim])
            line.set_ydata([vf.time,vf.time])
            V=np.sqrt(vf.v1**2+vf.v2**2)
            img.set_data(V)
            img2.set_data(vf2.v)
            #txt.text="time="+str(vf.time)
            #txt=ax.text(20,30,"t="+str(vf.time),size=12,color="w")
        ax.set_title("incident field (t="+"{:.2f}".format(vf.time)+"$\mu$ sec)")
        bx.set_title("scattered field (t="+"{:.2f}".format(vf.time)+"$\mu$ sec)")
        axp=ax.get_position()
        bxp=bx.get_position()
        cxp=cx.get_position()
        w=axp.width*0.8
        h=axp.height
        x0=cxp.x0
        y0=bxp.y0
        h=axp.y0+axp.height-bxp.y0
        cx.set_position([x0,y0,w,h])
        #cx.set_xlim([-25,45])
        #if k==1:
        #	plt.colorbar(cax1,orientation='horizontal')
        fig.savefig(str(k)+".png",bbox_inches="tight",dpi=300)
        #plt.pause(0.1)
        iplt+=1
