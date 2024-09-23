import cv2
import yt_dlp
import os
import colorsys

def list_to_string(lst, num_digits=2):
    rounded_strings = [f"{int(round(num)):0{num_digits}d}" for num in lst]
    return ''.join(rounded_strings)

def rgb_to_hsb(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = h * 98 + 1
    s = s * 98 + 1
    v = v * 98 + 1
    return h, s, v

def process_frame(frame):
    # Resize the frame to 50x50 pixels
    frame = cv2.resize(frame, (50, 50))
    
    hue, saturation, brightness = [], [], []
    
    for y in range(50):
        for x in range(50):
            b, g, r = frame[y, x]
            h, s, v = rgb_to_hsb(r, g, b)
            hue.append(h)
            saturation.append(s)
            brightness.append(v)
    
    hue_str = list_to_string(hue)
    saturation_str = list_to_string(saturation)
    brightness_str = list_to_string(brightness)
    
    return hue_str, saturation_str, brightness_str

def download_youtube_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo',
            'outtmpl': 'downloaded_video.mp4',
            'noplaylist': True,
            'merge_output_format': None,  # Disable merging
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return 'downloaded_video.mp4'
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return None

def process_youtube_video(url):
    video_path = download_youtube_video(url)
    
    if video_path is None:
        print("Failed to download or process the video.")
        return
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return
        
        with open("HSB_data.txt", "w") as file:
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                print(f"Processing frame {frame_count}...")
                hue_str, saturation_str, brightness_str = process_frame(frame)
                file.write(f"Frame {frame_count}: {hue_str}|{saturation_str}|{brightness_str}|\n")
            
            print(f"Total frames processed: {frame_count}")
        
        cap.release()
    
    except Exception as e:
        print(f"An error occurred while processing the video: {e}")

def main():
    url = input("Please enter the YouTube video URL: ")
    process_youtube_video(url)

if __name__ == "__main__":
    main()
