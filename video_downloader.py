import os
import streamlit as st
import yt_dlp
import instaloader
import re

# Streamlit app configuration
st.set_page_config(page_title=" Video Downloader", page_icon=":arrow_down:", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 15px;
            border-radius: 10px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput input {
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
        }
        .stProgress {
            height: 25px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# UI elements
st.title("📹  Video Downloader")
st.sidebar.header("Select Platform and Settings")

# Sidebar for platform selection and quality option
platform = st.sidebar.selectbox("Choose a platform", ["YouTube", "Instagram", "Facebook"])
video_quality = st.sidebar.selectbox("Choose video quality", ["Best Available", "Low", "Medium", "High"])
url = st.text_input("Enter the video/content URL")

# Folder input with default
save_path = st.text_input("Enter the folder to save the video/content (default: downloads)", "downloads")

# File format selection for YouTube
file_format = st.sidebar.selectbox("Select File Format", ["MP4", "MP3"])

# Progress bar widget initialization
progress_bar = st.progress(0)
progress_text = st.empty()

# Function to display download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        # Strip out any color codes from the progress string
        percent_str = d['_percent_str'].strip('%')
        percent_clean = re.sub(r'\x1b\[.*?m', '', percent_str)  # Remove color codes
        try:
            percent_complete = float(percent_clean)
            progress_bar.progress(int(percent_complete))
            progress_text.text(f"Downloading... {percent_complete}% complete")
        except ValueError:
            pass  # In case the conversion fails, just ignore it

# Function to download YouTube videos with options
def download_youtube_video(url, quality, save_path='downloads', format_choice="mp4"):
    format_map = {
        "Best Available": "best",
        "Low": "worst",
        "Medium": "best[height<=720]",
        "High": "best[height<=1080]"
    }
    file_extension = "mp4" if format_choice == "MP4" else "mp3"
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.' + file_extension),
        'format': format_map.get(quality, 'best'),
        'progress_hooks': [progress_hook]
    }
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.info(f"Starting download from YouTube...")
            ydl.download([url])
            st.success("Download completed!")
            progress_bar.empty()  # Clear progress bar after completion
            progress_text.empty()  # Clear text after completion
    except Exception as e:
        st.error(f"Error: {e}")
        progress_bar.empty()  # Clear progress bar in case of error
        progress_text.empty()  # Clear text in case of error

# Function to download Instagram content
def download_instagram_content(url, save_path='downloads'):
    try:
        loader = instaloader.Instaloader(download_videos=True, download_comments=False)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        shortcode = url.split("/")[-2]
        st.info(f"Downloading content from Instagram post: {shortcode}")
        loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=save_path)
        st.success("Download completed!")
    except Exception as e:
        st.error(f"Error: {e}")

# Function to download Facebook videos
def download_facebook_video(url, quality, save_path='downloads'):
    format_map = {
        "Best Available": "best",
        "Low": "worst",
        "Medium": "best[height<=720]",
        "High": "best[height<=1080]"
    }
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'format': format_map.get(quality, 'best'),
        'progress_hooks': [progress_hook]
    }
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.info(f"Starting download from Facebook...")
            ydl.download([url])
            st.success("Download completed!")
            progress_bar.empty()  # Clear progress bar after completion
            progress_text.empty()  # Clear text after completion
    except Exception as e:
        st.error(f"Error: {e}")
        progress_bar.empty()  # Clear progress bar in case of error
        progress_text.empty()  # Clear text in case of error

# Main download button with custom icon
download_button = st.button("Download Video 📥")

# Clear button
clear_button = st.button("Clear All Fields ❌")

# Main download logic
if download_button:
    if platform == "YouTube":
        download_youtube_video(url, video_quality, save_path, file_format)
    elif platform == "Instagram":
        download_instagram_content(url, save_path)
    elif platform == "Facebook":
        download_facebook_video(url, video_quality, save_path)
    else:
        st.error("Invalid platform selection!")

# Clear all inputs when the clear button is clicked
if clear_button:
    st.experimental_rerun()
