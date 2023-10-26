import cv2
import imutils
from datetime import datetime
from facepplib import FacePP, exceptions

faceCascade = cv2.CascadeClassifier("cascade/haarcascade_frontalface_default.xml")
data = str((datetime.now().strftime("%Y-%m-%d_%H_%M_%S")))

face_detection=""
faceset_initialize=""
face_search=""
face_landmarks=""
dense_facial_landmarks=""
face_attributes=""
beauty_score_and_emotion_recognition=""

def verifica(app):
        with open('banco/nomes.dat', 'r') as file:
            for line in file:
                pass
            last_img2 = line 

        with open('banco/matricula.dat', 'r') as file:
            for line in file:
                pass
            last_img1 = line 

        img1 = f'banco/{last_img1}'
        img2 = f'static/tentativas/{last_img2}'
        cmp_ = app.compare.get(image_file1=img1,image_file2=img2)
        confidence = cmp_.confidence

        while True:
            img_identifica = cv2.imread(img2)
            img_identifica = imutils.resize(img_identifica, width=950)

            faces = faceCascade.detectMultiScale(img_identifica, scaleFactor=1.1, minNeighbors=8, minSize=(25, 25))                                  

            for (x, y, w, h) in faces:
                cv2.rectangle(img_identifica, (x, y), (x + w, y + h), (255, 255, 0), 2)
                contador = str(faces.shape[0])
                if contador > '1':
                    print('Mais de um rosto detectado')
                
            if confidence > 80:
                result = True
                result = str(result)             
                print('acesso autorizado')   
                with open('banco/result.dat', 'w') as file:
                    file.write(result)
                return False
            
            else:
                result = False
                result = str(result)  
                print('acesso não autorizado')   
                with open('banco/result.dat', 'w') as file:
                    file.write(result)
                return False

if __name__ == '__main__':

    api_key ='xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
    api_secret ='TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'

    try:
        app_ = FacePP(api_key=api_key, api_secret=api_secret)
        funcs = [
            face_detection,
            verifica,
            faceset_initialize,
            face_search,
            face_landmarks,
            dense_facial_landmarks,
            face_attributes,
            beauty_score_and_emotion_recognition
        ]
        verifica(app_)

    except exceptions.BaseFacePPError as error:
        with open('log/log.dat', 'a') as file:
            file.write(f"{data} \n log de FacePP\n {error} \n\n------------------------------------------------------------------------------\n\n")
        verifica(app_)
        

cv2.destroyAllWindows()