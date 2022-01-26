import numpy as np
import matplotlib.pyplot as plt


fp=open("g822_kcell.dat","r")

fp.readline()
dat=fp.readline()
dat=dat.split(",")
W=dat[0]
H=dat[1]

fp.readline()
dat=fp.readline()
dat=dat.split(",")
Nx=int(dat[0])
Ny=int(dat[1])
fp.readline()
K=[]
for row in fp:
    K.append(int(row))

K=np.array(K)

K=np.reshape(K,[Nx,Ny])
K=np.transpose(K)

fig=plt.figure()
ax=fig.add_subplot(111)

mm_pix=0.08
mm_pix=0.05

ext=[0,mm_pix*Nx,0,mm_pix*Ny]
ax.imshow(K,origin="lower",extent=ext)

ax.set_xlabel("x [mm]",fontsize=12)
ax.set_ylabel("y [mm]",fontsize=12)
ax.tick_params(labelsize=12)


print(Nx,Ny)

plt.show()
