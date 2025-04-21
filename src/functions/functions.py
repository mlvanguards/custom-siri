import subprocess
import webbrowser

import psutil

# -------------- Tool Functions ------------------


def lock_screen() -> str:
    try:
        subprocess.run(["pmset", "displaysleepnow"])
        return "Screen locked"
    except Exception as e:
        return f"Failed to lock screen: {e}"


def get_battery_status() -> dict:
    try:
        battery = psutil.sensors_battery()
        return {"percent": battery.percent, "charging": battery.power_plugged}
    except Exception as e:
        return {"error": str(e)}


def search_google(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searched for: {query}"
    except Exception as e:
        return f"Failed to search: {e}"


def set_volume(level: int) -> str:
    try:
        subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
        return f"Volume set to {level}%"
    except Exception as e:
        return f"Failed to set volume: {e}"


def create_note(title: str, content: str) -> str:
    try:
        # First, open the Notes app
        subprocess.Popen(["open", "-a", "Notes"])

        # Create an AppleScript to create a new note with the title and content
        applescript = f'''
        tell application "Notes"
            tell account "iCloud"
                make new note with properties {{name:"{title}", body:"{content}"}}
            end tell
            activate
        end tell
        '''

        # Execute the AppleScript
        subprocess.run(["osascript", "-e", applescript])
        return f"Note created: {title} - {content}"
    except Exception as e:
        return f"Failed to create note: {e}"


available_function_calls = {
    "lock_screen": lock_screen,
    "get_battery_status": get_battery_status,
    "search_google": search_google,
    "set_volume": set_volume,
    "create_note": create_note,
}
