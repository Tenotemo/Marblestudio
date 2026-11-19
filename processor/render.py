"""Offline football-to-marble renderer. Requires Ultralytics segmentation model weights.
This is an experimental pipeline, not a validated football tracking solution.
"""
import argparse
import json
import math
from pathlib import Path
import cv2
import numpy as np


def render(input_path, output_path, progress=None, fps=24, size=640, spacing=7, goal=None):
    from ultralytics import YOLO
    # Weights download on first run. CPU works but can be slow.
    model = YOLO('yolo11n-seg.pt')
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError('Could not decode video. Convert to H.264 MP4 and try again.')
    source_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if not width or not height:
        raise RuntimeError('Video dimensions unavailable')
    scale = min(1., size/max(width,height))
    w = max(2, int(width*scale)//2*2); h = max(2,int(height*scale)//2*2)
    fps = min(int(fps), int(max(1,round(source_fps))))
    writer = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*'mp4v'), fps, (w,h))
    if not writer.isOpened():
        raise RuntimeError('Could not create output MP4')
    # Sample original footage at output timestamps, preserving original duration.
    duration = (total/source_fps) if total else 0
    count = int(math.ceil(duration*fps)) if duration else 0
    last_mask = None
    last_cut = -999
    prev_gray = None
    # A goal rectangle can be supplied as normalized x,y,width,height.
    ball_history = []
    for j in range(count):
        t = j/fps
        cap.set(cv2.CAP_PROP_POS_MSEC, t*1000)
        ok, frame = cap.read()
        if not ok: break
        frame = cv2.resize(frame, (w,h), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Avoid false cuts from rapid player motion; require major global change + cooldown.
        cut = False
        if prev_gray is not None and j-last_cut > fps//2:
            difference = np.mean(cv2.absdiff(cv2.resize(gray,(80,45)), cv2.resize(prev_gray,(80,45))))
            if difference > 65:
                cut = True; last_cut=j
        prev_gray=gray
        if cut: last_mask=None
        results = model.track(frame, persist=not cut, tracker='bytetrack.yaml', verbose=False, imgsz=640, conf=0.18)[0]
        person_mask = np.zeros((h,w),np.uint8)
        balls=[]
        if results.boxes is not None:
            classes=results.boxes.cls.cpu().numpy().astype(int)
            boxes=results.boxes.xyxy.cpu().numpy()
            masks=results.masks.data.cpu().numpy() if results.masks is not None else None
            for k,(cls,box) in enumerate(zip(classes,boxes)):
                if cls == 0 and masks is not None and k < len(masks):
                    m=cv2.resize(masks[k],(w,h),interpolation=cv2.INTER_LINEAR)
                    person_mask=np.maximum(person_mask,(m>0.45).astype(np.uint8)*255)
                elif cls == 32:  # COCO sports ball, not guaranteed to be football
                    x1,y1,x2,y2=box
                    balls.append(((x1+x2)/2,(y1+y2)/2))
        # Temporal carry-over only when still broadly plausible; no large ghosting.
        if last_mask is not None and not cut:
            person_mask=np.maximum(person_mask,(last_mask*0.30).astype(np.uint8))
        last_mask=person_mask.copy()
        bg=np.zeros((h,w,3),np.uint8)
        bg[:]=(17,18,23)
        cv2.line(bg,(0,int(h*.89)),(w,int(h*.89)),(37,39,47),1,cv2.LINE_AA)
        if goal:
            gx,gy,gw,gh=goal
            a=(int(gx*w),int(gy*h)); b=(int((gx+gw)*w),int((gy+gh)*h))
            cv2.rectangle(bg,a,b,(198,202,211),2,cv2.LINE_AA)
            for x in range(a[0]+10,b[0],12):cv2.line(bg,(x,a[1]),(x,b[1]),(55,59,67),1)
            for y in range(a[1]+10,b[1],12):cv2.line(bg,(a[0],y),(b[0],y),(55,59,67),1)
        # Draw silver/black metallic spheres inside segmentation mask.
        for y in range(spacing//2,h,spacing):
            for x in range(spacing//2,w,spacing):
                if person_mask[y,x] < 100:continue
                r=max(1,int(spacing*.38))
                shade=88+int(55*(.5+.5*math.sin(x*.17+y*.13)))
                cv2.circle(bg,(x,y),r,(shade,shade,shade),-1,cv2.LINE_AA)
                cv2.circle(bg,(x-max(1,r//3),y-max(1,r//3)),max(1,r//3),(225,226,231),-1,cv2.LINE_AA)
                cv2.circle(bg,(x,y),r,(30,31,37),1,cv2.LINE_AA)
        if balls:
            # Sports ball detector is unreliable on small wide shots.
            bx,by=balls[0];ball_history.append([round(t,3),round(float(bx/w),4),round(float(by/h),4)])
            cv2.circle(bg,(int(bx),int(by)),max(3,spacing//2),(238,239,243),-1,cv2.LINE_AA)
        writer.write(bg)
        if progress and (j%max(1,fps)==0 or j==count-1):progress(j+1,count)
    writer.release();cap.release()
    metadata={'frames_written':j+1 if count else 0,'fps':fps,'duration_seconds':duration,'ball_detections':ball_history,'goal_overlay':goal,'notes':['Goal is manually placed; no automatic goal/net tracking.','Goalkeeper is not separately classified.','Small players and ball may be missed.','Output MP4 uses mp4v codec; convert to H.264 for Safari.']}
    return metadata

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');p.add_argument('--fps',type=int,default=24);p.add_argument('--size',type=int,default=640);p.add_argument('--spacing',type=int,default=7);p.add_argument('--goal',type=float,nargs=4)
    a=p.parse_args()
    info=render(a.input,a.output,lambda i,n:print(f'Processing {i}/{n}',flush=True),a.fps,a.size,a.spacing,a.goal)
    print(json.dumps(info,indent=2))
