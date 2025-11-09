# Youtube Music Download
A simple script to download free music from YouTube using `yt-dlp` and `ffmpeg`. It will output a `.m4a` file with metadatas : title (russian to english autotranslation), artist and square thumbnail.
## Requirements
- Python 3.x
- `yt-dlp` (YouTube downloader)
- `ffmpeg` (for audio conversion)
## Installation
  1. Clone the repository
2. Install the required packages
   ```bash
   pip install os mutagen.mp4 PIL translate
   ```
3. Make sure `ffmpeg` is installed in the newly created ffmpeg folder and accessible in your system's PATH.
## Usage
1. Run the script with a YouTube URL music or a playlist URL in the links.txt file.
   ```bash
   python ytdlscript.py
   ```
