import streamlit as st
from plyer import notification
import pygame
import time
import threading
import os

# Initialize session state for threading
if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()
    st.session_state.thread = None

# Folder where your sounds are stored
SOUNDS_DIR = "sounds"

# List available sound files in the folder
available_sounds = [f for f in os.listdir(SOUNDS_DIR) if f.endswith((".wav", ".mp3"))]

# Function to show notification and play sound
def send_notification(title, message, sound_file):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    time.sleep(3)

# Threaded notification loop
def start_notifier(title, message, sound_file, interval, stop_event):
    while not stop_event.is_set():
        send_notification(title, message, sound_file)
        if stop_event.wait(interval):
            break

# Streamlit UI
st.title("🔔 Notification App with Sound")

title = st.text_input("Notification Title", "Hydration Reminder")
message = st.text_input("Notification Message", "Time to drink some water!")
interval = st.number_input("Repeat Interval (seconds)", min_value=10, value=60)

# Sound selection dropdown
selected_sound = st.selectbox("Select Notification Sound", available_sounds)

sound_file = os.path.join(SOUNDS_DIR, selected_sound)

# Sound Preview Button
if st.button("🔊 Preview Sound"):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        time.sleep(3)
        st.success("Sound played successfully!")
    except Exception as e:
        st.error(f"Error playing sound: {e}")

# Test Notification Button
if st.button("🧪 Send Test Notification"):
    try:
        send_notification(title, message, sound_file)
        st.success("Test notification sent!")
    except Exception as e:
        st.error(f"Error sending test notification: {e}")

# Start/Stop buttons
col1, col2 = st.columns(2)

if col1.button("▶ Start Notification"):
    if st.session_state.thread is None or not st.session_state.thread.is_alive():
        st.session_state.stop_event.clear()
        thread = threading.Thread(
            target=start_notifier,
            args=(title, message, sound_file, interval, st.session_state.stop_event),
            daemon=True
        )
        thread.start()
        st.session_state.thread = thread
        st.success("Notifications started!")

if col2.button("⏹ Stop Notification"):
    if st.session_state.thread and st.session_state.thread.is_alive():
        st.session_state.stop_event.set()
        st.warning("Notifications will stop shortly.")
