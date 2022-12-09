#Importo las librerias que voy a utilizar.
import cv2
import os
import sys
import json

def VideoCapture(videoPath):
    if os.path.isfile(videoPath): #Pregunto si existe el archivo de video
        VideoCapture.cap = cv2.VideoCapture(videoPath) #Creo el objeto de captura de videos para leerlo

        success, VideoCapture.frame = VideoCapture.cap.read() #Leo una trama
        if not success: #si falla al leer el video cierro el programa
            print('Fallo al leer video')
            sys.exit(1) #Cierro programa

        fps = VideoCapture.cap.get(cv2.CAP_PROP_FPS) #Leo los FPS del video
        frame_width = int(VideoCapture.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #Obtengo la resolución de ancho
        print("El ancho del video es: " + str(frame_width))
        frame_height = int(VideoCapture.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #Obtengo la resolución de alto
        print("El alto del video es: " + str(frame_height))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Eligo el formato del video de salida
        VideoCapture.writer = cv2.VideoWriter("development_assets/output.mp4", fourcc, fps, (frame_width, frame_height))#Creo el objeto de video de salida
    else:
        print("falta archivo de video")
        sys.exit(1) #Sino cierro programa

def JSONCapture(jsonPath):
    JSONCapture.bboxes = [] #Aquí almaceno las coordenadas de los objetos a realizar el tracking.

    if os.path.isfile(jsonPath): #Pregunto si existe el archivo JSON
        f = open(jsonPath) #Abro el archivo
        JSONCapture.data = json.load(f) #Lo cargo en una lista
        for i in range(len(JSONCapture.data)): #Con un condicional for voy iterando en cada valor de data
            #print(data[i]['coordinates']) Aquí había agregado un print para saber cuales son las coordenadas x,y,w,h
            JSONCapture.bboxes.append(tuple(JSONCapture.data[i]['coordinates'])) #Agrego cada terna de coordenadas como tupla en la lista vacia
            print("Las coordenadas para el id " + i + " son:" + str(tuple(JSONCapture.data[i]['coordinates'])))
        f.close() #cierro el archivo

    else:
        print("falta archivo de JSON")
        sys.exit(1) #Sino cierro programa

def TrackingObject():
    VideoCapture(videoPath)
    JSONCapture(jsonPath)
        
    multiTracker = cv2.MultiTracker_create() # Creo el objeto MultiTracker

        # Inicializo MultiTracker. Uso como Tracking individual el método MOSSE (Minimum Output Sum of Squared Error)
    for bbox in JSONCapture.bboxes: #itero sobre cada conjunto de coordenadas
        multiTracker.add(cv2.TrackerMOSSE_create(), VideoCapture.frame, bbox)

    color = (255, 0, 0) #Este va a ser el color de los bounding boxes. Es azul

    while VideoCapture.cap.isOpened(): #Mientras se estan capturando las tramas del video
        success, frame = VideoCapture.cap.read() #Voy leyendo cada trama y la variable Success indica en valor booleano si existe.
        if not success:
            break

        success, boxes = multiTracker.update(frame) #voy actualizando las coordenadas de localización de los objetos de los siguientes frames.

        for i, newbox in enumerate(boxes): #Voy graficando los bounding boxes.
            p1 = (int(newbox[0]), int(newbox[1])) #esquina inferior de cada recuadro
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3])) #esquina superior de cada recuadro
            id_box = str(JSONCapture.data[i]['id']
            print("Para el ID: " + id_box)
            print("Los punto son: ")
            print(str(list((p1,p2))))
            cv2.rectangle(frame, p1, p2, color, 2, 1) #Voy dibujando los rectangulos
            cv2.putText(frame, id_box), 
                        (int(newbox[0])+30,int(newbox[1])+30), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,0),2)
            #agrego también como texto el id de cada bounding box y se vaya moviendo a medida que se actualiza.

            #cv2.imshow(frame) #Con esto podría ir viendo cada frame pero como hacía el proceso mas pesado lo comente
        VideoCapture.writer.write(frame) #Esto permite guardar cada frame en el nuevo video.
                  
    VideoCapture.cap.release()
    VideoCapture.writer.release()

videoPath = "development_assets/input.mkv"
jsonPath = "development_assets/initial_conditions.json"

TrackingObject()