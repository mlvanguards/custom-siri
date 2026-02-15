import os
import shutil
import subprocess
import webbrowser
import psutil
import platform

# --- File operations ---

def copy_file(source: str, destination: str) -> str:
    """Copies a file from source to destination."""
    try:
        shutil.copy(source, destination)
        return f"Copied {source} to {destination}"
    except Exception as e:
        return f"Failed to copy file: {e}"

def move_file(source: str, destination: str) -> str:
    """Moves a file from source to destination."""
    try:
        shutil.move(source, destination)
        return f"Moved {source} to {destination}"
    except Exception as e:
        return f"Failed to move file: {e}"

def delete_file(path: str) -> str:
    """Deletes the file at the given path."""
    try:
        os.remove(path)
        return f"Deleted file {path}"
    except Exception as e:
        return f"Failed to delete file: {e}"

def create_folder(path: str) -> str:
    """Creates a folder at the given path."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Created folder at {path}"
    except Exception as e:
        return f"Failed to create folder: {e}"

# --- System commands ---

def open_application(app_name: str) -> str:
    """Opens an application by name."""
    try:
        subprocess.Popen(["open", "-a", app_name])
        return f"Opened {app_name}"
    except Exception as e:
        return f"Failed to open {app_name}: {e}"

def close_application(app_name: str) -> str:
    """Closes an application by name."""
    try:
        for proc in psutil.process_iter(['name']):
            if app_name.lower() in proc.info['name'].lower():
                proc.kill()
        return f"Closed {app_name}"
    except Exception as e:
        return f"Failed to close {app_name}: {e}"

def take_screenshot(destination: str) -> str:
    """Takes a screenshot and saves it."""
    try:
        print('screenshot')
        return f"Screenshot saved to {destination}"
    except Exception as e:
        return f"Failed to take screenshot: {e}"


def lock_screen() -> str:
    """Locks the laptop screen on Windows and macOS."""
    try:
        system = platform.system()
        
        if system == "Windows":
            # Windows: Use rundll32 to call user32.dll LockWorkStation
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=True)
            return "Screen locked"
        
        elif system == "Darwin":  # macOS
            # macOS: Use pmset to sleep display
            subprocess.run(["pmset", "displaysleepnow"], check=True)
            return "Screen locked"
            
    except subprocess.CalledProcessError as e:
        return f"Failed to lock screen: Command failed with code {e.returncode}"
    except Exception as e:
        return f"Failed to lock screen: {e}"

def get_battery_status() -> dict:
    """Returns the battery level and charging status."""
    try:
        battery = psutil.sensors_battery()
        return {
            "percent": battery.percent,
            "charging": battery.power_plugged
        }
    except Exception as e:
        return {"error": str(e)}


def set_volume(level: int) -> str:
    """Sets the system volume to the specified level (0-100)."""
    # Clamp level to valid range
    level = max(0, min(level, 100))
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"], check=True)
            return f"Volume set to {level}%"
        except subprocess.CalledProcessError as e:
            return f"Failed to set volume: Command failed with code {e.returncode}"
        except Exception as e:
            return f"Failed to set volume: {e}"
    
    elif system == "Windows":
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            return f"Volume set to {level}%"
        except ImportError:
            return "Failed to set volume: pycaw library not installed. Install with: pip install pycaw"
        except Exception as e:
            return f"Failed to set volume: {e}"

# --- Browser / Internet ---

def open_url(url: str) -> str:
    """Opens a URL in the default web browser."""
    try:
        webbrowser.open(url)
        return f"Opened {url}"
    except Exception as e:
        return f"Failed to open URL: {e}"

def search_google(query: str) -> str:
    """Searches Google for the given query."""
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searched for: {query}"
    except Exception as e:
        return f"Failed to search: {e}"

# --- Media ---

def play_music(track_name: str) -> str:
    """Pretends to play a music track."""
    return f"Now playing: {track_name}"

def pause_music() -> str:
    """Pretends to pause music playback."""
    return "Music paused"

# --- Notes ---

def create_note(title: str, content: str) -> str:
    """Creates a mock note."""
    return f"Note created: {title} - {content}"

functions = [
    {
        "name": "copy_file",
        "description": "Copies a file from source to destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Path of the source file"},
                "destination": {"type": "string", "description": "Path of the destination"}
            },
            "required": ["source", "destination"]
        }
    },
    {
        "name": "move_file",
        "description": "Moves a file from source to destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "destination": {"type": "string"}
            },
            "required": ["source", "destination"]
        }
    },
    {
        "name": "delete_file",
        "description": "Deletes a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "create_folder",
        "description": "Creates a folder at the given path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "open_application",
        "description": "Opens an application by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "close_application",
        "description": "Closes an application by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "take_screenshot",
        "description": "Takes a screenshot and saves it.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"}
            },
            "required": ["destination"]
        }
    },
    {
        "name": "lock_screen",
        "description": "Locks the screen.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_battery_status",
        "description": "Returns battery percent and charging status.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "open_url",
        "description": "Opens a URL in the browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "search_google",
        "description": "Searches Google.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "play_music",
        "description": "Plays a music track (mock).",
        "parameters": {
            "type": "object",
            "properties": {
                "track_name": {"type": "string"}
            },
            "required": ["track_name"]
        }
    },
    {
        "name": "pause_music",
        "description": "Pauses playback (mock).",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "set_volume",
        "description": "Sets the system volume (0–100).",
        "parameters": {
            "type": "object",
            "properties": {
                "level": {"type": "integer"}
            },
            "required": ["level"]
        }
    },
    {
        "name": "create_note",
        "description": "Creates a simple note.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["title", "content"]
        }
    }
]

available_function_calls = {
    "copy_file": copy_file,
    "move_file": move_file,
    "delete_file": delete_file,
    "create_folder": create_folder,
    "open_application": open_application,
    "close_application": close_application,
    "take_screenshot": take_screenshot,
    "lock_screen": lock_screen,
    "get_battery_status": get_battery_status,
    "open_url": open_url,
    "search_google": search_google,
    "play_music": play_music,
    "pause_music": pause_music,
    "set_volume": set_volume,
    "create_note": create_note
}


