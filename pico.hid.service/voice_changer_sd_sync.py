import threading
import time
import sounddevice as sd
import numpy as np
import scipy.fftpack as fft
from pysndfx import AudioEffectsChain
from queue import Queue


fx = (
    AudioEffectsChain()
    #.highshelf()
    .pitch(100)
    # .vol(12, "dB", limiter_gain=0.5)
    # .upsample(2)
    # .equalizer(550)
    # .reverb(room_scale=50, wet_gain=-5)
    #.phaser()
    #.delay()
    .speed(0.75)
    .vol(12, "dB", limiter_gain=0.5)
    # .compand()
    #.lowshelf()
    #.normalize()
)

class OutputStreamThread(threading.Thread):
    def __init__(self, queue, output_device=sd.default.device[1], *args, **kwargs):
        self.queue = queue
        self.os = sd.OutputStream(device=output_device, samplerate=48000, channels=1)  
        self._isRunning = True
        super().__init__(*args, **kwargs)

    def run(self):
        self.os.start()
        while self._isRunning:
            if self.queue.not_empty:
                self.os.write(self.queue.get())

    def stop(self):
        self._isRunning = False
        self.os.stop()
    
class InputStreamThread(threading.Thread):
    def __init__(self, main_queue, monitoring_queue, fx, *args, **kwargs):
        self.main_queue = main_queue
        self.monitoring_queue = monitoring_queue
        self.fx = fx
        self._isRunning = True
        super().__init__(*args, **kwargs)

    def run(self):
        with sd.InputStream(samplerate=48000, blocksize = 4096, channels=1, callback=self.input_callback):
            while self._isRunning:
                sd.sleep(1)

    def stop(self):
        with self.main_queue.mutex:
            self.main_queue.queue.clear()
        with self.monitoring_queue.mutex:
            self.monitoring_queue.queue.clear()
        self._isRunning = False

    def filter_low_vol_values(self, data, lowerThresh=-1.0e-3, higherThresh=1.0e-3):
        return data[(lowerThresh > data) | (data > higherThresh)]

    def input_callback(self,indata, frames, time, status):
        if status:
            print(status)
        
        if not self._isRunning:
            raise Exception("thread is exiting")
        
        if self.fx is not None:
            output = self.applyEffects(indata.reshape(2,int(indata.shape[0]/2)))
            output = output.reshape([int(output.shape[1]*2),1])
            # output_before = len(output)
            output = self.filter_low_vol_values(output)
            # print(f"output before: {output_before}, output after: {len(output)}, queue length: {self.main_queue.qsize()}\r")
            self.main_queue.put(output)
            self.monitoring_queue.put(output)
        else:
            self.main_queue.put(indata)
            self.monitoring_queue.put(indata)

    def applyEffects(self, data):
        return self.fx(data)

class VoiceChanger(threading.Thread):
    def __init__(self, input_device, output_device, monitoring_device=None):
        self.queue = Queue()
        self.monitoring_queue = Queue()
        sd.default.device = (input_device, output_device)
        self.monitoring_device = monitoring_device

        self.inputStream = None
        self.outputStream = None
        self.monitoringStream = None



        self.setEffect()



    def setEffect(self, effect = None):
        self.effect = effect
        self.setupStreamingThreads()
        
    def setupStreamingThreads(self):
        if(self.outputStream is not None):
            self.outputStream.stop()
        if(self.monitoringStream is not None):
            self.monitoringStream.stop()
        if(self.inputStream is not None):
            self.inputStream.stop()
        self.inputStream = InputStreamThread(self.queue, self.monitoring_queue, self.effect)
        self.outputStream = OutputStreamThread(self.queue)
        if self.monitoring_device is not None:
            self.monitoringStream = OutputStreamThread(self.monitoring_queue, self.monitoring_device)
            self.monitoringStream.start()
        self.outputStream.start()
        self.inputStream.start()


print(sd.query_devices())

vc = VoiceChanger(1, 5, 10)

time.sleep(10)

vc.setEffect(fx)

time.sleep(10)
