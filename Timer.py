from tkinter import *
import time

class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        #
        self._elapsedtime = 0.0 #
        self._running = 0 #
        self.makeWidgets()
        
    def makeWidgets(self):
        global timeLabel
        timeLabel = Label(self, text=f'Time elapsed: {int(self._elapsedtime)}')
        timeLabel.grid(row=0, column=0)
   
    def _update(self): #
        """ Update the label with elapsed time. """ 
        global timeLabel
        self._elapsedtime = time.time() - self._start
        self._timer = self.after(500, self._update)
        timeLabel.config(text=f'Time elapsed: {int(self._elapsedtime)}')
        
    
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._running = 0
