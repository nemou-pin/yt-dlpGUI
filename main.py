import flet as ft
import os
import subprocess
import platform
import pyperclip
if platform == "Windows":
    import winsound
else:
    pass

home_dir = os.path.expanduser("~")
quality_video = [ft.dropdown.Option("1080p"),ft.dropdown.Option("720p"),ft.dropdown.Option("480p"),ft.dropdown.Option("360p"),ft.dropdown.Option("240p")]
quality_mp3 = [ft.dropdown.Option("320kbps"),ft.dropdown.Option("128kbps")]
quality_wav = []

process_running = False
current_process = None

def main(page: ft.Page):
    page.title = "yt-dlpGUI"
    page.theme = ft.Theme(color_scheme_seed="RED")
    page.window_width = 600
    page.padding = 20
    page.window_height = 900
    page.scroll = "auto"
    
    def save_dir_select(e:ft.FilePickerResultEvent):
        if e.path:
            save_dir_input.value = e.path
        else:
            save_dir_input.value = home_dir
        page.update()
        
    def cookie(e:ft.FilePickerResultEvent):
        if e.files:
            cookie_file.value = e.files[0].path
        else:
            cookie_file.value = ""
        page.update()
        
    save_dir = ft.FilePicker(on_result=save_dir_select)
    page.overlay.append(save_dir)
    cokkie_dialog = ft.FilePicker(on_result=cookie)
    page.overlay.append(cokkie_dialog)
    
    def change_quality(e):
        if e.control.value == "mp3":
            video_quality.options = quality_mp3
            video_quality.value = "320kbps"
        elif e.control.value == "wav":
            video_quality.options = quality_wav
        else:
            video_quality.options = quality_video
            video_quality.value = "1080p"
        page.update()
        
    def check_num(e):
        if e.control.value == True:
            multiconnection_num.disabled = False
            multiconnection_num.update()
        elif e.control.value == False:
            multiconnection_num.disabled = True
            multiconnection_num.update()
            
    def get_clip(e):
        try:
            url_input.value = pyperclip.paste()
            page.snack_bar = ft.SnackBar(ft.Text("Pasted URL"))
            page.snack_bar.open = True
            page.update()
        except pyperclip.PyperclipException as e:
            page.snack_bar = ft.SnackBar(ft.Text("Error: " + str(e)))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text("Error: " + str(e)))
            page.snack_bar.open = True
            page.update()
    
    def download(e):
        global process_running
        global current_process
        
        if process_running:
            if current_process:
                current_process.terminate()
            process_running = False
            return
        
        command = ["yt-dlp","--add-metadata","--no-color","--add-chapters"]
        if url_input.value:
            command.append(url_input.value)
            if video_format.value == "mp4":
                if video_quality.value == "1080p":
                    command.append("--format=bestvideo[height<=1080]+bestaudio/best[ext=mp4][height<=1080]/best")
                    command.extend(["--merge-output-format","mp4"])
                elif video_quality.value == "720p":
                    command.append("--format=bestvideo[height<=720]+bestaudio/best[ext=mp4][height<=720]/best")
                    command.extend(["--merge-output-format","mp4"])
                elif video_quality.value == "480p":
                    command.append("--format=bestvideo[height<=480]+bestaudio/best[ext=mp4][height<=480]/best")
                    command.extend(["--merge-output-format","mp4"])
                elif video_quality.value == "360p":
                    command.append("--format=bestvideo[height<=360]+bestaudio/best[ext=mp4][height<=360]/best")
                    command.extend(["--merge-output-format","mp4"])
                elif video_quality.value == "240p":
                    command.append("--format=bestvideo[height<=240]+bestaudio/best[ext=mp4][height<=240]/best")
                    command.extend(["--merge-output-format","mp4"])
                
            elif video_format.value == "mp3":
                if video_quality.value == "320kbps":
                    command.append("--format=bestaudio[ext=m4a]/best")
                    command.extend(["-x","--audio-format","mp3","--audio-quality","320K"])
                elif video_quality.value == "128kbps":
                    command.append("--format=bestaudio[ext=m4a]/best")
                    command.extend(["-x", "--audio-format", "mp3", "--audio-quality", "128K"])
                    
            elif video_format.value == "wav":
                command.append("--format=bestaudio[ext=m4a]/best")
                command.extend(["-x", "--audio-format", "wav"])
                
            if enable_playlist.value == False:
                if enable_playlist_index.value == True:
                    command.extend(["-o",f"{save_dir_input.value}/%(playlist_index)s-%(title)s.%(ext)s"])
                elif enable_playlist_index.value == False:
                    command.extend(["-o",f"{save_dir_input.value}/%(title)s.%(ext)s"])
            elif enable_playlist.value == True:
                if enable_playlist_index.value == True:
                    command.extend(["-o", f"{save_dir_input.value}/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s"])
                elif enable_playlist_index.value == False:
                    command.extend(["-o", f"{save_dir_input.value}/%(playlist_title)s/%(title)s.%(ext)s"])
                
            if enable_multiconnection.value == True:
                command.extend(["-N",f"{multiconnection_num.value}"])
                
            if embed_thumbnail.value == True:
                if video_format.value == "wav":
                    pass
                else:
                    command.extend(["--embed-thumbnail"])
                    
            if enable_cookie.value == True:
                if cookie_file.value:
                    command.extend(["--cookies", f"{cookie_file.value}"])
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Cookie file not selected"))
                    page.snack_bar.open = True
                    page.update()
                    return
            
            progress_bar.value = None
            page.window_progress_bar = None
            print(command)
            page.update()
            progress_bar.update()
            process_running = True
            with open("log.log",mode="a",encoding="shift-jis") as f:
                try:
                    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True,creationflags=subprocess.CREATE_NO_WINDOW) as p:
                        current_process = p
                        
                        for line in p.stdout:
                            progress_text.value = line
                            progress_text.update()
                            f.write(line)
                            page.title = f"yt-dlpGUI - {line}"
                            page.update()
                            
                        p.wait()
                        
                        if p.returncode != 0:
                            page.snack_bar = ft.SnackBar(ft.Text(f"An error occurred during processing."))
                            page.snack_bar.open = True
                            page.title = "yt-dlpGUI"
                            progress_bar.value = 0
                            progress_bar.update()
                            page.window_progress_bar = 0
                            page.update()
                            if platform == "Windows":
                                winsound.MessageBeep(winsound.MB_ICONERROR)
                        else:
                            page.snack_bar = ft.SnackBar(ft.Text("Download complete"))
                            page.title = "yt-dlpGUI"
                            progress_bar.value = 1
                            progress_bar.update()
                            page.snack_bar.open = True
                            page.window_progress_bar = 1
                            page.update()
                            if platform == "Windows":
                                winsound.MessageBeep(winsound.MB_ICONHAND)
                except Exception as e:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"))
                    page.snack_bar.open = True
                    page.title = "yt-dlpGUI"
                    progress_bar.value = 0
                    progress_bar.update()
                    page.window_progress_bar = 0
                    page.update()
                    if platform == "Windows":
                        winsound.MessageBeep(winsound.MB_ICONERROR)
                        
                finally:
                    process_running = False
                    current_process = None
            
        else:
            # SnackBar
            page.snack_bar = ft.SnackBar(ft.Text("URL not specified"))
            page.snack_bar.open = True
            page.update()
    
    url_input = ft.TextField(label="URL",icon=ft.icons.LINK,expand=True)
    url_clip = ft.IconButton(icon=ft.icons.PASTE,on_click=get_clip,tooltip="Copy URL from clipboard")
    save_dir_input = ft.TextField(label="Save directory", icon=ft.icons.FOLDER,value=home_dir,expand=True)
    save_dir_button = ft.IconButton(icon=ft.icons.OPEN_IN_NEW, on_click=lambda _: save_dir.get_directory_path(dialog_title="保存先を選択",initial_directory=home_dir),tooltip="Select save destination")
    download_button = ft.FloatingActionButton(icon=ft.icons.DOWNLOAD,on_click=download)
    progress_bar = ft.ProgressBar(value=0)
    video_format = ft.Dropdown(label="Format", options=[ft.dropdown.Option("mp4"), ft.dropdown.Option("mp3"), ft.dropdown.Option("wav")],expand=True,on_change=change_quality,value="mp4")
    video_quality = ft.Dropdown(expand=True,label="quality", options=quality_video, value="1080p")
    progress_text = ft.Text("No Task",max_lines=1,semantics_label="...")
    embed_thumbnail = ft.Checkbox(label="Embed thumbnail(However, it is not embedded in wav)")
    enable_playlist = ft.Checkbox(label="Create a directory with the playlist name")
    enable_playlist_index = ft.Checkbox(label="Add playlist index to the beginning of the file name")
    enable_multiconnection = ft.Checkbox(label="Enable multiconnection",on_change=check_num)
    multiconnection_num = ft.TextField(label="Number of connections", value="5",expand=True,disabled=True)
    enable_cookie = ft.Checkbox(label="Enable cookie")
    cookie_file = ft.TextField(label="Cookie file", value="",expand=True)
    sel_cookie_file = ft.IconButton(icon=ft.icons.COOKIE,on_click=lambda _:cokkie_dialog.pick_files(allow_multiple=False,allowed_extensions=["txt"]))
    cookies = ft.Row([cookie_file,sel_cookie_file])
    
    page.add(ft.Text("Main",size=24),ft.Row([url_input,url_clip]),ft.Row([save_dir_input,save_dir_button]),ft.Text("Option",size=24),ft.Row([video_format,video_quality]),embed_thumbnail,enable_playlist,enable_playlist_index,ft.Row([enable_multiconnection,multiconnection_num]),enable_cookie,cookies,ft.Text("Progress",size=24),progress_text,progress_bar, download_button)


if __name__ == "__main__":
    ft.app(target=main)
