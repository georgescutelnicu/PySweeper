import webbrowser
import winsound


def open_github():
    """
    Open the GitHub repository for the PySweeper project.
    """

    github_url = "https://github.com/georgescutelnicu/PySweeper"
    webbrowser.open(github_url)


def play_sound(sound_path):
    """
    Play a sound file.

    Parameters:
    - sound_path (str): The path to the sound file.
    """

    winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
