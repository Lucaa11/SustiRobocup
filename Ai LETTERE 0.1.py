# Edge Impulse - OpenMV Image Classification Example

import sensor, image, time, os, tf, uos, gc

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

nero = (31, 0, 125, -51, 127, -4)
thresholds = [nero]
net = None
labels = None

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=100, area_threshold=1000, merge=True):
        if blob.code() == 1:
            #print('PRESENTE QUALCOSA DI NERO')
            for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
                img.draw_rectangle(obj.rect())
                predictions_list = list(zip(labels, obj.output()))
                if (predictions_list[0][1]> 0.85 ):
                    print( (predictions_list[0][1]))
                    print('Lettera H')
                elif (predictions_list[1][1]> 0.85 ):
                    print( (predictions_list[1][1]))
                    print('Lettera S')
                elif (predictions_list[2][1]> 0.85 ):
                    print( (predictions_list[2][1]))
                    print('Lettera U')



#for i in range(len(predictions_list)):
   # print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))

