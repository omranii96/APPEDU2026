import cv2, numpy as np, math, sys
from PIL import Image, ImageFilter
logo=Image.open('logo_mask.png'); A=np.array(logo)[:,:,3]
def load(f): return np.array(Image.open(f).convert('RGB')).astype(np.uint8)
def foil(w,h,c1,c2):
    g=np.linspace(0,1,w)[None,:]*0.6+np.linspace(0,1,h)[:,None]*0.4
    c1=np.array(c1);c2=np.array(c2); return (c1[None,None,:]*(1-g[...,None])+c2[None,None,:]*g[...,None]).astype(np.uint8)
def paste(img,cx,cy,width,angle,c1=(196,163,104),c2=(150,116,62),op=.92):
    s=width/A.shape[1]; a=cv2.resize(A,(int(A.shape[1]*s),int(A.shape[0]*s)),interpolation=cv2.INTER_AREA)
    h,w=a.shape; pad=int(max(h,w)*.6); a=cv2.copyMakeBorder(a,pad,pad,pad,pad,cv2.BORDER_CONSTANT,0)
    M=cv2.getRotationMatrix2D((a.shape[1]/2,a.shape[0]/2),-angle,1); a=cv2.warpAffine(a,M,(a.shape[1],a.shape[0]))
    a=cv2.GaussianBlur(a,(0,0),.45).astype(float)/255*op
    col=foil(a.shape[1],a.shape[0],c1,c2).astype(float)
    x0=int(cx-a.shape[1]/2); y0=int(cy-a.shape[0]/2)
    H,W=img.shape[:2]; xa,ya=max(0,x0),max(0,y0); xb,yb=min(W,x0+a.shape[1]),min(H,y0+a.shape[0])
    sub=img[ya:yb,xa:xb].astype(float); aa=a[ya-y0:yb-y0,xa-x0:xb-x0,None]; cc=col[ya-y0:yb-y0,xa-x0:xb-x0]
    img[ya:yb,xa:xb]=(sub*(1-aa)+cc*aa).astype(np.uint8)
def erase(img,win,thr=18,rb=22):
    x0,y0,x1,y1=win; roi=img[y0:y1,x0:x1].astype(int); g=roi.mean(2); med=np.median(g)
    m=((g<med-thr)&((roi[:,:,0]-roi[:,:,2])>rb)).astype(np.uint8)*255
    m=cv2.dilate(m,np.ones((5,5),np.uint8),iterations=2)
    full=np.zeros(img.shape[:2],np.uint8); full[y0:y1,x0:x1]=m
    ys,xs=np.nonzero(m); pts=np.stack([xs,ys],1).astype(np.float32)
    vx,vy,_,_=cv2.fitLine(pts,cv2.DIST_L2,0,.01,.01).flatten(); ang=math.degrees(math.atan2(vy,vx))
    if ang>90: ang-=180
    if ang<-90: ang+=180
    cx,cy=x0+xs.mean(),y0+ys.mean(); wdt=xs.max()-xs.min()
    out=cv2.inpaint(cv2.cvtColor(img,cv2.COLOR_RGB2BGR),full,7,cv2.INPAINT_TELEA)
    img[:]=cv2.cvtColor(out,cv2.COLOR_BGR2RGB)
    return cx,cy,wdt,ang
res={}
# Femme
im=load('f.webp')
cx,cy,w,a=erase(im,(395,280,520,345)); print('f lid',cx,cy,w,a); paste(im,cx,cy+4,w*1.35,a)
cx,cy,w,a=erase(im,(235,570,365,630)); print('f gift',cx,cy,w,a); paste(im,cx,cy+3,w*1.25,a,c1=(190,158,100),c2=(140,108,58))
Image.fromarray(im).save('out_f.jpg',quality=93)
# Homme
im=load('h.png')
cx,cy,w,a=erase(im,(425,95,540,148)); print('h lid',cx,cy,w,a); paste(im,cx,cy+3,w*1.35,a)
Image.fromarray(im).save('out_h.jpg',quality=93)
# Noel (lids are blank)
for f,cx,cy,w,a in [('noel-f.jpg',float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])),('noel-h.jpg',float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8]))]:
    im=load(f); paste(im,cx,cy,w,a); Image.fromarray(im).save('out_'+f.split('.')[0]+'.jpg',quality=93)
