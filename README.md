# Advanced Telegram VC Music Bot

A premium, modular, and high-performance Telegram Voice Chat Music Bot built with Python, Pyrogram, and Py-TgCalls.

## Features

- **Voice Chat Streaming**: High-quality audio streaming from YouTube and other sources.
- **No Paid APIs**: Uses `yt-dlp` for search and extraction.
- **Advanced Queue**: Managed via MongoDB for persistence.
- **Admin System**: Secure admin controls and DJ mode.
- **Config Cloning**: Export and import group settings easily.
- **Modular**: Easy to extend with new plugins.
- **Filters**: Bassboost, nightcore, and more.
- **Playlists**: Personal and group playlists.
- **Lyrics**: Scraped from open-source providers.

## Setup

1. **Clone the repo**
2. **Install requirements**: `pip install -r requirements.txt`
3. **Configure Environment**: Create a `.env` file based on `.env.example`.
4. **Run the bot**: `python3 main.py`

## Commands

- `/play <song>`: Play a song in VC.
- `/pause`: Pause playback.
- `/resume`: Resume playback.
- `/skip`: Skip to next song.
- `/stop`: Stop playback and clear queue.
- `/queue`: Show current queue.
- `/filter`: List available audio filters.
- `/lyrics <song>`: Get song lyrics.
- `/exportconfig`: Export group settings.
- `/importconfig`: Import group settings.

## Deployment

### VPS
```bash
sudo apt update && sudo apt install ffmpeg -y
python3 main.py
```

### Docker
```bash
docker-compose up -d
```
