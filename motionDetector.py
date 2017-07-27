# import cv2.cv as cv
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
#import imutils
import video
import os

# import copy
os.getcwd()
# Change all CV to CV2

debug = True
debug_print = False
ceil = 40
gauss = 7
erode = 18
dilate = 18
threshold = 20

start_from_frame = 10
end_frame = 100  # el frame donde va a terminar
nth_frame = 1  # read every 5 frames
percentage_of_mov = 45 # si hay mas de 30 porciento, entonces es un video que se queda

# TODO: Verificar nth_frame no sea mayor que la duracion total del video,
# TODO: Sacar la version profesional
# TODO: CLION
# TODO: Poner las variables en un archivo,




class MotionDetectorContour:

    def __init__(self, ceil=ceil, videoPath=None, video=None):
        self.ceil = ceil
        self.end_frame = end_frame
        # self.capture = imutils.getCamera(videoPath)
        # Todo: Recibir un objeto de la clase Video y con eso tengo y ahi tengo la propiedad,
        # Todo: Metodo estatico, tiene que tener un decorador, que se llama class Method.
       # self.capture = imutils.getCamera('sampleVideos/basura1.mp4')
      #  self.video = video
        self.capture = video

    def run(self):
        '''Detect movement and return True and the frame, otherwise return False and total number of frames checked '''
        grabbed, frame = self.capture.read()
        self.capture.set(1, start_from_frame);  # Where frame_no is the frame you want
        total_Frames = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        print total_Frames

        if nth_frame > 1:
            self.ceil *= nth_frame * 0.65
        if self.end_frame > total_Frames:
            self.end_frame = total_Frames;
            #print "Se cambio"
        try:
            dimensions = frame.shape
            height = dimensions[0]
            width = dimensions[1]
            surface = width * height  # Surface area of the image
            cursurface = 0  # Hold the current surface that have changed
            frame_counter = 0  # A counter for frames read
        except:
            return (0,0,0,0,0,True)

        moving_average = np.float32(frame)
        difference = None
        analyzed_frames = 0;
        frames_with_motion = 0;
        while True:
            try:
                frame_counter += 1
              #  print frame_counter
                grabbed, color_image = self.capture.read()

                if frame_counter >= end_frame :
                    # se han procesado todos los frames requeridos.
                   # print "Termine"
                    break;
                if frame_counter % nth_frame == 0:  #
                    analyzed_frames += 1
                    color_image = cv2.GaussianBlur(color_image, (gauss, gauss), 0)
                    if difference is None:  # For the first time put values in difference, temp and moving_average hhh
                        cv2.convertScaleAbs(color_image, moving_average, 1.0, 0.0)
                    else:
                        cv2.accumulateWeighted(color_image, moving_average, 0.020)  # Compute the average

                    # Convert the scale of the moving average.
                    temp = cv2.convertScaleAbs(moving_average)

                    # Minus the current frame from the moving average.
                    difference = cv2.absdiff(color_image, temp)

                    gray_image = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                    ret, gray_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

                    gray_image = cv2.dilate(gray_image, None, dilate)  # to get object blobs
                    gray_image = cv2.erode(gray_image, None, erode)

                    # Find contours
                    contours, hierarchy = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    # print contours
                    for h, contour in enumerate(contours):
                        cursurface += cv2.contourArea(contour)

                    avg = (cursurface * 100) / surface  # Calculate the average of contour area on the total size
                    if avg > self.ceil:
                        frames_with_motion += 1
                    cursurface = 0  # Put back the current surface to 0
            except:
                #termino de procesar los frames
                break
        percentage = (frames_with_motion * 100.0) / analyzed_frames
        result = True
        if(percentage>percentage_of_mov):
            result = False
        #Todo: Regresar un arreglo con la informacion,
        #print "Total frames: %s, analyzed_frames: %s, frames_with_motion: %s, percentage of movement: %s, Minimum percentage allowed: %s,  delete it?: %s " % (str(frame_counter),str(analyzed_frames),str(frames_with_motion),str(percentage),str(percentage_of_mov),str(result))
       # return result

        return (total_Frames, analyzed_frames,frames_with_motion,percentage,percentage_of_mov,result)


if __name__ == "__main__":
    t = MotionDetectorContour()
    print t.run()
