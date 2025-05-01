from fastapi import FastAPI, UploadFile, File
import psycopg2
import subprocess
import shutil
import os
from datetime import date
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Database connection settings
DB_NAME = "postgres"
DB_USER = "postgres.ecgtfnppbzlwjeqhvskn"
DB_PASSWORD = "hxESAkVzfXBayO76"
DB_HOST = "aws-0-us-east-1.pooler.supabase.com"
DB_PORT = "6543"

# Function to get clips from the database
def get_clips_from_db(player_names: List[str]):
    
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    # Example query
    cur = conn.cursor()
    cur.execute('SELECT * FROM "HighlightClips" WHERE players_arr && %s;', (player_names,))
    rows = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()
    return rows
def download_videos(video_urls):
    local_paths = []
    os.makedirs("temp", exist_ok=True)  # Ensure temp folder exists
    for i, url in enumerate(video_urls):
        local_path = f"temp/clip_{i}.mp4"
        with requests.get(url, stream=True) as r:
            r.raise_for_status()  # Fail fast if download error
            with open(local_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        # Confirm file was written
        if not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
            raise RuntimeError(f"Download failed or file is empty: {local_path}")
        local_paths.append(local_path)
    return local_paths
def merge_with_ffmpeg(file_list_path):
    output_path = "temp/merged.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", file_list_path,
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path
def write_ffmpeg_filelist(local_paths):
    file_list_path = "temp/filelist.txt"
    with open(file_list_path, "w", encoding="utf-8") as f:
        for path in local_paths:
            abs_path = os.path.abspath(path)
            f.write(f"file '{abs_path}'\n")
    return file_list_path

@app.get("/video")
def get_merged_video():
    return FileResponse("temp/merged.mp4", media_type="video/mp4")
# API endpoint to merge clips
@app.post("/merge")
async def merge_videos(player_names: List[str]):
    # Step 1: Get clips from the database
    clips_to_merge = get_clips_from_db(player_names)
    video_urls = [row[3] for row in clips_to_merge]
    local_paths = download_videos(video_urls)
    print(len(local_paths))
    if len(local_paths) == 0:
        return {"message": "No clips found for the specified players"}
    print("test")
    file_list_path = write_ffmpeg_filelist(local_paths)
    print(local_paths, file_list_path)
    output_path = merge_with_ffmpeg(file_list_path)
    print(output_path)
    return {"message": "Merged successfully", "output_file": output_path}
    
    # print(clips_to_merge)
    # if not clips_to_merge:
    #     return {"message": "No clips found for the specified players"}
    
    # # Step 2: Create a temp directory to store the files
    # os.makedirs("temp", exist_ok=True)
    
    # # Create a file list for ffmpeg
    # file_list_path = "temp/filelist.txt"
    # with open(file_list_path, "w") as f:
    #     for i, clip in enumerate(clips_to_merge):
    #         f.write(f"file '{clip}'\n")

    # # Step 3: Merge clips with FFmpeg
    # output_path = "temp/merged.mp4"
    # cmd = [
    #     "ffmpeg", "-y",
    #     "-f", "concat", "-safe", "0",
    #     "-i", file_list_path,
    #     "-c", "copy",
    #     output_path
    # ]
    
    # subprocess.run(cmd, check=True)

    # # Return the path to the merged file
    # return {"message": "Merged successfully", "output_file": output_path}
