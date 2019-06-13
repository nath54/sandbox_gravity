#coding:utf-8
import random,math,pygame,time
from pygame.locals import *

tex,tey=1000,800
pygame.init()
fenetre=pygame.display.set_mode([tex,tey])
pygame.key.set_repeat(40,30)
font=pygame.font.SysFont("Serif",15)

mats=[["bois sapin",450,(43,30,8)] , ["acier",7850,(150,150,150)] , ["or",19300,(88,78,10)] , ["bronze",8800,(27,18,3)] , ["argent",10500,(185,185,185)],["trou noir",1.3574*10**8,(20,20,20)]]
#0=nom , 1=masse volumique , 2=couleur

cg=6.67408*10**-11

class Objet:
    def __init__(self,x,y,t,m,vitx,vity):
        self.px=x
        self.py=y
        self.ray=t
        self.mat=m
        self.aire=math.pi*math.pow(self.ray,2)
        self.masse=m[1]*self.aire
        self.cl=m[2]
        self.rect=pygame.draw.circle(fenetre,self.cl,(self.px,self.py),self.ray,0)
        self.vitx=vitx
        self.vity=vity

def aff(objs,msel,tcurs,poscurs,fps,dc):
    fenetre.fill((0,0,0))
    noa=0
    for o in objs:
        o.rect=pygame.draw.circle(fenetre,o.cl,(int(o.px),int(o.py)),o.ray,0)
        if o.rect.collidepoint(poscurs):
            fenetre.blit(font.render("objet : mat : "+o.mat[0]+" masse : "+str(o.masse)+"g aire : "+str(o.aire)+"px²",15,(255,255,255)),[15,70+15*noa])
            noa+=1
    if dc!=None:
        pygame.draw.line(fenetre,(0,0,255),dc,pos,2)
    pygame.draw.circle(fenetre,(0,0,255),(poscurs[0],poscurs[1]),tcurs,1)
    fenetre.blit(font.render("matiere sel : "+mats[msel][0],15,(255,255,255)),[15,50])
    fenetre.blit(font.render(str(fps)+" fps",15,(255,255,255)),[15,15])
    pygame.display.update()

def grav(objs):
    for o in objs:
        o.px+=vitx
        o.py+=vity
    for o in objs:
        for oo in objs:
            if o!=oo and (o.px!=oo.px or o.py!=oo.py):
                fg=(cg*o.masse*oo.masse)/math.pow(math.sqrt(math.pow(o.px-oo.px,2)+math.pow(o.py-oo.py,2)),2)
                v=fg
                a=oo.px-o.px
                b=oo.py-o.py
                c=math.sqrt(a*a+b*b)
                if v>=c:
                    o.px=oo.px
                    o.py=oo.py
                else:
                    e=(b*v)/c
                    d=(a*v)/c
                    o.px+=d
                    o.py+=e
    """
    otd=[]
    for o in objs:
        for oo in objs:
            if o!=oo:
                if o.px==oo.px and o.py==oo.py:
                    if o.masse>oo.masse:
                        otd.append(oo)
                        o.masse+=oo.masse
                    else:
                        otd.append(o)
                        oo.masse+=o.masse
    for o in otd:
        if o in objs:
            del(objs[objs.index(o)])
    """

objs=[]
tcurs=10
fps=0
msel=0

dc=None

encour=True
while encour:
    t1=time.time()
    pos=pygame.mouse.get_pos()
    grav(objs)
    aff(objs,msel,tcurs,pos,fps,dc)
    for event in pygame.event.get():
        if event.type==QUIT: exit()
        elif event.type==KEYDOWN:
            if event.key==K_q: exit()
        if event.type==MOUSEBUTTONDOWN:
            dc=pos
        if event.type==MOUSEBUTTONUP:
            if event.button==1:
                vitx=(pos[0]-dc[0])/100
                vity=(pos[1]-dc[1])/100
                objs.append( Objet(pos[0],pos[1],tcurs,mats[msel],vitx,vity) )
            if event.button==3:
                msel+=1
                if msel >= len(mats): msel=0
            if event.button==4:
                if tcurs<150: tcurs+=1
            if event.button==5:
                if tcurs>1: tcurs-=1
            dc=None
    t2=time.time()
    fps=int(1.0/(t2-t1))










