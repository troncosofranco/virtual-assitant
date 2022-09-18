import  speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, colores, os
from pygame import mixer

name = 'Negri'
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

sites= {
    'google':'google.com',
    'youtube':'youtube.com',
    'facebook':'facebook.com',
    'whatsapp':'web.whatsapp.com',
    'infobae':'infobae.com'
}

files = {
    'Python': 'Python.doc',
    'Cryptotrading':'Cryptotrading.doc'
}

def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
            with sr.Microphone() as source:
                print('Escuchando...')
                pc = listener.listen(source)
                rec = listener.recognize_google(pc, language='es')
                rec = rec.lower()
                if name in rec:
                   rec = rec.replace(name, '') 

    except:
        pass
    return rec


def run_negri():
    while True:  
        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '') 
            print('Reproduciendo ' + music)
            talk('Reproduciendo ' + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca','')
            wikipedia.set_lang('es')
            wiki = wikipedia.summary(search, 1)
            print(search +': ' + wiki)
            talk(wiki)
        elif 'alarma' in rec:
            num = rec.replace('alarma', '')
            num = num.strip()
            talk('Alarma activada a las ') + num + ' horas'
            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print('DESPIERTA!!!')
                    mixer.init()
                    mixer.music.locad('auronplay-alarma.mp3')
                    mixer.music.play()
                    if keyboard.read_key() == 's':
                        mixer.music.stop()
                        break
        elif 'colores' in rec:
            talk('Enseguida')
            colores.capture()
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'star chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open('nota.txt', 'a') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open('nota.text', 'w')
                write(file)
        elif 'termina' in rec:
            talk('Adios!')
            break

def write(f):
    talk('¿Qué quieres que escriba?')
    rec_write = listen()
    f.write(rec_write + os.linesep)              
    f.close()
    talk('Listo, puedes revisarlo')
    sub.Popen('nota.text', shell=True)
if __name__ == '__main__':
   run_negri() 
