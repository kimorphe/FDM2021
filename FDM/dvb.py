#!  /home/kazushi/anaconda3/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
import bscan
import bnd
import os

from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

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
		#img=ax.imshow(V,extent=rng,vmin=0,vmax=vmax,cmap="jet",origin="lower",aspect="equal");
		img=ax.imshow(self.v2,extent=rng,vmin=-vmax,vmax=vmax,cmap="jet",origin="lower",aspect="equal");
		return(img)


if __name__=="__main__":

    dir_name="L4A15"
    dir_name=input("Data folder?")
    png_dir="PNG_"+dir_name
    if not os.path.exists(png_dir):
        os.mkdir(png_dir)

    dir_name+="/"
    fnrec="rec0.out"
    rec=bscan.REC(dir_name+fnrec)


    rec2=bscan.REC("None/"+fnrec)
    rec.dat-=rec2.dat

    geom_in=bnd.Crv("None/bnd.out")
    geom_sc=bnd.Crv(dir_name+"bnd.out")

    nfile=100;
    inc=1;
    n1=1

    fig=plt.figure(figsize=[11,6]);
    ax=fig.add_subplot(221) # incident field
    bx=fig.add_subplot(223) # scattered field
    cx=fig.add_subplot(122) # Bscan

    #---------COLOR SCALES-----------
    vmax_bwv=5.e-04
    vmax_in= 5.e-03
    vmax_sc= 5.e-04
    #--------------------------------
    bimg=rec.bscan3(cx,v1=-vmax_bwv,v2=vmax_bwv,cmap="jet")

    ax_divider=make_axes_locatable(ax)
    bx_divider=make_axes_locatable(bx)
    cx_divider=make_axes_locatable(cx)
    cax=ax_divider.append_axes("right",size="5%",pad="3%")
    cbx=bx_divider.append_axes("right",size="5%",pad="3%")
    ccx=cx_divider.append_axes("bottom",size="3%",pad="12%")
    fmt=matplotlib.ticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0,0))
    cb3=fig.colorbar(bimg,cax=ccx,orientation="horizontal",format=fmt)

    iplt=0
    for k in range(n1,nfile,inc):
        fname="v"+str(k)+".out";
        print(fname)
        vf=Vfld(dir_name+fname);
        vf2=Vfld("None/"+fname);
        vf.v1-=vf2.v1
        vf.v2-=vf2.v2
        if iplt==0:
            #line,=cx.plot([vf.time,vf.time],rec.ylim)
            line,=cx.plot(rec.ylim,[vf.time,vf.time],"k",linewidth=1.0,label="current time")

            img2=vf2.draw1(ax,vmax=vmax_in);
            img=vf.draw1(bx,vmax=vmax_sc);
            ax.set_ylabel("y [mm]")
            bx.set_ylabel("y [mm]")
            bx.set_xlabel("x [mm]")
            cx.set_xlabel("x [mm]")
            cx.set_ylabel("time [micro sec]",rotation=90)
            ax.set_title("incident field")
            #bx.set_title("scattered field")
            cx.set_title("travel time plot")

            bx.plot(rec.ylim,rec.ysrc[0:2],"k",linewidth=2,label="observation area")
            #txt=ax.text(20,30,"t="+str(vf.time),size=12,color="w")
            cb1=fig.colorbar(img,cax=cax,orientation="vertical",format=fmt)
            cb2=fig.colorbar(img2,cax=cbx,orientation="vertical",format=fmt)
            ax.set_xlim(vf.xlim)
            bx.set_xlim(vf.xlim)
            ax.set_ylim(vf.ylim)
            bx.set_ylim(vf.ylim)
            geom_in.draw(ax,"w",lw=1.0)
            geom_sc.draw(ax,"w",lw=0.5)
            geom_sc.draw(bx,"w",lw=1.0)

            axp=ax.get_position()
            bxp=bx.get_position()
            cxp=cx.get_position()
            w=axp.width*0.7
            #h=axp.height
            x0=cxp.x0+0.01
            y0=bxp.y0
            h=(axp.y0+axp.height-bxp.y0)
            cx.set_position([x0,y0,w,h])
            bx.legend(loc="upper right")
            cx.legend(loc="upper right")
            cx.set_ylim([45,0])
        else:
            #line.set_xdata([vf.time,vf.time])
            #line.set_ydata([rec.ylim])
            line.set_xdata([rec.ylim])
            line.set_ydata([vf.time,vf.time])
            V=np.sqrt(vf.v1**2+vf.v2**2)
            #img.set_data(V)
            #img2.set_data(vf2.v)
            img.set_data(vf.v2)
            img2.set_data(vf2.v2)
            #txt.text="time="+str(vf.time)
            #txt.text="time="+str(vf.time)
            #txt=ax.text(20,30,"t="+str(vf.time),size=12,color="w")
        ax.set_title("incident field (t={:.2f}".format(vf.time)+"$\mu$sec)")
        bx.set_title("scattere field (t={:.2f}".format(vf.time)+"$\mu$sec)")
        #cx.set_xlim([-25,45])
        #if k==1:
        #	plt.colorbar(cax1,orientation='horizontal')
        fig.savefig(png_dir+"/"+str(k)+".png",bbox_inches="tight")
        #plt.pause(0.1)
        iplt+=1
