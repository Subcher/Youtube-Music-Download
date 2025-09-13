import os
from mutagen.mp4 import MP4, MP4Cover
from PIL import Image
from translate import Translator

def download_videos():
    extension = "m4a"
    command_line_download = ((".\yt-dlp "
                  "--extract-audio "
                  "--audio-format ") + extension +
                 (" "
                  "--audio-quality 320K "
                  "--add-metadata "
                  "--embed-thumbnail "
                  "--convert-thumbnail png "
                  "--ffmpeg-location .\\ffmpeg\\bin -o \"%(playlist)s/"))
    file_name = "%(title)s.%(ext)s\" "
    operating_command = command_line_download + file_name

    list = []
    with open('links.txt', 'r') as file:
        list = file.readlines()
    file.close()

    for i in range(len(list)):
        commande = operating_command + list[i]
        os.system(commande)

def extract_thumbnail_from_m4a(file_path):
    try:
        audio = MP4(file_path)
        if 'covr' in audio:
            cover = audio['covr'][0]
            ext = "jpg" if cover.imageformat == MP4Cover.FORMAT_JPEG else "png"
            output_file = os.path.splitext(file_path)[0] + f".{ext}"
            with open(output_file, "wb") as img_out:
                img_out.write(cover)
            print(f"🟢 Extracted thumbnail: {output_file}")
        else:
            print(f"⚠️ No thumbnail in: {file_path}")
    except Exception as e:
        print(f"❌ Error extracting {file_path}: {e}")


def crop_center_square(img):
    width, height = img.size
    min_edge = min(width, height)
    left = (width - min_edge) // 2
    top = (height - min_edge) // 2
    right = left + min_edge
    bottom = top + min_edge
    return img.crop((left, top, right, bottom))


def crop_png(file_path):
    try:
        with Image.open(file_path) as img:
            cropped_img = crop_center_square(img)
            cropped_img.save(file_path)
            print(f"✂️ Cropped: {file_path}")
    except Exception as e:
        print(f"❌ Failed to crop {file_path}: {e}")


def embed_cover(m4a_path, image_path):
    if not os.path.exists(image_path):
        print(f"⚠️ Image missing for: {m4a_path}")
        return
    try:
        audio = MP4(m4a_path)
        with open(image_path, "rb") as img:
            cover_data = img.read()
        audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_PNG)]
        audio.save()
        print(f"✅ Embedded cover in: {m4a_path}")
    except Exception as e:
        print(f"❌ Failed to embed in {m4a_path}: {e}")


def delete_png_files(folder_path="."):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
                print(f"🗑️ Deleted: {filename}")
            except Exception as e:
                print(f"❌ Failed to delete {filename}: {e}")


def process_all_m4a_in_folder(folder_path="."):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".m4a"):
            m4a_path = os.path.join(folder_path, filename)
            base_name = os.path.splitext(filename)[0]
            png_name = base_name + ".png"
            png_path = os.path.join(folder_path, png_name)

            extract_thumbnail_from_m4a(m4a_path)
            if os.path.exists(png_path):
                crop_png(png_path)
                embed_cover(m4a_path, png_path)
            process_russian_title(m4a_path)

    # Final cleanup
    delete_png_files(folder_path)

def process_russian_title(file_path):
    try:
        title_meta = MP4(file_path)
        if '\xa9nam' in title_meta:
            title = title_meta['\xa9nam'][0]
            if any('\u0400' <= char <= '\u04FF' for char in title):
                print('🔄 Detected Russian artist, translating...')
                translated_title = Translator(provider='mymemory', from_lang='autodetect', to_lang='en').translate(title)
                title_meta['\xa9nam'] = translated_title
                title_meta['\xa9alb'] = 'Russian Pop'
                title_meta.save()
            print(f"🟢 Translated title to English: {file_path}")
        else:
            print(f"⚠️ No Title in: {file_path}")
    except Exception as e:
        print(f"❌ Error translating {file_path}: {e}")

def download_and_process():
    download_videos()
    process_all_m4a_in_folder("Download")

download_and_process()