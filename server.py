from pathlib import Path
from threading import Thread
import json, subprocess, shutil, uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from processor.render import render

ROOT=Path(__file__).resolve().parent
JOBS=ROOT/'jobs';JOBS.mkdir(exist_ok=True)
app=FastAPI(title='Mystery Marble Studio V20 Local Processor')
state={}
@app.post('/api/process')
async def process(file:UploadFile=File(...), fps:int=Form(12), size:int=Form(640), spacing:int=Form(7), goal:str=Form('')):
    if not 1<=fps<=30 or not 256<=size<=1280 or not 3<=spacing<=20:raise HTTPException(400,'Invalid settings')
    job=uuid.uuid4().hex[:12]; folder=JOBS/job;folder.mkdir()
    suffix=Path(file.filename or 'clip.mp4').suffix.lower()
    if suffix not in ('.mov','.mp4','.m4v','.avi'):raise HTTPException(400,'Use a video file')
    source=folder/('input'+suffix)
    with source.open('wb') as out:shutil.copyfileobj(file.file,out)
    try:
        rect=[float(n) for n in goal.split(',')] if goal.strip() else None
        if rect and (len(rect)!=4 or not all(0<=v<=1 for v in rect)):raise ValueError()
    except ValueError:raise HTTPException(400,'Goal must be x,y,width,height between 0 and 1')
    state[job]={'status':'queued','progress':'Waiting'}
    def work():
        try:
            state[job].update(status='processing')
            def report(i,n):state[job]['progress']=f'{i}/{n} frames ({round(i/max(1,n)*100)}%)'
            intermediate=folder/'raw.mp4';output=folder/'result.mp4'
            meta=render(source,intermediate,report,fps,size,spacing,rect)
            # H.264 conversion for iPhone / web compatibility.
            cmd=['ffmpeg','-y','-loglevel','error','-i',str(intermediate),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
            result=subprocess.run(cmd,capture_output=True,text=True)
            if result.returncode!=0:raise RuntimeError('ffmpeg H.264 conversion failed: '+result.stderr[-500:])
            (folder/'metadata.json').write_text(json.dumps(meta,indent=2))
            state[job].update(status='complete',progress='Finished',metadata=meta)
        except Exception as e:state[job].update(status='error',error=str(e))
    Thread(target=work,daemon=True).start()
    return {'job_id':job}
@app.get('/api/status/{job}')
def status(job:str):
    if job not in state:raise HTTPException(404,'Job not found')
    return state[job]
@app.get('/api/download/{job}')
def download(job:str):
    path=JOBS/job/'result.mp4'
    if not path.is_file():raise HTTPException(404,'Not ready')
    return FileResponse(path,media_type='video/mp4',filename='mystery-marble-v20.mp4')
app.mount('/',StaticFiles(directory=ROOT/'web',html=True),name='web')
