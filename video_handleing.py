import moviepy.editor as mp
import PIL
from PIL import Image
import constants as c

def GetVideoLength(filepath):
    '''
    input is the file path to a video, output is the duration of the video
    '''
    return mp.AudioFileClip(filepath).duration      #uses moviepy to get duration

def CompileCommentBasedVideo(post_id, comment_ids):
    '''
    input is the id of the main post and the list of the comment ids. Resizes screen shots 
    based on if the image is has a larger width or height. Adjusts opacity to c.COMMENT_OPACITY 
    Images expressed as moviepy image clips with duration as the coresponding audio clip.
    These image clips are concated and layered over a backgroung clip stored in c.BACKGROUND_CLIP
    video is written to the complete_videos folder with fps set to c.VIDEO_FPS
    '''
    #adds the title image clip to the list to concate. title is diffrent because file path doesnot contain comment id
    title_path = f'image_temp/{post_id}.png'    #sets file path of screenshot
    title_audio = mp.AudioFileClip(f'audio_temp/{post_id}_t.mp3')   #makes moviepy audio clip from mp3
    background = mp.VideoFileClip(c.BACKGROUND_CLIP)
    background_size = background.size
    title = mp.ImageClip(title_path).set_duration(title_audio.duration)     #create moviepy image clip
    #resize and change opacity of image clip then add to list of videos
    img = PIL.Image.open(title_path)
    wid, hgt = img.size
    scaleFactor = 1780/hgt
    if scaleFactor * wid > 940:
        title = title.resize(width = int(background_size[0] * 0.87))
    else:
        title = title.resize(height = int(background_size[1] * 0.92))
    title = title.set_opacity(c.COMMENT_OPACITY)
    title.audio = title_audio
    clip_list = [title]

    for i in comment_ids:
        comment_path = f'image_temp/{post_id}_{i}.png'  #sets file path of screenshot
        comment_audio = mp.AudioFileClip(f'audio_temp/{post_id}_{i}.mp3')   #makes moviepy audio clip from mp3


        comment = mp.ImageClip(comment_path).set_duration(comment_audio.duration)   #create moviepy image clip
        #resize and change opacity of image clip then add to list of videos
        img = PIL.Image.open(comment_path)
        wid, hgt = img.size
        scaleFactor = 1780/hgt
        if scaleFactor * wid > 940:
            comment = comment.resize(width = int(background_size[0] * 0.87))
        else:
            comment = comment.resize(height = int(background_size[1] * 0.92))
        comment = comment.set_opacity(c.COMMENT_OPACITY)
        clip_list.append(comment)
        comment.audio = comment_audio
    #compiles video from previous steps
    previd = mp.concatenate(clip_list, method="compose")    #concation step
    background = background.set_duration(previd.duration)  #cuts background video to correct length
    video = mp.CompositeVideoClip([background, previd.set_position("center")])  #overlays the comments on background
    video = video.fx( mp.vfx.speedx, c.FINAL_VID_SPEED)
    video.write_videofile(f'completed_videos/{post_id}.mp4', fps=c.VIDEO_FPS)   #saves the video
