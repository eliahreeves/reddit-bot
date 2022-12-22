import subprocess
import pull_images
import errors

def upload_video(post_id, subreddit, title, number_of_videos):
    '''
    Spawns a child process and communicates to it via stdin and stdout
    Calls get_auth_token to parse url and retreive token
    '''
    for i in range(number_of_videos):
        if number_of_videos > 1:
            vid_title = title + f' Part {i + 1}'
        # Spawn subprocess to upload videos, set up communication
        print(str(f'completed_videos/{post_id}_v{i}.mp4'), str(subreddit), str(vid_title))
        p = subprocess.Popen(['python3', 'youtube_child.py', str(f'completed_videos/{post_id}_v{i}.mp4'), str(subreddit), str(vid_title)], 
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Scan output for url and parse it
        url = ''
        while True:
            a = p.stdout.readline().decode('utf-8')
            if not a == '': print(a)
            if 'http' in a:
                url = a.split(' ')[-1:][0].strip('\n')
                break

        # Get the authentication token from the url
        codein = pull_images.GetAuthToken(url)

        if type(codein) == errors.BotError:
            codein.log()
            p.communicate(input='\n'.encode())[0]
            return

        
        # Send to the child 
        output = p.communicate(input=codein.encode())[0]
        print(output.decode('utf-8'))