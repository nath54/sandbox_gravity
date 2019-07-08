#coding:utf-8
#!/bin/python3
import random,math,pygame,time
from pygame.locals import *

tex,tey=1000,800
pygame.init()
fenetre=pygame.display.set_mode([tex,tey])
pygame.key.set_repeat(40,30)
font=pygame.font.SysFont("Serif",15)
cam=[0,0]

mats=[["eau",997,(0,50,150),None],["bois sapin",450,(43,30,8),None] , ["acier",7850,(150,150,150),None] , ["or",19300,(88,78,10),None] , ["bronze",8800,(27,18,3),None] , ["argent",10500,(185,185,185),None],["Soleil",1410,(250,250,0),"images/Soleil.png"],["Terre",5510,(100,100,200),"images/Terre.png"],["trou noir",135740000,(20,20,20),None]]
#0=nom , 1=masse volumique , 2=couleur , 3=image

cg=6.67408*10**-11

class Objet:
    def __init__(self,x,y,t,m,vix,viy):
        self.px=x
        self.py=y
        self.ray=t
        self.mat=m
        self.aire=math.pi*math.pow(self.ray,2)
        self.masse=m[1]*self.aire
        self.cl=m[2]
        self.rect=pygame.draw.circle(fenetre,self.cl,(self.px,self.py),self.ray,0)
        self.vitx=vix
        self.vity=viy
        self.image=None
        self.traces=[]
        if m[3]!=None:
            self.image=pygame.transform.scale(pygame.image.load(m[3]),[self.ray*2,self.ray*2])

def aff(objs,msel,tcurs,poscurs,fps,dc,pause,cam,objsel,activtraces):
    fenetre.fill((0,0,0))
    noa=0
    for o in objs:
        if o.image==None: o.rect=pygame.draw.circle(fenetre,o.cl,(cam[0]+int(o.px),cam[1]+int(o.py)),o.ray,0)
        else: o.rect=fenetre.blit(o.image,[cam[0]+int(o.px-o.ray),cam[1]+int(o.py-o.ray)])
        if o.rect.collidepoint(poscurs):
            fenetre.blit(font.render("objet : pos : "+str(int(o.px))+" , "+str(int(o.py))+"  mat : "+o.mat[0]+" masse : "+str(o.masse/1000)+"kg aire : "+str(o.aire)+"px²",15,(255,255,255)),[15,110+15*noa])
            noa+=1
        if activtraces:
            for t in o.traces:
                tx,ty=cam[0]+t[0],cam[1]+t[1]
                if tx>=0 and tx<tex and ty >= 0 and ty < tey: pygame.draw.rect(fenetre,o.cl,(tx,ty,1,1),0)
    if dc!=None:
        pygame.draw.line(fenetre,(0,0,255),dc,pos,2)
    pygame.draw.circle(fenetre,(0,0,255),(poscurs[0],poscurs[1]),tcurs,1)
    fenetre.blit(font.render("matiere sel : "+mats[msel][0],15,(255,255,255)),[15,50])
    fenetre.blit(font.render(str(fps)+" fps",15,(255,255,255)),[15,15])
    fenetre.blit(font.render("nb objs : "+str(len(objs)),15,(255,255,255)),[15,90])
    if pause: fenetre.blit(font.render("PAUSE",15,(255,185,0)),[505,15])
    if activtraces: fenetre.blit(font.render("traces",15,(0,185,85)),[805,15])
    if objsel!=None: fenetre.blit(font.render("objsel = "+str(objs[objsel]),15,(255,185,0)),[505,45])
    pygame.display.update()

def grav(objs,pause,activtraces):
    if not pause:
        for o in objs:
            for oo in objs:
                if o!=oo and (o.px!=oo.px or o.py!=oo.py):
                    fg=(cg*o.masse*oo.masse)/math.pow(math.sqrt(math.pow(o.px-oo.px,2)+math.pow(o.py-oo.py,2)),2)
                    #fg/=o.masse
                    v=fg
                    a=oo.px-o.px
                    b=oo.py-o.py
                    c=math.sqrt(a*a+b*b)
                    if c<=v:
                        o.px=oo.px
                        o.py=oo.py
                    else:
                        e=(b*v)/c
                        d=(a*v)/c
                        o.vitx+=d
                        o.vity+=e
        for o in objs:
            o.px+=o.vitx
            o.py+=o.vity
            if activtraces: o.traces.append([o.px,o.py])

objs=[]
objsel=None
tcurs=10
fps=0
msel=0
activtraces=True

dc=None
pause=False
encour=True
vitcam=10
tpa=0.5
while encour:
    t1=time.time()
    pos=pygame.mouse.get_pos()
    grav(objs,pause,activtraces)
    if objsel!=None:
        cam=[int(tex/2-objs[objsel].px),int(tey/2-objs[objsel].py)]
    aff(objs,msel,tcurs,pos,fps,dc,pause,cam,objsel,activtraces)
    for event in pygame.event.get():
        if event.type==QUIT: exit()
        elif event.type==KEYDOWN:
            if event.key==K_q: exit()
            elif event.key==K_SPACE:
                pause=not pause
                time.sleep(tpa)
            elif event.key==K_BACKSPACE:
                objs=[]
                objsel=None
            elif event.key==K_UP: cam[1]+=vitcam
            elif event.key==K_DOWN: cam[1]-=vitcam
            elif event.key==K_LEFT: cam[0]+=vitcam
            elif event.key==K_RIGHT: cam[0]-=vitcam
            elif event.key==K_PAGEUP:
                if objsel==None and objs!=[]:
                    objsel=0
                else:
                    objsel+=1
                    if objsel>=len(objs): objsel=None
                time.sleep(tpa)
            elif event.key==K_PAGEDOWN:
                if objsel==None and objs!=[]:
                    objsel=len(objs)-1
                else:
                    objsel-=1
                    if objsel<0: objsel=None
                time.sleep(tpa)
            elif event.key==K_t:
                activtraces=not activtraces
                for o in objs: o.traces=[]
                time.sleep(tpa)
        if event.type==MOUSEBUTTONDOWN:
            dc=pos
        if event.type==MOUSEBUTTONUP:
            if event.button==1:
                avitx=(pos[0]-dc[0])/100
                avity=(pos[1]-dc[1])/100
                objs.append( Objet(-cam[0]+pos[0],-cam[1]+pos[1],tcurs,mats[msel],avitx,avity) )
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











