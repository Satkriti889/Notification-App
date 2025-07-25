from plyer import notification
import pygame
import time

def send_notification(title, message, sound_file):
    # Show desktop notification
    notification.notify(
        title=title,
        message=message,
        timeout=5  # seconds
    )

    # Play sound
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    time.sleep(3)  # wait for sound to finish

# Main logic
if __name__ == "__main__":
    title = "Hydration Reminder"
    message = "Time to drink some water!"
    sound_file = "notification.wav"  # Must exist in same folder

    while True:
        send_notification(title, message, sound_file)
        time.sleep(60 * 60)  # every hour (change to 10 for testing)
