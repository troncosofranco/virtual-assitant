import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import colores
import os
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
import threading as tr
import whatsapp as whapp
import browser 
import database
from chatterbot import ChatBot
from chatterbot import preprocessors
from chatterbot.trainers import ListTrainer
import face_recognizer as fr

main_window= Tk()
main_window.title('Helena AI')

main_window.geometry('800x500')
main_window.resizable(0,0) #la ventana no se puede aumentar
main_window.configure(bg='#02AAB0')

comandos="""
    Comandos:
    - Reproduce...(canción)
    - Busca... (algo)
    - Abre... (website o app)
    - Alarma... (hora en 24H)
    - Escribe...(texto)
    - Archivo...(nombre)
    - Colores (rojo, amarillo)
    - Mensaje... (contacto)
    - Cierra... (programa)
    - Termina o ciérrate
"""

label_title = Label(main_window, text= 'Negri AI', bg='#FFFDE4',fg='#005AA7', font=('Arial', 30,'bold'))
label_title.pack(pady=10)

negri_photo = ImageTk.PhotoImage(Image.open('photo_AI.jpg'))
window_photo = Label(main_window, image=negri_photo)
window_photo.pack(pady=5)

canvas_comandos = Canvas(bg='#3a7bd5', width= 180, height = 170)
canvas_comandos.place(x=85, y=80)
canvas_comandos.create_text(90,80, text=comandos, fill='white', font='Arial 10 bold')

text_info = Text(main_window, bg='#F6EAD9', fg='black')
text_info.place(x=85, y=245, width=183, height= 190)



def mexican_voice():
    change_voice(0)
def english_voice():
    change_voice(1)
def change_voice(id):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk('Hola, soy Helena, ¿En qué puedo servirte?')


name = 'Negri'
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(',')
                val = val.rstrip('\n')
                name_dict[key] = val
    except FileNotFoundError as e:
        pass

#Diccionarios
sites = dict()
charge_data(sites, 'pages.txt')
files = dict()
charge_data(files, 'archivos.txt')
programs = dict()
charge_data(programs, 'apps.txt')
contacts = dict()
charge_data(contacts, 'apps.txt')

def talk(text):
    engine.say(text)
    engine.runAndWait()

def read_and_talk():
    text = text_info.get('1.0', 'end')
    talk(text)

def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

def listen(phrase=None):
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk(phrase)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language='es')
        rec = rec.lower()
    except sr.UnknownValueError:
       print('No te entendí, intenta de nuevo')
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.formar(e))
    return rec

#Funciones asociadas a las palabras claves

def reproduce(rec):
    music = rec.replace('reproduce', '')
    print('Reproduciendo ' + music)
    talk('Reproduciendo ' + music)
    pywhatkit.playonyt(music)

def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang('es')
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ': ' + wiki)

def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start(rec)

def colores(rec):
    talk('Enseguida')
    t = tr.Thread(target=colores.capture)
    t.start()

def abre(rec):
    task = rec.replace('abre','').strip()
    
    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'star chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
       
    elif task in programs:
        for task in programs:
            if task in rec:
                talk(f'Abriendo {task}')
                os.startfile(programs[task])
    else:
        talk('Lo siento, no se ha encontrado, usa los botones para agregar archivos')

def archivo(rec):
    file = rec.replace('archivo', '').strip
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk('Lo siento, no se ha encontrado el archivo, usa los botones para agregar archivos')

def escribe(rec):
    try:
        with open('nota.txt', 'a') as f:
            write(f)
    except FileNotFoundError as e:
        file = open('nota.text', 'w')
        write(file)

  

def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk('Alarma activada a las ' + num + ' horas')
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print('DESPIERTA!!!')
            mixer.init()
            mixer.music.locad('auronplay-alarma.mp3')
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == 's':
            mixer.music.stop()
            break

def enviar_mensaje(rec):
    talk('¿A quién se envía el mensaje?')
    contact = listen('Te escucho')
    contact = contact.strip()

    if contact in contacts:
        for cont in contacts:
            if cont ==contact:
                contact = contacts[cont]
                talk('Di tu mensaje')
                message = listen('Te escucho')
                talk('Enviando mensaje')
                whapp.send_message(contact, message)
    else:
        talk('Contacto no registrado, agrégalo!')


def cierra(rec):
    for task in programs:
        kill_task = programs[task].split('\\')
        kill_task = kill_task[-1]
        if task in rec:
            sub.call(f'TASKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
        if 'todo' in rec:
            sub.call(f'TASKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
    if 'ciérrate' in rec:
        talk(f'Adiós')
        sub.call('TASKKILL \IM Negri_gui.exe \F', shell=True)
        
def buscame(rec):
    something =rec.replace('búscame', '').strip()
    talk('Buscando ' + something)
    browser.search(something)

def conversar(rec):
    chat = ChatBot('helena', database_uri=None)
    trainer = ListTrainer(chat)
    trainer.train(database.get_question_answers())
    talk('Vamos a conversar...')
    while True:
        try:
            request = listen('')
        except UnboundLocalError:
            talk('No te entendí, repite')
            continue
        print('Tú: ' + request)
        answer = chat.get_response(request)
        print('Helena: ', answer)
        talk(answer)
        if 'chau' in request:
            break

def reconocimiento(rec):
    rec = rec.replace('reconocimiento', '').strip()
    if rec == 'activado':
        t = tr.Thread(target = fr.face_rec, args=(0,))
        t.start()
        talk('Activando reconocimiento...')
    elif 'aguacate':
        fr.face_rec(1)
    


#Diccionario con palabras claves
key_words = {
    'reproduce': reproduce,
    'busca': busca,
    'alarma': thread_alarma,
    'colores': colores,
    'abre': abre,
    'archivo': archivo,
    'escribe': escribe,
    'mensaje': enviar_mensaje,
    'cierra': cierra,
    'ciérrate': cierra,
    'búscame': buscame,
    'reconocimiento': reconocimiento 
}


def run_negri():
    chat = ChatBot('helena', database_uri=None)
    trainer = ListTrainer(chat)
    trainer.train(database.get_question_answers())
    talk('Te escucho...')
    while True:
        try:
            rec = listen('')
        except UnboundLocalError:
            talk('No te entendí, intenta de nuevo')
            continue
        if 'busca' in rec:
            key_words['busca'](rec)
            break
        elif rec.split()[0] in key_words:
            key = rec.split()[0]
            key_words[key](rec)
        else:
            print('Tú: ' + rec)
            answer = chat.get_response(rec)
            print('Helena: ', answer)
            talk(answer)
            if 'chau' in rec:
                break

            
    main_window.update()

def write(f):
    talk('¿Qué quieres que escriba?')
    rec_write = listen('Te escucho')
    f.write(rec_write + os.linesep)
    f.close()
    talk('Listo, puedes revisarlo')
    sub.Popen('nota.text', shell=True)

def open_w_files():
    global namefile_entry, pathf_entry  
    window_files = Toplevel()
    window_files.title('Agrega archivos')
    window_files.configure(bg='#434343')
    window_files.geometry('300x200')
    window_files.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')

    title_label = Label(window_files, text='Agrega un archivo', fg='white', bg='#434343', font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    
    name_label = Label(window_files, text='Nombre del archivo', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    namefile_entry = Entry(window_files)
    namefile_entry.pack(pady=1)

    path_label = Label(window_files, text='Ruta del archivo', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)

    pathf_entry = Entry(window_files, width=35)
    pathf_entry.pack(pady=1)

    save_button = Button(window_files, text='Guardar', bg='#16222A', fg='white', width = 8, height=1, command=add_files)
    save_button.pack(pady=4)

def open_w_apps():
    global nameapps_entry, patha_entry 
    window_apps = Toplevel()
    window_apps.title('Agrega apps')
    window_apps.configure(bg='#434343')
    window_apps.geometry('300x200')
    window_apps.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_apps)} center')

    title_label = Label(window_apps, text='Agrega una app', fg='white', bg='#434343', font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    
    name_label = Label(window_apps, text='Nombre de la app', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    nameapps_entry = Entry(window_apps)
    nameapps_entry.pack(pady=1)

    patha_label = Label(window_apps, text='Ruta de la app', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    patha_label.pack(pady=2)

    patha_entry = Entry(window_apps, width=35)
    patha_entry.pack(pady=1)

    save_button = Button(window_apps, text='Guardar', bg='#16222A', fg='white', width = 8, height=1, command=add_apps)
    save_button.pack(pady=4)


def open_w_pages():
    global namepages_entry, pathp_entry
    window_pages = Toplevel()
    window_pages.title('Agrega páginas web')
    window_pages.configure(bg='#434343')
    window_pages.geometry('300x200')
    window_pages.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')

    title_label = Label(window_pages, text='Agrega una página web', fg='white', bg='#434343', font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    
    name_label = Label(window_pages, text='Nombre de página web', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    namepages_entry = Entry(window_pages)
    namepages_entry.pack(pady=1)

    path_label = Label(window_pages, text='URL de la página web', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)

    pathp_entry = Entry(window_pages, width=35)
    pathp_entry.pack(pady=1)

    save_button = Button(window_pages, text='Guardar', bg='#16222A', fg='white', width = 8, height=1, command=add_pages)
    save_button.pack(pady=4)

def open_w_contacts():
    global namecontact_entry, phone_entry
    window_contacts = Toplevel()
    window_contacts.title('Agrega un contacto')
    window_contacts.configure(bg='#434343')
    window_contacts.geometry('300x200')
    window_contacts.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_contacts)} center')

    title_label = Label(window_contacts, text='Agrega un contacto', fg='white', bg='#434343', font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    
    name_label = Label(window_contacts, text='Nombre', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    namecontact_entry = Entry(window_contacts)
    namecontact_entry.pack(pady=1)

    phone_label = Label(window_contacts, text='Teléfono', fg='white', bg='#434343', font=('Arial', 10, 'bold'))
    phone_label.pack(pady=2)

    phone_entry = Entry(window_contacts, width=35)
    phone_entry.pack(pady=1)

    save_button = Button(window_contacts, text='Guardar', bg='#16222A', fg='white', width = 8, height=1, command=add_contacts)
    save_button.pack(pady=4)


def add_files():
    name_file = namefile_entry.get().strip()
    path_file = pathf_entry.get().strip()

    files[name_file] = path_file
    save_data(name_file, path_file,'archivos.txt')
    namefile_entry.delete(0, 'end')
    pathf_entry.delete(0, 'end')

def add_apps():
    name_file = nameapps_entry.get().strip()
    path_file = patha_entry.get().strip()

    programs[name_file] = path_file
    save_data(name_file, path_file,'apps.txt')
    nameapps_entry.delete(0, 'end')
    patha_entry.delete(0, 'end')

def add_pages():
    name_page = namepages_entry.get().strip()
    url_pages = pathp_entry.get().strip()

    sites[name_page] = url_pages
    save_data(name_page, url_pages,'pages.txt')
    namepages_entry.delete(0, 'end')
    pathp_entry.delete(0, 'end')

def add_contacts():
    name_contact = namecontact_entry.get().strip()
    phone = phone_entry.get().strip()

    contacts[name_contact] = phone
    save_data(name_contact, phone,'contacts.txt')
    namecontact_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')


def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + ',' + value + "\n")
    except FileNotFoundError as f:
        file = open(file_name, 'a')
        file.write(key + 'a' + value + '\n')

def talk_pages():
    if bool(sites) == True:
        talk('Haz agregado las siguientes páginas web')
        for site in sites:
            talk(site)
    else: 
        talk('Aún no has agregado páginas web')

def talk_apps():
    if bool(programs) == True:
        talk('Haz agregado las siguientes apps')
        for app in programs:
            talk(app)
    else: 
        talk('Aún no has agregado apps')

def talk_files():
    if bool(files) == True:
        talk('Haz agregado los siguientes archivos')
        for file in files:
            talk(file)
    else: 
        talk('Aún no has agregado archivos')

    try:
        with open('name.text', 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open('name.txt', 'w')
        file.write(name)

def talk_contacts():
    if bool(contacts) == True:
        talk('Haz agregado las siguientes contactos')
        for cont in contacts:
            talk(cont)
    else: 
        talk('Aún no has agregado contactos')


def say_hello():
    if os.path.exists('name.text'):
        with open('name.text') as f:
            for name in f:
                talk(f'Hola, bienvenido {name}')
    else:
        give_me_name()

def give_me_name():
    talk('Hola, ¿Cómo te llamas?')
    name = listen('Te escucho')
    name= name.strip()
    talk(f'Bienvenido {name}')

def thread_hello():
    t=tr.Thread(target=say_hello)
    t.start()

thread_hello()


#Botones laterales
button_voice_mx = Button(main_window, text='Voz México', fg='white', bg='#38ef7d', font=('Arial', 10, 'bold'), command= mexican_voice)
button_voice_mx.place(x=615, y= 80, width=100, height=30)

button_voice_en = Button(main_window, text='Voz inglés', fg='white', bg='#ef8e38', font=('Arial', 10, 'bold'),command= english_voice)
button_voice_en.place(x=615, y= 120, width=100, height=30)

button_listen = Button(main_window, text='Escuchar', fg='white', bg='#B24592', font=('Arial', 15, 'bold'), width=20, height=30, command= run_negri)
button_listen.pack(side=BOTTOM, pady=10)
#(x=348, y= 350, width=120, height=40)

button_add_files = Button(main_window, text='Agregar files', fg='white', bg='#3a7bd5', font=('Arial', 10, 'bold'), command = open_w_files)
button_add_files.place(x=615, y= 160, width=100, height=30)

button_add_apps = Button(main_window, text='Agregar apps', fg='white', bg='#3a7bd5', font=('Arial', 10, 'bold'), command = open_w_apps)
button_add_apps.place(x=615, y= 200, width=100, height=30)

button_apps_pages = Button(main_window, text='Agregar sites', fg='white', bg='#3a7bd5', font=('Arial', 10, 'bold'), command = open_w_pages)
button_apps_pages.place(x=615, y= 240, width=100, height=30)

button_apps_contacts = Button(main_window, text='Agregar ctos.', fg='white', bg='#3a7bd5', font=('Arial', 10, 'bold'), command = open_w_contacts)
button_apps_contacts.place(x=615, y= 280, width=100, height=30)

button_speak = Button(main_window, text='Hablar', fg='white', bg='#ED4264', font=('Arial', 10, 'bold'), command= read_and_talk)
button_speak.place(x=615, y= 320, width=100, height=30)

#Botones inferiores
button_tell_pages = Button(main_window, text='Lista páginas', fg='white', bg='#003973', font=('Arial', 10, 'bold'), command = talk_pages)
button_tell_pages.place(x=300, y= 360, width=100, height=30)

button_tell_apps = Button(main_window, text='Lista Apps', fg='white', bg='#003973', font=('Arial', 10, 'bold'), command = talk_apps)
button_tell_apps.place(x=300, y= 400, width=100, height=30)

button_tell_files = Button(main_window, text='Lista Archivos', fg='white', bg='#003973', font=('Arial', 10, 'bold'), command = talk_files)
button_tell_files.place(x=420, y= 360, width=100, height=30)

button_tell_contacts = Button(main_window, text='Lista Contactos', fg='white', bg='#003973', font=('Arial', 10, 'bold'), command = talk_contacts)
button_tell_contacts.place(x=420, y= 400, width=100, height=30)

main_window.mainloop()