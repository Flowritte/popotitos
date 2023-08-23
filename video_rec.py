import RPi.GPIO as gp
import numpy as np
import cv2 as cv
import time
import random
import telebot


"""time.strftime("%H-%M")"""
"""f=time.strftime("%y-%m-%d")"""
"""num=(str(random.randrange(1,100)))"""

name_c='cam-1_jarra.avi'
name_c1='cam-2_desp.avi'

print('Bienvenido a EMVECO MONITOR....Espere')
time.sleep(1) and time.sleep(0.01)
print('Abriendo sistema')
def gpi_on():

    gp.setmode(gp.BOARD)
    gp.setup(40,gp.IN)
    
    #if gp.input(31) is True:
     #   pass
    
    
    c=0
    print('precione boton')
    while True:
        if gp.input(40):
            c=c+1
            print("boton presionado" +" "+ str(c) +" "+ "veces")
            #time.sleep(0.5)
            print("Abriendo sistema")
            print("")
            time.sleep(0.5)
            cap0=cv.VideoCapture(0)
            cap1=cv.VideoCapture(2)
            fourcc0=cv.VideoWriter_fourcc(*'XVID')
            fourcc1=cv.VideoWriter_fourcc(*'XVID')
            size1=(int(cap0.get(3)),int(cap0.get(4)))
            size2=(int(cap1.get(3)),int(cap1.get(4)))
            out0=cv.VideoWriter(name_c,fourcc0,7.65,(size1))
            out1=cv.VideoWriter(name_c1,fourcc1,7.65,(size2))
            #print('la mamalona')
            while cap0.isOpened():
                
                ret,frame0=cap0.read()
                ret,frame1=cap1.read()                
                frame0=cv.flip(frame0,1)
                frame1=cv.flip(frame1,1)
                out0.write(frame0)
                out1.write(frame1)
                cv.imshow("Camara Jarra Medidora",frame0)
                cv.imshow("Camara Despachador",frame1)
                cv.moveWindow('Camara Jarra Medidora', 650, 430)
                cv.moveWindow('Camara Despachador', 4, 20)
                
               
                if not ret:
                    print("Una o dos Camaras no estan conectadas..Error 102")
                    break
                
                if cv.waitKey(1)==ord('q') or gp.input(40):
                    c=c+1
                    time.sleep(1)
                    break
            cap0.release()
            out0.release()
            cap1.release()
            out1.release()
            cv.destroyAllWindows()
            continue   
        
        if c==2:
            print('Cerrando sistema')
            c=0
            break
    
gpi_on()

def bot():
    

    tele_k='5429802685:AAEnPXzvZlvBFG8YfPArXz2NEKPD7H18Nu8' #token exclusivo del bot creado por botfather de telegram

    
    bot=telebot.TeleBot(tele_k)


    @bot.message_handler(commands=["start","video"])
    def cmd_start(message):   
    
        bot.reply_to(message,'Hola!,vamos a empezar.!')


    @bot.message_handler(content_types=["text"])
    def bot_mss_text(message):
        h=time.strftime("%H-%M")
        f=time.strftime("%y-%m-%d")
        archivo=open("cam-1_jarra.avi","rb")
        bot.send_video(message.chat.id, archivo, caption=h +" "+ f+" "+"Camara De La Jarra Volumetrica")
        time.sleep(0.5)
        archivo=open("cam-2_desp.avi","rb")
        bot.send_video(message.chat.id, archivo, caption=h +" "+ f+" "+ "Camara Del despachador")
        
        #main##############
    if __name__=='__main__':
        print('hola...Iniciando,bot')
        bot.infinity_polling()   
        print('fin')
    
bot()    