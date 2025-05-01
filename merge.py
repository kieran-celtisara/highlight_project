import subprocess

# Step 1: Create the file list for FFmpeg
with open("filelist.txt", "w") as f:
    f.write("file 'clip1.mp4'\n")
    f.write("file 'clip2.mp4'\n")

# Step 2: Run the FFmpeg command
cmd = [
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", "filelist.txt",
    "-c", "copy",
    "merged.mp4"
]

# Step 3: Execute FFmpeg
try:
    subprocess.run(cmd, check=True)
    print("✅ Merge complete! Output: merged.mp4")
except subprocess.CalledProcessError as e:
    print("❌ FFmpeg failed:", e)