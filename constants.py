from enum import Enum, auto
import api_keys.secrets as s

#general control keys
MULTI_PART_VIDEOS = True
MAX_PARTS = 2
BUFFER_CONSTANT = 10
MAX_VIDEO_LENGTH = 60
ALLOWABLE_BODY_LENGTH = 20      #number of characters a comment based post is allowed to have in the body
ALLOWABLE_TITLE_LENGTH = MAX_VIDEO_LENGTH / 3
MINIMUM_NUMBER_OF_COMMENTS = 2  #min comments in a post
MAX_NUMBER_OF_COMMENTS = 12  #max comments to use
#praw keys
USER_AGENT = 'Scraper'
CLIENT_ID = s.CLIENT_ID
CLIENT_SECRET = s.CLIENT_SECRET
#google log in
GOOGLE_EMAIL = s.GOOGLE_EMAIL
GOOGLE_PASSWORD = s.GOOGLE_PASSWORD

#types of reddit
COMMENT_BASED = ['AskReddit']
POST_BODY_BASED = ['tifu', 'AITAH']

#gTTS constants
LANG = 'en'
SLOW = False
#pytts3x constants
RATE = 240
VOICE = 1 #0 Male, 1 Female
VOLUME = 1.0 #Between 0.0 and 1.0
#moviepy constants
VIDEO_FPS = 30
COMMENT_OPACITY = 0.9
BACKGROUND_CLIP = 'background_clips/background1.mp4'
FINAL_VID_SPEED = 1.0 #speed mulitplier for the final video

# Constants for error types
class ErrorType(Enum):
    NO_ERROR = auto()
    NONE_ERROR = auto()
    NSFW_ERROR = auto()
    VIDEO_TYPE_ERROR = auto()
    LENGTH_ERROR = auto()
    BODY_TOO_LONG_ERROR = auto()
    PINNED_ERROR = auto()
    UPLOAD_ERROR = auto()

# Message to display for error type
messages = {ErrorType.NO_ERROR:   "NO ERRORS",
            ErrorType.NONE_ERROR: "RETURNED A NONE TYPE",
            ErrorType.NSFW_ERROR: "DETECTED NSFW CONTENT",
            ErrorType.LENGTH_ERROR: "VIDEO LENGTH IS MORE OR LESS THEN ALLOWED LIMIT",
            ErrorType.BODY_TOO_LONG_ERROR: "THIS VIDEO IS LIKELY PINNED",
            ErrorType.VIDEO_TYPE_ERROR: "VIDEO TYPE NOT DISCERNABLE",
            ErrorType.PINNED_ERROR: "THIS POST IS PINNED",
            ErrorType.UPLOAD_ERROR: "FAILED TO UPLOAD VIDEO"}

# Max tries to get auth code for video upload
MAX_GET_AUTH_TRIES = 5