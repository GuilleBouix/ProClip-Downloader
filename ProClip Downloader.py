from tkinter import *
from customtkinter import *
from pytube import YouTube
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
import os
import re



# Directorio #
if getattr(sys, 'frozen', False):
    directorio_base = sys._MEIPASS
else:
    directorio_base = os.path.dirname(os.path.abspath(__file__))
icono = os.path.join(directorio_base, "img", "icon.ico")
logo_path = os.path.join(directorio_base, "img", "logo.png")
def resize_image(image_path, new_size):
    original_image = Image.open(image_path)
    aspect_ratio = original_image.width / original_image.height
    new_width = int(new_size * aspect_ratio)
    resized_image = original_image.resize((new_width, new_size), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)



# Ventana Principal #
root = Tk()
root.resizable(False,False)
root.title("ProClip - Downloader")
root.config(background='#131b2e')
if os.path.exists(icono):
    root.iconbitmap(icono)
    


# Colores # 
fondo = '#131b2e' 
azul = '#070b14'
celeste = '#344053'
celeste_claro = '#27d3ff'



# Header #
header_frame = CTkFrame(root,
                        fg_color=(azul,azul),
                        corner_radius=20)
header_frame.grid(padx=50, pady=10)

if os.path.exists(logo_path):
    resized_logo = resize_image(logo_path, 85)
    logo_label = Label(header_frame, 
                       image=resized_logo, 
                       bg='#070b14',
                       borderwidth=0)
    logo_label.image = resized_logo
    logo_label.pack(padx=30, pady=10)




# Body #
main_frame = CTkFrame(root,fg_color=(azul,azul),corner_radius=20)
main_frame.grid(row=1, padx=50, pady=20)



# Entry #
txt_enlace = CTkEntry(main_frame,
                      width=430,
                      height=50,
                      fg_color=('white','white'),
                      bg_color=azul,
                      border_width=0,
                      text_color='black',
                      font=('Montserrat',20),
                      corner_radius=20,
                      justify='center',
                      placeholder_text='Paste your link')
txt_enlace.grid(padx=20,pady=20)



# Botones #
button_frame = CTkFrame(main_frame,fg_color=(azul,azul),corner_radius=20)
button_frame.grid(row=1)

def on_enter_conversor(event):
    btn_conversor.configure(border_color=celeste_claro, text_color=celeste_claro)
def on_leave_conversor(event):
    btn_conversor.configure(border_color=celeste, text_color='white')

btn_conversor = CTkButton(button_frame,
                          width=210,
                          height=60,
                          text='Location',
                          font=('Montserrat Light',25),
                          corner_radius=20,
                          border_color=celeste,
                          fg_color=(azul,azul),
                          text_color='white',
                          border_width=1,
                          cursor='hand2',
                          hover=None,
                          command=lambda:location())
btn_conversor.grid(row=0,column=0,padx=5)

def on_enter_limpiar(event):
    btn_restart.configure(border_color=celeste_claro, text_color=celeste_claro)
def on_leave_limpiar(event):
    btn_restart.configure(border_color=celeste, text_color='white')
    
btn_restart = CTkButton(button_frame,
                          width=210,
                          height=60,
                          text='Restart',
                          font=('Montserrat Light',25),
                          corner_radius=20,
                          border_color=celeste,
                          fg_color=(azul,azul),
                          text_color='white',
                          border_width=1,
                          cursor='hand2',
                          hover=None,
                          command=lambda:restart())
btn_restart.grid(row=0,column=1,padx=5)

btn_conversor.bind("<Enter>", on_enter_conversor)
btn_conversor.bind("<Leave>", on_leave_conversor)
btn_restart.bind("<Enter>", on_enter_limpiar)
btn_restart.bind("<Leave>", on_leave_limpiar)

def on_enter_download(event):
    btn_download.configure(border_color=celeste_claro, fg_color=(celeste_claro,celeste_claro), text_color='black')
def on_leave_download(event):
    btn_download.configure(border_color=celeste,fg_color=(azul,azul),text_color='white')
    
btn_download = CTkButton(main_frame,
                width=430,
                height=60,
                text='\uf063  Download',
                font=('Montserrat Light',25),
                corner_radius=20,
                border_color=celeste,
                fg_color=(azul,azul),
                text_color='white',
                border_width=1,
                cursor='hand2',
                hover=None,
                command=lambda:count(lbl_descarga,1),)
btn_download.grid(row=2,pady=20)

btn_download.bind("<Enter>", on_enter_download)
btn_download.bind("<Leave>", on_leave_download)



# Contador Progreso #
lbl_descarga = Label(main_frame, text="", font=('Montserrat', 15), bg=azul, fg=celeste_claro)
lbl_descarga.grid(row=3)

empty_frame = Frame(main_frame,background=azul)
empty_frame.grid(row=4,pady=10)



# Funciones #

# Seleccionar Ubicación #
ubicacion_seleccionada = os.path.join(os.path.expanduser("~"), "Desktop")
def location():
    global ubicacion_seleccionada
    ubicacion_seleccionada = filedialog.askdirectory(initialdir=os.path.join(os.path.expanduser("~"), "Desktop"))
    if not ubicacion_seleccionada:
        ubicacion_seleccionada = os.path.join(os.path.expanduser("~"), "Desktop")

# Reiniciar Downloader #
def restart():
    global ubicacion_seleccionada
    ubicacion_seleccionada = os.path.join(os.path.expanduser("~"), "Desktop")
    lbl_descarga.config(text="")
    txt_enlace.delete(0, 'end')
    txt_enlace.focus()

# Contador de Descarga #
def count(lbl_descarga, progress):
    global ubicacion_seleccionada
    if re.match(r'https?://(?:www\.)?(?:youtube\.com/.*|youtu\.be/.*)', txt_enlace.get()):
        if progress <= 99:
            lbl_descarga.config(text=f"{progress}%")
            root.after(30, count, lbl_descarga, progress + 1)
        else:
            lbl_descarga.config(text="Download Completed!")
            enlace_youtube = txt_enlace.get()
            # Validar si el enlace es de YouTube usando una expresión regular
            if re.match(r'https?://(?:www\.)?(?:youtube\.com/.*|youtu\.be/.*)', enlace_youtube):
                if ubicacion_seleccionada:
                    descargar_video(enlace_youtube, ubicacion_seleccionada)
    else:
        messagebox.showerror("Error", "Invalid link.")

# Descargar Video #
def descargar_video(enlace, ubicacion):
    video = YouTube(enlace)
    stream = video.streams.get_highest_resolution()
    stream.download(output_path=ubicacion)



# Centrar Ventana #
root.update_idletasks()
width = root.winfo_reqwidth()
height = root.winfo_reqheight()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f'{width}x{height}+{x}+{y-20}')



# Bucle Principal #
root.mainloop()