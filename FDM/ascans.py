#!/home/kazushi/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt

nfiles=90;
nums=range(0,nfiles);

fig=plt.figure();
ax1=fig.add_subplot(2,1,1);
ax2=fig.add_subplot(2,1,2);
AMP=np.array([]);
for k in nums:
	fname="inwv"+str(k)+".dat";
	print(fname)
	fp=open(fname,"r");

	for m in range(3): fp.readline();
	
	Nt=int(fp.readline().lstrip());

	for m in range(5): fp.readline();
	tmp=fp.readline().lstrip().split(" ");
	(t1,t2)=list(map(float,tmp));
	fp.readline();

	amp=fp.readlines();

	amp=np.array(list(map(float,amp)));
	tt=np.linspace(t1,t2,Nt);

	fp.close();

	ax1.plot(tt,amp,'k-')
	AMP=np.append(AMP,amp)
	

AMP=np.reshape(AMP,(nfiles,Nt))
ext=[t1,t2,nfiles,0];
ax2.imshow(AMP,extent=ext)
ax1.grid(True)
plt.show();

