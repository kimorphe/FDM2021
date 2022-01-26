from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.axes_grid1.colorbar import colorbar

class IMG:
    def __init__(self,fname):
        img_rgb=Image.open(fname)
        IM=np.array(img_rgb)
        print(type(IM))
        print(IM.dtype)
        print(IM.shape)
        self.IM=IM;
        self.N=IM.shape
        self.img_rgb=img_rgb
        self.fname=fname
    def draw_rect(self,ax,Xa,Xb,clr="k"):
        xs=[Xa[0],Xb[0],Xb[0],Xa[0],Xa[0]]
        ys=[Xa[1],Xa[1],Xb[1],Xb[1],Xa[1]]
        ax.plot(xs,ys,clr)
    def trim(self,Xa,Xb):
        self.IM=self.IM[Xa[0]:Xb[0],Xa[1]:Xb[1],:]
        self.N=self.IM.shape
        print(self.N)
    def show_mm(self,ax,mm_pix=1):
            h=self.N[0]*mm_pix
            w=self.N[1]*mm_pix
            ext=[0,w,0,h]
            ax_im=ax.imshow(self.IM,extent=ext)
            ax.grid(True)
            ax.set_xlabel("x [mm]",fontsize=12)
            ax.set_ylabel("y [mm]",fontsize=12)
    def trim_mm(self,Xa,Xb,mm_pix):
        #print("Xa=",Xa[0],Xa[1],"-->")
        #print("Xb=",Xb[0],Xb[1],"-->")
        Xa=(np.array(Xa))/mm_pix+0.5
        Xb=(np.array(Xb))/mm_pix+0.5
        Xa=Xa.astype(int)
        Xb=Xb.astype(int)
        print("Xa=",Xa[0],Xa[1])
        print("Xb=",Xb[0],Xb[1])
        Ia=[self.N[0]-Xa[1],Xa[0]]
        Ib=[self.N[0]-Xb[1],Xb[0]]
        #self.IM=self.IM[Xb[1]:Xa[1],Xa[0]:Xb[0],:]
        self.IM=self.IM[Ib[0]:Ia[0],Ia[1]:Ib[1],:]
        self.N=self.IM.shape
        print("image size(trimmed)=",self.N)
    def img2kcell(self,mm_pix=1):
        R=self.IM[:,:,0].astype(float)
        G=self.IM[:,:,1].astype(float)
        B=self.IM[:,:,2].astype(float)
        #self.IM=R*0.299+G*0.587+B*0.114
        #self.IM=(R+G+B)/3
        self.IM=self.IM[:,:,3]

        Lev=100;
        indxH=(self.IM >Lev)
        indxL=(self.IM <=Lev)
        self.IM[indxL]=1
        self.IM[indxH]=0

        fn=self.fname.replace(".png","_kcell.dat")
        fp=open(fn,"w")
        W=mm_pix*self.N[1]
        H=mm_pix*self.N[0]
        fp.write("# width, height\n")
        fp.write(str(W)+", "+str(H)+"\n")
        fp.write("# Nx, Ny\n")
        fp.write(str(self.N[1])+", "+str(self.N[0])+"\n")
        fp.write("# binary data (0/1)\n")
        for x in range(self.N[1]):
            j=x
            for y in range(self.N[0]):
                i=self.N[0]-y-1
                fp.write( str(self.IM[i,j])+"\n")
        print("kcell data has been written in",fn)
        fp.close()


    def show(self,ax,typ=""):
        self.R=self.IM[:,:,0].astype(float)
        self.G=self.IM[:,:,1].astype(float)
        self.B=self.IM[:,:,2].astype(float)
        self.I=(self.R+self.G+self.B)/3.
        R=self.R
        G=self.G
        B=self.B
        I=self.I
        im_cmp="hot"
        if typ=="":
            ax_im=ax.imshow(self.IM)
            ax.set_title("Original")
        if typ=="R":
            ax_im=ax.imshow(self.R,cmap=im_cmp)
            ax.set_title("R")
        if typ=="G":
            ax_im=ax.imshow(self.G,cmap=im_cmp)
            ax.set_title("G")
        if typ=="B":
            ax_im=ax.imshow(self.B,cmap=im_cmp)
            ax.set_title("B")
        if typ=="mean":
            ax_im=ax.imshow(I,cmap=im_cmp)
            ax.set_title("Mean (brightness)")
        if typ=="dR":
            ax_im=ax.imshow(R-I,cmap=im_cmp,vmin=0)
            ax.set_title("dR")
        if typ=="dG":
            ax_im=ax.imshow(G-I,cmap=im_cmp,vmin=0)
            ax.set_title("dG")
        if typ=="dB":
            ax_im=ax.imshow(B-I,cmap=im_cmp,vmin=0)
            ax.set_title("dB")
        if typ=="Bt":
            ax_im=ax.imshow(-I,cmap=im_cmp,vmin=-50,vmax=-0)
            ax.set_title("Biotite")
        if typ=="K":
            ax_im=ax.imshow(R-G,cmap=im_cmp,vmin=-0,vmax=20)
            ax.set_title("K-Feldspar")
        if typ=="Na":
            ax_im=ax.imshow(B-G,cmap=im_cmp,vmin=-5,vmax=20)
            ax.set_title("Na-Feldspar")
        ax.grid(True)
        return(ax_im)
    def show_hist(self,ax,typ=""):
        R=self.R
        G=self.G
        B=self.B
        R=np.reshape(R,[self.N[0]*self.N[1]])
        G=np.reshape(G,[self.N[0]*self.N[1]])
        B=np.reshape(B,[self.N[0]*self.N[1]])
        I=(R+G+B)/3.0
        nbin=50
        if typ=="":
            ax.hist(R,range=[0,255],bins=nbin,color="r")
            ax.hist(G,range=[0,255],bins=nbin,alpha=0.6,color="g")
            ax.hist(B,range=[0,255],bins=nbin,alpha=0.3,color="b")
        if typ=="R":
            ax.hist(R,range=[0,255],bins=nbin,color="r")
            ax.set_title("R")
        if typ=="G":
            ax.hist(G,range=[0,255],bins=nbin,color="g")
            ax.set_title("G")
        if typ=="B":
            ax.hist(B,range=[0,255],bins=nbin,color="b")
            ax.set_title("B")
        if typ=="dR":
            ax.hist(R-I,range=[-30,30],bins=nbin,color="r")
            ax.set_title("dR")
        if typ=="dG":
            ax.hist(G-I,range=[-30,30],bins=nbin,color="g")
            ax.set_title("dG")
        if typ=="dB":
            ax.hist(B-I,range=[-30,30],bins=nbin,color="b")
            ax.set_title("dB")
        if typ=="mean":
            ax.hist(I,range=[0,225],bins=nbin,color="k")
        if typ=="Na":
            ax.hist(B-R,range=[-30,30],bins=nbin,color="G")
        if typ=="K":
            ax.hist(R-G,range=[-25,25],bins=nbin,color="R")
        ax.grid(True)
    def plot_scatter(self,ax):
        R=np.reshape(self.R,[self.N[0]*self.N[1]])
        G=np.reshape(self.G,[self.N[0]*self.N[1]])
        B=np.reshape(self.B,[self.N[0]*self.N[1]])
        I=(R+G+B)/3.0
        #ax.plot(I,R-B,"o",markersize=1,alpha=0.3)
        ax.grid(True)
        ax.set_xlabel("mean (brightness)")
        ax.set_ylabel("reddishness R-B")

        Y2=30
        Y1=-30
        W=np.zeros((255,Y2-Y1))
        for k in range(len(I)):
            ix=int(I[k])
            #iy=int(R[k]-B[k]-Y1)
            iy=int(R[k]-I[k]-Y1)
            #iy=int(I[k]-B[k]-Y1)
            if iy>=Y2-Y1:
                continue
            if iy<0:
                continue
            W[ix,iy]+=1
        W=np.transpose(W)
        ext=[0,225,Y1,Y2]
        ax.imshow(W,cmap="jet",origin="lower",extent=ext,interpolation="bicubic",aspect="auto")

    def min_map(self):
        n1=self.N[0]
        n2=self.N[1]
        y1=40
        y2=125
        y2=120
        M=np.zeros((n1,n2))
        for k in range(n1):
            for l in range(n2):
                r=self.R[k,l]
                g=self.G[k,l]
                b=self.B[k,l]
                y=(r+g+b)/3.

                if y < y1: # Biotite
                    M[k,l]=0 
                elif y < y2: # Quartz
                    M[k,l]=1
                elif r-g>0: # K-feldspar
                    M[k,l]=2 
                else: # Na-feldspar
                    M[k,l]=3
        self.M=M
        return(M)
    def write_M(self,fname):
        fp=open(fname,"w")
        n1=self.N[0]
        n2=self.N[1]
        fp.write("# Nx, Ny\n");
        fp.write(str(n1)+", "+str(n2)+"\n")
        fp.write("# 0:Bt, 1: Qt, 2: K, 3: Na\n")
        for k in range(n1):
            for l in range(n2):
                dat=str(int(self.M[k,l]))+"\n"
                fp.write(dat)
        fp.close();
    def show_min_map(self,ax):
        M=self.M
        R4=np.zeros(np.shape(M))
        G4=np.zeros(np.shape(M))
        B4=np.zeros(np.shape(M))

        # Biotite
        indx=np.where(M==0)
        r=int(np.mean(self.R[indx]))
        g=int(np.mean(self.G[indx]))
        b=int(np.mean(self.B[indx]))
        y=(r+g+b)/3.
        self.Bt_rgb=[r,g,b,y]
        R4[indx]=r; G4[indx]=g; B4[indx]=b;

        # Quartz 
        indx=np.where(M==1)
        r=int(np.mean(self.R[indx]))
        g=int(np.mean(self.G[indx]))
        b=int(np.mean(self.B[indx]))
        y=(r+g+b)/3.
        self.Qt_rgb=[r,g,b,y]
        R4[indx]=r; G4[indx]=g; B4[indx]=b;

        # K-Feldspar 
        indx=np.where(M==2)
        r=int(np.mean(self.R[indx]))
        g=int(np.mean(self.G[indx]))
        b=int(np.mean(self.B[indx]))
        y=(r+g+b)/3.
        self.K_rgb=[r,g,b,y]
        R4[indx]=r; G4[indx]=g; B4[indx]=b;

        # Na-Feldspar 
        indx=np.where(M==3)
        r=int(np.mean(self.R[indx]))
        g=int(np.mean(self.G[indx]))
        b=int(np.mean(self.B[indx]))
        y=(r+g+b)/3.
        self.Na_rgb=[r,g,b,y]
        R4[indx]=r; G4[indx]=g; B4[indx]=b;
        
        M4=self.IM.copy()
        M4[:,:,0]=R4
        M4[:,:,1]=G4
        M4[:,:,2]=B4
        M4img=Image.fromarray(M4)
        ax.imshow(M4img)
        ax.grid(True)

        self.M4img=M4img

if __name__=="__main__":

    #-----------RAW IMAGE---------------
    fig1=plt.figure()
    ax0=fig1.add_subplot(211)
    ax1=fig1.add_subplot(212)
    fname="g838.png"
    fname="beadless.png"
    img=IMG(fname)

    mm_pix=0.05 # length[mm]/pixel
    img.show(ax0)
    img.show_mm(ax1,mm_pix=mm_pix)

    #-----------TRIMMED IMAGE-----------
    Xa=[00,0]
    Xb=[70,35]
    img.draw_rect(ax1,Xa,Xb,clr="m")
    img.trim_mm(Xa,Xb,mm_pix=mm_pix)

    fig2=plt.figure()
    ax2=fig2.add_subplot(211)
    ax3=fig2.add_subplot(212)
    img.show(ax2)
    img.show_mm(ax3,mm_pix=mm_pix)


    fig3=plt.figure()
    ax4=fig3.add_subplot(111)
    img.img2kcell(mm_pix=mm_pix)
    ext=[0,img.N[1]*mm_pix,0,img.N[0]*mm_pix]
    ax4.imshow(img.IM,cmap="cool",extent=ext)
    ax4.set_title("Binary (0/1) Image",fontsize=14)
    ax4.grid(True)
    ax4.tick_params(labelsize=12)
    ax4.set_xlabel("x [mm]",fontsize=12)
    ax4.set_ylabel("y [mm]",fontsize=12)


    plt.show()
