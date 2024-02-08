import os
import threading
import shutil
import urllib.request
from tqdm import tqdm
from pytube import YouTube
from win10toast import ToastNotifier

# Create a directory to store downloaded videos
download_dir = "downloaded_videos"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Function to download YouTube video
def download_video(url, resolution):
    yt = YouTube(url)
    if resolution == "highest":
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    elif resolution == "lowest":
        video = yt.streams.filter(progressive=True, file_extension='mp4').last()
    elif resolution == "custom":
        print("Available resolutions:")
        for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
            print(f"{stream.resolution} - {stream.mime_type}")
        selected_resolution = input("Enter the resolution you want to download (e.g., '720p', '360p'): ")
        video = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_resolution).first()
    else:
        print("Invalid resolution option.")
        return

    file_size = video.filesize
    filename = video.default_filename
    file_path = os.path.join(download_dir, filename)

    # Download progress bar
    def progress_callback(block_num, block_size, total_size):
        progress_bar.update(block_size)

    with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=filename, ascii=True) as progress_bar:
        urllib.request.urlretrieve(video.url, file_path, reporthook=progress_callback)

    # Notify when download completes
    toaster = ToastNotifier()
    toaster.show_toast("Download Complete", f"{filename} has been downloaded successfully.", duration=10)

# Main function
def main():
    url = input("Enter the YouTube video URL: ")
    if not url.startswith("https://www.youtube.com/watch?v="):
        print("Invalid YouTube URL.")
        return

    resolution_option = input("Choose resolution option ('highest', 'lowest', or 'custom'): ").lower()
    if resolution_option not in ['highest', 'lowest', 'custom']:
        print("Invalid resolution option.")
        return

    try:
        # Start download in a separate thread
        download_thread = threading.Thread(target=download_video, args=(url, resolution_option))
        download_thread.start()

        # Wait for the download thread to finish
        download_thread.join()
    except KeyboardInterrupt:
        print("Download cancelled.")

if __name__ == "__main__":
    main()
