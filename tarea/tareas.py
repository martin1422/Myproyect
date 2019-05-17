# -*- coding: utf-8 -*-
#!/usr/bin/python2.7.13

import time
from threading import Thread
from variables import var as vg


class Timer1(Thread):
    over=False
    pause=False
    def __init__(self,func):
        Thread.__init__(self)
        self.func=func
        #self.setDaemon(True)
    def run(self):
        global t,root
        time.sleep(5)
        finish=False
        while not self.over and not finish:
            if not self.pause:
                finish=self.func()
            time.sleep(5)
        if finish:
            #root.focus_force()
            root.event_generate('<<pop>>',when='tail')
        t=None
    def kill(self): self.over=True
    def paus(self): self.pause=True
    def cont(self): self.pause=False



class Timer(Thread):
    over=False
    pause=False
    def __init__(self,func):
        Thread.__init__(self)
        self.func=func
        #self.setDaemon(True)
    def run(self):
        global t,root
        time.sleep(1)
        finish=False
        while not self.over and not finish:
            if not self.pause:
                finish=self.func()
            time.sleep(1)
        if finish:
            #root.focus_force()
            root.event_generate('<<pop>>',when='tail')
        t=None
    def kill(self): self.over=True
    def paus(self): self.pause=True
    def cont(self): self.pause=False