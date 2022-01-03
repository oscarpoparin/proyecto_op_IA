import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import colors
import os
from pygame import mixer
import threading as tr
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pytz import timezone

name = "oparin"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')  # coloca una voz
# colocar voz que este en esa posicion
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 145)

sites = {
    'google': 'google.com'
}

files = {
    'carta': 'carta - carta.pdf'
}

commands = {
    'play': 'spotifi play',
    'pausa': 'sporifi pause'
}

programs = {
    'word': r'C:\Program Files\Microsof Office\root\Office16\WINWORD.EXE'
}


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            print("puedes decir algo...")
            talk("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass
    return rec


def run_oparin():
    rec = listen()
    if 'reproduce' in rec:
        music = rec.replace('reproce', '')
        print("reproduciendo" + music)
        talk("reproduciendo" + music)
        pywhatkit.playonyt(music)
    elif 'busca' in rec:
        search = rec.replace('busca', '')
        wikipedia.set_lang("es")
        wiki = wikipedia.summary(search, 1)
        print(search + ": " + wiki)
        talk(wiki)
    elif 'alarma' in rec:
        num = rec.replace('alarma', '')
        num = num.strip()
        talk("Alarma activada a las " + num + "horas")
        while True:
            if datetime.datetime.now().strftime('%H:%M') == num:
                print("despierta")
                mixer.init()
                mixer.music.load("")
                mixer.music.play()
                if keyboard.read_key() == "s":
                    mixer.music.stop()
                    break
    elif 'colores' in rec:
        talk("Enseguida")
        colors.capture()
    elif 'abre' in rec:
        for site in sites:
            if site in rec:
                sub.call(f'start chrome.exe {sites[site]}', shell=True)
                talk("Arbiendo {site}")
        for app in programs:
            if app in rec:
                talk("Abriendo {app}")
                os.startfile(programs[app])
    elif 'archivo' in rec:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    elif 'escribe' in rec:
        try:
            with open("notas.txt", 'a') as f:
                write(f)

        except FileNotFoundError as e:
            file = open("notas.txt", 'w')
            write(file)

    elif 'termina' in rec:
        talk("adios")
       #break


def write(f):
    talk("¿Qué deseas que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("notas.txt", shell=True)


if __name__ == '__main__':
    run_oparin()