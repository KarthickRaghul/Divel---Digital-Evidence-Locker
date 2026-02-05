from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os
import uuid
import sys

# Ensure we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from inference.predictor import HybridPredictor
from inference.audio import AudioForensics
from utils.url_loader import download_from_url
from utils.report_generator import generate_report

app = FastAPI(title="Deepfake Detective API", version="2.0")

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Models (Lazy load or startup)
visual_model = HybridPredictor(device='cpu') # Loads EffNet
audio_model = AudioForensics()

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "online", "system": "Deepfake Detective Hybrid Engine"}

@app.post("/analyze/upload")
async def analyze_upload(file: UploadFile = File(...)):
    try:
        # Save File
        ext = file.filename.split('.')[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(TEMP_DIR, filename)
        
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Determine Type
        is_video = ext in ['mp4', 'mov', 'avi', 'mkv']
        is_audio = ext in ['wav', 'mp3', 'flac', 'm4a']
        
        response = {
            "filename": file.filename,
            "type": "video" if is_video else ("audio" if is_audio else "image"),
            "visual_score": 0,
            "audio_score": 0,
            "final_score": 0,
            "verdict": "Unknown",
            "details": {}
        }

        # --- PIPELINE ---
        
        # 1. Audio Analysis (if video or audio)
        if is_audio or is_video:
            # Extract audio from video if needed
            audio_path = filepath
            if is_video:
                # Todo: Extract audio using ffmpeg
                # For now assuming we can extract or skip
                # We need extract_audio logic here.
                # Let's assume silent video for MPV or use moviepy if available
                # Re-implement simple extraction:
                try:
                    from moviepy.editor import VideoFileClip
                    clip = VideoFileClip(filepath)
                    if clip.audio:
                        audio_path = filepath.replace(f".{ext}", ".wav")
                        clip.audio.write_audiofile(audio_path, logger=None)
                    else:
                        audio_path = None
                except:
                    audio_path = None

            if audio_path and os.path.exists(audio_path):
                a_res = audio_model.analyze(audio_path)
                response['audio_score'] = a_res['score']
                response['details']['audio'] = a_res
        
        # 2. Visual Analysis (if video or image)
        if not is_audio:
            v_res = visual_model.predict(filepath)
            response['visual_score'] = v_res['fake_prob']
            response['details']['visual'] = {k:v for k,v in v_res.items() if k not in ['heatmap', 'original_face', 'ela_image', 'noiseprint']}
            
            # Todo: Handle Images (Heatmaps) serialization?
            # For API, we usually return URLs or Base64.
            # We will skip sending heavy images in JSON for now.

        # 3. Fusion
        if is_video and audio_path:
            # Max Evidence Fusion
            if response['visual_score'] > 0.7 or response['audio_score'] > 0.7:
                response['final_score'] = max(response['visual_score'], response['audio_score'])
            else:
                 response['final_score'] = (0.6 * response['visual_score']) + (0.4 * response['audio_score'])
        elif is_audio:
            response['final_score'] = response['audio_score']
        else:
            response['final_score'] = response['visual_score']

        # Verdict
        score = response['final_score']
        if score > 0.6: response['verdict'] = "FAKE"
        elif score > 0.4: response['verdict'] = "SUSPICIOUS"
        else: response['verdict'] = "REAL"
        
        return response

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/url")
async def analyze_url_endpoint(url: str = Form(...)):
    # use utils.url_loader
    try:
        res = download_from_url(url, save_dir=TEMP_DIR)
        if res['error']:
            return {"error": res['error']}
            
        # If success, run analysis on local file...
        # (Simplified: Just return success and path for now, or recurse)
        return {"status": "downloaded", "path": res['file_path']}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
