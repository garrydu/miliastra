from random import randint
from p44 import p44

def gen(width=8, height=8):
    vis=[0]*(width*height+10)
    wall=[1]*(width*height+10)
    ds=[-1,1,width,-width]
    p0=0
    stack=[p44[randint(0,23)]]
    while (len(stack)>0):
        val=stack.pop()
        p=val //1000
        dirs=
    
    
    



