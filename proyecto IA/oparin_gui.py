import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import os
import threading as tr
import whatsapp as whapp
import browser
import database
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
from chatterbot import ChatBot 
from chatterbot.trainers import ListTrainer
from chatterbot import preprocessors

#diseño panel

main_window = Tk()
main_window.title("CHAT BOT")
main_window.geometry("800x530")
main_window.resizable(0,0)
main_window.configure(bg='#000')
label_title = Label(main_window, text="PROYECTO IA",bg="#000",fg="#fff",font=('Arial', 30, 'bold'))
label_title.pack(pady=10)#posicion label titulo

#canvas_comandos = Canvas(bg="#2193b0", height=180, width=230)
#canvas_comandos.place(x=0,y=0)
#canvas_comandos.create_text(90, 80, text=comandos, fill="white", font='Arial 10')

text_info = Text(main_window, bg="#000", fg="#fff")
text_info.place(x=0,y=100, height=345 ,width=233)

#coloca la imagen

oparin_photo = ImageTk.PhotoImage(Image.open("fondo2.jpg"))
window_photo = Label(main_window, image=oparin_photo, width=310, bg="#000")
window_photo.pack(pady=5)


#Inicio codigo 

name = "oparin"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')  # coloca una voz
engine.setProperty('voices', voices[0].id) # colocar voz que este en esa posicion
engine.setProperty('rate', 145) # velocidad de la voz

#Funcion que cargara datos almacenados dentro de mis diccionarios

def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val
    except FileNotFoundError as e:
        pass

#Directorios

sites = dict()
charge_data(sites, "pages.txt")

files = dict()
charge_data(files, "archivos.txt")

programs = dict()
charge_data(programs, "apps.txt")

agenda = dict()
charge_data(agenda, "contactos.txt")

#Funcion para convertir audio a texto

def talk(text):
    engine.say(text)  # convierte el texto en voz
    engine.runAndWait()

#Funcion opara leer y decir lo encontrado en internet

def read_and_talk():
    text = text_info.get("1.0", "end")
    talk(text)

#Funcion para scribir lo encontrado en internet en textarea

def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

#funcion para voz de IA

def listen(phrase=None):
    listener = sr.Recognizer()

    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk(phrase)
        pc = listener.listen(source)
        try:
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
        except sr.UnknownValueError:
            print("No te entendí, intenta d nuevo")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognitin service; {0}".format(e))
        return rec

#funciones que hay en los diccionarios como palabras claves

def reproduce(rec):
    music = rec.replace('reproduce', '')
    print("Reproduciendo " + music)
    talk("Reproduciendo " + music)
    pywhatkit.playonyt(music)

def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang('es')
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ": " + wiki)

def alarma(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
        print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("DESPIERTA!!!")
            mixer.init()
            mixer.music.load("auronplay-alarma.mp3")
            mixer.music.play()
            if keyboard.read_key() == 's':
                mixer.music.stop()
            break

def abre(rec):
    task = rec.replace('abre','').strip()
            
    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
    elif task in programs:
        for task in programs:
            if task in rec:
                talk(f'Abriendo {task}')
                os.startfile(programs[task])
    else:
        talk("No se ha encontrado la app o pagina web, \
            usa los botones de agregar...")

def archivo(rec):
    file = rec.replace('archivo','').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
            else:
                talk("No se ha encontrado el archivo, \
                    usa los botones de agregar...")

def escribir(rec):
    try:
        with open("notas.txt", 'a') as f:
            write(f)

    except FileNotFoundError as e:
        file = open("notas.txt", 'w')
        write(file)

def enviar_mensaje(rec):
    talk("¿A quien quieres enviar el mensaje?")
    contact = listen("Te escucho")
    contact = contact.strip()

    if contact in agenda:
        for con in agenda:
            if con == contact:
                contact = agenda[con]
                talk("¿Qué mensaje deseas enviar?")
                message = listen("Te escucho")
                talk("Enviando mensaje...")
                whapp.send_menssage(contact, message)
    else:
        talk("No existe un contacto con ese nombre")

def cierra(rec):
    for task in programs:
        kill_task = programs[task].split('\\')
        kill_task = kill_task[-1]
        if task in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
        if 'todo' in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
    if 'termina' in rec:
        talk(f'Adiós')
        sub.call(f'TASKKILL /IM python.exe /F', shell=True)

def buscame(rec):
    something = rec.replace('buscame', '').strip()
    talk("Buscando " + something)
    browser.search(something)

#Palabras clave
key_words = {
    'reproduce' : reproduce,
    'busca' : busca,
    'alarma' : alarma, #cambiar para que diga la hora
    'abre' : abre,
    'archivo' : archivo,
    'escribe' : escribir,
    'mensaje' : enviar_mensaje,
    'cierra' : cierra,
    'termina' : cierra,
    'buscame' : buscame,
}

#funcion principal

def run_oparin():
    chat = ChatBot('oparin', database_uri=None)
    trainer = ListTrainer(chat)
    trainer.train(database.get_questions_answers()) 
    talk("Te escucho...")
    while True:
        try:
            #rec = listen("")
            rec = listen("Te escucho")
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo")
            continue
        if 'busca' in rec:
            key_words['busca'](rec)
            break
        elif rec.split()[0] in key_words:
            #for word in key_words:
            #    if word in rec:
            key_words[rec.split()[0] ](rec)
        else:
            print("Tu: " , rec)
            answer = chat.get_response(rec)
            print("bot ",answer)
            if 'adios' in rec:
                break
    main_window.update()

#funcion para escrirbir dentro de un documento

def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen("Te escucho")
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("notas.txt", shell=True)

#Funciones para abrir, escribir y guardar datos

def open_w_files():
    global namefile_entry, pathf_entry
    windows_files = Toplevel() # segunda ventana
    windows_files.title("Agregar Archivos")
    windows_files.geometry("300x200")
    windows_files.resizable(0,0)
    windows_files.configure(bg='#434343')
    main_window.eval(f'tk::PlaceWindow {str(windows_files)} center') # centrar segunda ventana

    title_label = Label(
                            windows_files,
                            text="Agregar Archivos",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    title_label.pack(pady=3)
    name_label = Label(
                            windows_files,
                            text="Nombre del Archivo",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    name_label.pack(pady=2)

    namefile_entry = Entry(windows_files)
    namefile_entry.pack(pady=1)

    path_label = Label(
                            windows_files,
                            text="Ruta del Archivo",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    path_label.pack(pady=2)

    pathf_entry = Entry(windows_files, width=35)
    pathf_entry.pack(pady=1)

    save_button = Button(
                            windows_files,
                            text="Guardar",
                            bg="#16222a",
                            fg="#fff",
                            width=8,
                            height=1,
                            command=add_files
                        )
    save_button.pack(pady=5)


def open_w_apps():
    global nameapps_entry, pathapps_entry
    windows_apps = Toplevel() # tercer ventana
    windows_apps.title("Agregar una app")
    windows_apps.geometry("300x200")
    windows_apps.resizable(0,0)
    windows_apps.configure(bg='#434343')
    main_window.eval(f'tk::PlaceWindow {str(windows_apps)} center') # centrar segunda ventana

    title_label = Label(
                            windows_apps,
                            text="Agregar una app",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    title_label.pack(pady=3)
    name_label = Label(
                            windows_apps,
                            text="Nombre de la app",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    name_label.pack(pady=2)

    nameapps_entry = Entry(windows_apps)
    nameapps_entry.pack(pady=1)

    path_label = Label(
                            windows_apps,
                            text="Ruta de la app",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    path_label.pack(pady=2)

    pathapps_entry = Entry(windows_apps, width=35)
    pathapps_entry.pack(pady=1)

    save_button = Button(
                            windows_apps,
                            text="Guardar",
                            bg="#16222a",
                            fg="#fff",
                            width=8,
                            height=1,
                            command=add_apps
                        )
    save_button.pack(pady=5)

def open_w_pages():
    global namep_entry, pathp_entry
    windows_pages = Toplevel() # cuarta ventana
    windows_pages.title("Agregar una pagina web")
    windows_pages.geometry("300x200")
    windows_pages.resizable(0,0)
    windows_pages.configure(bg='#434343')
    main_window.eval(f'tk::PlaceWindow {str(windows_pages)} center') # centrar segunda ventana

    title_label = Label(
                            windows_pages,
                            text="Agregar una pagina",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    title_label.pack(pady=3)
    name_label = Label(
                            windows_pages,
                            text="Nombre de la pagina",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    name_label.pack(pady=2)

    namep_entry = Entry(windows_pages)
    namep_entry.pack(pady=1)

    path_label = Label(
                            windows_pages,
                            text="URL de la pagina",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    path_label.pack(pady=2)

    pathp_entry = Entry(windows_pages, width=35)
    pathp_entry.pack(pady=1)

    save_button = Button(
                            windows_pages,
                            text="Guardar",
                            bg="#16222a",
                            fg="#fff",
                            width=8,
                            height=1,
                            command=add_pages
                        )
    save_button.pack(pady=5)

def open_w_contacts():
    global namec_entry, pathc_entry
    windows_contacts = Toplevel() # cuarta ventana
    windows_contacts.title("Agregar contacto")
    windows_contacts.geometry("300x200")
    windows_contacts.resizable(0,0)
    windows_contacts.configure(bg='#434343')
    main_window.eval(f'tk::PlaceWindow {str(windows_contacts)} center') # centrar segunda ventana

    title_label = Label(
                            windows_contacts,
                            text="Agregar contacto",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    title_label.pack(pady=3)
    name_label = Label(
                            windows_contacts,
                            text="Nombre del contacto",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    name_label.pack(pady=2)

    namec_entry = Entry(windows_contacts)
    namec_entry.pack(pady=1)

    path_label = Label(
                            windows_contacts,
                            text="Numero (codigo pais)",
                            fg="#fff",
                            bg="#434343",
                            font=('Arial', 10, 'bold')
                        )
    path_label.pack(pady=2)

    pathc_entry = Entry(windows_contacts, width=35)
    pathc_entry.pack(pady=1)

    save_button = Button(
                            windows_contacts,
                            text="Guardar",
                            bg="#16222a",
                            fg="#fff",
                            width=8,
                            height=1,
                            command=add_contact
                        )
    save_button.pack(pady=5)

#funcion para agregar archivos,paginas y apps

def add_files():
    name_file = namefile_entry.get().strip()
    path_file = pathf_entry.get().strip()
    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefile_entry.delete(0, "end")
    pathf_entry.delete(0,"end")


def add_apps():
    name_app = nameapps_entry.get().strip()
    path_app = pathapps_entry.get().strip()
    programs[name_app] = path_app
    save_data(name_app, path_app, "apps.txt")
    nameapps_entry.delete(0, "end")
    pathapps_entry.delete(0,"end")

def add_pages():
    name_pages = namep_entry.get().strip()
    url_pages = pathp_entry.get().strip()
    sites[name_pages] = url_pages
    save_data(name_pages, url_pages, "pages.txt")
    namep_entry.delete(0, "end")
    pathp_entry.delete(0,"end")

def add_contact():
    name_contacto = namec_entry.get().strip()
    path_contacto = pathc_entry.get().strip()
    agenda[name_contacto] = path_contacto
    save_data(name_contacto, path_contacto, "contactos.txt")
    namec_entry.delete(0, "end")
    pathc_entry.delete(0,"end")

#funcion para guardar datos

def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError:
        file = open(file_name, 'a')
        file.write(key + "," + value + "\n")

#funcion para mostrar los datos almacenados

def talk_pages():
    if bool(sites) == True:
        talk("Has agregado las siguientes paginas web")
        for site in sites:
            talk(site)
    else:
        talk("Aun no has agregado páginas web!")

def talk_apps():
    if bool(programs) == True:
        talk("Has agregado las siguientes apps")
        for app in programs:
            talk(app)
    else:
        talk("Aun no has agregado apps!")

def talk_files():
    if bool(files) == True:
        talk("Has agregado las siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("Aun no has agregado archivos!")

def talk_contact():
    if bool(agenda) == True:
        talk("Has agregado los siguientes contactos")
        for conta in agenda:
            talk(conta)
    else:
        talk("Aun no hay contactos registrados!")

#funcion para preguntar nombre
def give_me_name():
    talk("Hola, ¿Cómo te llamas?")
    name = listen("Te escucho")
    name = name.strip()
    talk(f"Bienvenido {name}")
    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(name)

#funcion para decir nombre

def say_hello():
    if os.path.exists("name.txt"):
        with open("name.txt") as f:
            for name in f:
                talk(f"Hola, bienvenido {name}")
    else:
        give_me_name()


def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()

thread_hello()

#diseño panel botones
#boton hablar

button_speak = Button( main_window, text="Hablar", fg="#fff", bg="#00b4db",font=('Arial', 13, "bold"), command=read_and_talk)
button_speak.place(x=580, y=100, width=200, height=30) #posicionamiento del boton

#boton guardar diccionario

button_add_files = Button( main_window, text="Agregar Archivos", fg="#fff", bg="#00b4db",font=('Arial', 13, "bold"), command=open_w_files)
button_add_files.place(x=580, y=140, width=200, height=30)

button_add_app = Button( main_window, text="Agregar Apps", fg="#fff", bg="#00b4db",font=('Arial', 13, "bold"), command=open_w_files)
button_add_app.place(x=580, y=180, width=200, height=30)

button_add_pages = Button(main_window, text="Agregar Paginas", fg="#fff",  bg="#00b4db",font=('Arial', 13, "bold"), command=open_w_pages)
button_add_pages.place(x=580, y=220, width=200, height=30)

button_add_contacts = Button( main_window, text="Agregar contactos",fg="#fff", bg="#00b4db",font=('Arial', 13, "bold"), command=open_w_contacts)
button_add_contacts.place(x=580, y=260, width=200, height=30)

#boton contar el total de archivos,paginas y apps guardadas

button_tell_pages = Button( main_window, text="Páginas agregadas",fg="#fff", bg="#00b4db",font=('Arial', 13, "bold"), command=talk_pages)
button_tell_pages.place(x=580, y=300, width=200, height=30)

button_tell_apps = Button( main_window,text="Apps agregadas", fg="#fff", bg="#00b4db", font=('Arial', 13, "bold"), command=talk_apps)
button_tell_apps.place(x=580, y=340, width=200, height=30)

button_tell_files = Button(main_window, text="Archivos agregados", fg="#fff", bg="#00b4db",font=('Arial', 13, "bold"), command=talk_files)
button_tell_files.place(x=580, y=380,width=200, height=30)

button_tell_contact = Button( main_window, text="Contactos agregados", fg="#fff", bg="#00b4db", font=('Arial', 13, "bold"), command=talk_contact)
button_tell_contact.place(x=580, y=420,width=200, height=30)

#boton principal

button_listen = Button(main_window,text="Escuchar",fg="white", bg="#1565c0",font=("Arial", 15, "bold"), width=10,height=1, command=run_oparin)
button_listen.pack(side=BOTTOM, pady=50)


main_window.mainloop()