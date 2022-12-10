# main.py
# Functionality:
# Input:
# Output:

import praw
import constants as c
from constants import ErrorType
from gtts import gTTS
import video_handleing
import os
import pull_images
from Errors import BotError
import glob
import re
import time

import youtube_upload

sub_reddit = 'AskReddit'  #TODO maybe add a way to pull from multiple subreddits
reddit = praw.Reddit(client_id = c.CLIENT_ID, client_secret = c.CLIENT_SECRET, user_agent = c.USER_AGENT)



def FindASubReddit(): 
    '''
    This function returns a unique post ID and then stores it in the file used_posts.txt to avoid
    repeated use.
    '''

    current_sub = reddit.subreddit(sub_reddit)
    with open('used_posts.txt', 'r') as file:
        used_posts = file.readlines()
    
    used_posts = [i[:-1] for i in used_posts]

    for post in current_sub.hot():
        if str(post.id) not in used_posts:
            with open('used_posts.txt', 'a') as file:
                file.write(post.id + '\n')
            
            
            if post.over_18:    # Return error if NSFW
                current_sub = None # Housekeeping to save resources
                return BotError(ErrorType.NSFW_ERROR, "FindASubReddit")
            elif post.stickied:
                current_sub = None # Housekeeping to save resources
                return BotError(ErrorType.PINNED_ERROR, "FindASubReddit")
            else:
                current_sub = None # Housekeeping to save resources
                return (post.id, post.url)

def CollectTextShort(post_id, post_url):
    '''
    Function takes post_id and post url. searches for comments to use in the video. returns a list of comment
    ids to screenshot as well as the file path to a extra audio file needed to delete. Returning the path
    instead of just deleting it seems to ensure in will be closed and able to be removed.
    '''
    working_submision = reddit.submission(post_id)
    
    title_text = working_submision.title    #gets title and body of post
    body_text = working_submision.selftext  #Body is not needed but it is used to guess if a post is pinned

    if len(body_text) > c.ALLOWABLE_BODY_LENGTH:    #if the body text is long the post is likely pinned and should be skipped
        return BotError(ErrorType.BODY_TOO_LONG_ERROR, "CollectTextShort") 
    else:
        title_audio = gTTS(text = title_text, lang = c.LANG, slow = c.SLOW)   #converts title to mp3
        title_audio.save(f"audio_temp/{post_id}_t.mp3")
        title_audio_length = video_handleing.GetVideoLength(f"audio_temp/{post_id}_t.mp3")
        if title_audio_length > c.ALLOWABLE_TITLE_LENGTH:   #checks to ensure title is not too long
            os.remove(f"./audio_temp/{post_id}_t.mp3")
            return BotError(ErrorType.LENGTH_ERROR, "CollectTextShort")
        else:       #if its not too long script will collect comments
    
            working_submision.comments.replace_more(limit=0)    #removes comment tree so only top level comments are retrived
            working_video_length = title_audio_length
            comments_used = []  #list of comment ids that need to be screenshoted
            
            for top_level_comment in working_submision.comments:
                if not top_level_comment.stickied:  #checks if a comment is pinned
    
                    comment_id = top_level_comment.id   #gets comment text and ID
                    comment_text = top_level_comment.body
                    comment_text = re.sub(r'http\S+', '', comment_text) #removes urls from comments 
                    comment_audio = gTTS(text = comment_text, lang = c.LANG, slow = c.SLOW)
                    comment_audio.save(f"audio_temp/{post_id}_{comment_id}.mp3")
                    comments_used.append(comment_id)    #adds each comment looked at to the list
                    working_video_length += video_handleing.GetVideoLength(f"audio_temp/{post_id}_{comment_id}.mp3")
                    
                    if working_video_length >= c.MAX_VIDEO_LENGTH:  #checks if a video will be too long
                        comments_used.remove(comment_id)    #removes the comment that will put the video over the limit
                        
                        if len(comments_used) < c.MINIMUM_NUMBER_OF_COMMENTS:  #checks if there are enough comments
                            return BotError(ErrorType.LENGTH_ERROR, "CollectTextShort")
                        pull_images.main('C', post_id, post_url, comments_used) #calls screenshot function
                        return comments_used, (f"./audio_temp/{post_id}_{comment_id}.mp3"), title_text # Title for uploading

def CollectTextLong(post_id, post_url):
    '''
    This function takes the post Id found by FindASubReddit() then it collects text and converts it to audio.
    I chose to collect the audio in this step in oreder to do a more accurate duration check. This function
    also will allow the program to produce both story and comment based videos.
    '''
    working_submision = reddit.submission(post_id)


    title_text = working_submision.title       #gets title and body of reddit post
    body_text = working_submision.selftext

    title_audio = gTTS(text = title_text, lang = c.LANG, slow = c.SLOW)   #converts title to mp3
    title_audio.save(f"audio_temp/{post_id}_t.mp3")

    body_audio = gTTS(text = body_text, lang = c.LANG, slow = c.SLOW)       #converts body to mp3
    body_audio.save(f"audio_temp/{post_id}_b.mp3")

    if IsAValidVideoBBased(post_id):
        pull_images.main('B', post_id, post_url)

    else:
        os.remove(f"./audio_temp/{post_id}_t.mp3")
        os.remove(f"./audio_temp/{post_id}_b.mp3")
        
        return BotError(ErrorType.LENGTH_ERROR, "CollectTextLong")

def IsAValidVideoBBased(post_id):
    '''
    post id is iputed directly and use to find stored audio files. Audio file length is
    calculated by GetVidoeLength module and then lenght of title and body are added.
    if lenght is more then the value of c.MAX_VIDEO_LENGHTH the function returns False
    otherwise True.
    '''
    title_duration = video_handleing.GetVideoLength(f"audio_temp/{post_id}_t.mp3")
    body_duration = video_handleing.GetVideoLength(f"audio_temp/{post_id}_b.mp3")

    return not title_duration + body_duration > c.MAX_VIDEO_LENGTH

# Main loop to find posts and make videos with them
def CleanUpTempFiles(path):
    '''
    Deletes all files in inputed folder
    '''
    time.sleep(2)
    files = glob.glob(f'{path}/*')
    for f in files:
        os.remove(f)

while True:
    ### Collect necessary data
    post_info = FindASubReddit()

    # If an Error was returned, log it and move on to next post
    if type(post_info) == BotError:
        post_info.log()
        continue

    # Try to access post info, log error if unsucessful and move on
    try:
       post_info[0] == post_info[0]
    except TypeError:
        BotError(ErrorType.NONE_ERROR, "Main Loop - Data collection").log()
        continue

    #if post is not nsfw and exists continue with the code 
    post_id = post_info[0]
    post_url = post_info[1]
    print(post_id)
    print(post_url)

    if sub_reddit in c.COMMENT_BASED:               #for short form comment based posts
        collect_text_short_returned = CollectTextShort(post_id, post_url) #comment list, file path to delete

        if type(collect_text_short_returned) == BotError:
            CleanUpTempFiles('image_temp')      #remove temporary files
            CleanUpTempFiles('audio_temp')
            continue
        os.remove(collect_text_short_returned[1])           #removes extra audio file from collection process
        video_handleing.CompileCommentBasedVideo(post_id, collect_text_short_returned[0])       #compiles video into final product
        CleanUpTempFiles('image_temp')      #remove temporary files
        CleanUpTempFiles('audio_temp')

    elif sub_reddit in c.POST_BODY_BASED:          #for long form story based posts
        if type(CollectTextLong(post_id, post_url)) == BotError:
            continue
    else:
        BotError(ErrorType.VIDEO_TYPE_ERROR, "Main Loop - Data collection").log()

    ### Post to youtube
    youtube_upload.upload_video(f'completed_videos/{post_id}.mp4', sub_reddit, collect_text_short_returned[2])

    ### Control logic to determine whether to create more or not
    CleanUpTempFiles('completed_videos')
    if True: # Currently only makes one for debugging purposes
        reddit = None # Housekeeping to save resources
        break