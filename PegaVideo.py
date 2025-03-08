import customtkinter as ctk
from tkinter import filedialog
import os
import yt_dlp
import sys
import re



# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("dark")  # Modo escuro
ctk.set_default_color_theme("blue")  # Tema azul

# Determina o diretório base
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

icone_path = os.path.join(base_path, "video.ico")

# Criar janela principal
window = ctk.CTk()
window.title("PegaVideo")
window.iconbitmap(icone_path)
window.geometry("500x500")

# Função para listar qualidades
def listar_qualidades():
    url = url_entry.get()
    qualidades = []
    ydl_opts = {'format': 'bestvideo+bestaudio/best', 'quiet': True, 'no_warnings': True, 'simulate': True, 'skip_download': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', None)
            if formats:
                for f in formats:
                    format_note = f.get('format_note', '')
                    acodec = f.get('acodec', 'none')
                    audio_disponivel = acodec != 'none'
                    qualidades.append(f"{f['format_id']} - {format_note} - Áudio: {audio_disponivel}")
        qualidades_combobox.configure(values=qualidades)
        if qualidades:
            qualidades_combobox.set(qualidades[0])
    except Exception as e:
        qualidades_combobox.configure(values=[f"Erro: {e}"])

# Função para atualizar progresso
def progress_hook(d):
    if d['status'] == 'downloading':
        p = d['_percent_str']
        p = re.sub(r'\x1b\[[0-9;]*m', '', p)
        try:
            progress_bar.set(float(p.replace('%', '')) / 100.0)
            progress_label.configure(text=p)
            window.update_idletasks()
        except ValueError:
            progress_label.configure(text=p)

# Função para baixar vídeo
def baixar_video():
    url = url_entry.get()
    selected_format = qualidades_combobox.get()
    if not selected_format:
        result_label.configure(text="Selecione um formato.")
        return
    format_id = selected_format.split(' - ')[0]
    ydl_opts = {
        'format': format_id,
        'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        result_label.configure(text="Download concluído!", text_color="green")
    except Exception as e:
        result_label.configure(text=f"Erro: {e}", text_color="red")

# Função para escolher diretório
def escolher_diretorio():
    global download_dir
    download_dir = filedialog.askdirectory()
    if download_dir:
        dir_label.configure(text=f"Diretório: {download_dir}")

# Função para colar link
def colar_link():
    try:
        texto = window.clipboard_get()
        url_entry.delete(0, "end")
        url_entry.insert(0, texto)
    except:
        pass

# Criando widgets estilizados
ctk.CTkLabel(window, text="URL do vídeo:", font=("Arial", 14)).pack(pady=5)

url_frame = ctk.CTkFrame(window, fg_color="transparent")
url_frame.pack(pady=5)

url_entry = ctk.CTkEntry(url_frame, width=320)
url_entry.pack(side="left", padx=5)

colar_button = ctk.CTkButton(url_frame, text="Colar", command=colar_link, width=70)
colar_button.pack(side="right")

listar_button = ctk.CTkButton(window, text="Listar Qualidades", command=listar_qualidades)
listar_button.pack(pady=10)

ctk.CTkLabel(window, text="Selecione a qualidade:", font=("Arial", 14)).pack(pady=5)

qualidades_combobox = ctk.CTkComboBox(window, width=350, )
qualidades_combobox.pack(pady=5)

dir_button = ctk.CTkButton(window, text="Escolher Diretório", command=escolher_diretorio)
dir_button.pack(pady=5)

dir_label = ctk.CTkLabel(window, text="Diretório: ", font=("Arial", 12))
dir_label.pack(pady=5)

baixar_button = ctk.CTkButton(window, text="Baixar Vídeo", command=baixar_video)
baixar_button.pack(pady=10)

progress_bar = ctk.CTkProgressBar(window, width=350)
progress_bar.pack(pady=5)
progress_bar.set(0)

progress_label = ctk.CTkLabel(window, text="", font=("Arial", 12))
progress_label.pack(pady=5)

result_label = ctk.CTkLabel(window, text="", font=("Arial", 12))
result_label.pack(pady=5)

download_dir = "."

# Iniciar interface gráfica
window.mainloop()
