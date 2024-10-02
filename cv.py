import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Fungsi untuk memotong dan membatasi panjang tampilan path
def format_path_for_display(path, max_length=50):
    if len(path) > max_length:
        return f"{path[:10]}...{path[-10:]}"
    return path

# Fungsi untuk memilih file video secara manual
def pilih_video():
    global video_path, fps
    video_path = filedialog.askopenfilename(
        title="Select Video Files",
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv")]
    )
    if video_path:
        truncated_path = format_path_for_display(video_path)
        label_file_path.config(text=f"Selected video: {truncated_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            messagebox.showerror("Error", "Error opening video")
            return
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.release()

        slider_fps.config(from_=1, to=fps)
        slider_fps.set(fps)

# Fungsi untuk membuat folder output tanpa menimpa
def buat_folder_output(base_folder_name):
    folder_name = base_folder_name
    counter = 1
    while os.path.exists(folder_name):
        folder_name = f"{base_folder_name}_{counter}"
        counter += 1
    os.makedirs(folder_name)
    return folder_name

# Fungsi untuk memulai proses ekstraksi frame
def mulai_proses():
    if not video_path:
        messagebox.showwarning("Warning", "Please select a video file first!")
        return

    frames_per_second = int(slider_fps.get())
    if frames_per_second <= 0:
        messagebox.showerror("Error", "FPS must be greater than 0")
        return

    output_folder = buat_folder_output('extracted_frames')
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Error opening video")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    second_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % int(fps / frames_per_second) == 0:
            frame_filename = os.path.join(output_folder, f'frame_second_{second_count}.jpg')
            cv2.imwrite(frame_filename, frame)
            
            # Update status label secara real-time
            label_status.config(text=f'Saving frame {second_count}')
            root.update()  # Refresh GUI to show updates
            
            second_count += 1

        frame_count += 1

    cap.release()
    messagebox.showinfo("Finished", f"Extraction complete! Frames saved in folder : {output_folder}")

# Setup GUI
root = tk.Tk()
root.title("Extracting Frames")

# Set ukuran jendela dan nonaktifkan resizing
root.geometry('280x230')  # Tetapkan ukuran jendela
root.resizable(False, False)  # Nonaktifkan resizing

# Variabel untuk menyimpan path video dan fps
video_path = ''
fps = 24  # Default sebelum video dipilih

# Label dan tombol untuk memilih file video
label_file_path = tk.Label(root, text="Extracting Frames from Video")
label_file_path.pack(pady=5)

btn_pilih_video = tk.Button(root, text="Select File", command=pilih_video)
btn_pilih_video.pack(pady=5)

# Slider untuk memilih frame rate per detik (FPS)
label_fps = tk.Label(root, text="Select Frames Per Second (FPS):")
label_fps.pack(pady=5)

slider_fps = tk.Scale(root, from_=1, to=fps, orient=tk.HORIZONTAL)
slider_fps.pack(pady=1)

# Label status untuk menampilkan informasi real-time
label_status = tk.Label(root, text="Waiting to start...")
label_status.pack(pady=5)

# Tombol untuk memulai proses
btn_mulai = tk.Button(root, text="Start Process", command=mulai_proses)
btn_mulai.pack(pady=5)

# Menjalankan GUI
root.mainloop()
