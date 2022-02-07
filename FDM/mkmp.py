import cv2

nfile=input("Number of files?")
nfile=int(nfile)
img_array=[]
for k in range(nfile):
    fname=str(k+1)+".png"
    img=cv2.imread(fname)
    height,width,layers=img.shape
    size=(width,height)

    img_array.append(img)

name="snaps.mp4"
out=cv2.VideoWriter(name,cv2.VideoWriter_fourcc(*'MP4V'),3.0,size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
