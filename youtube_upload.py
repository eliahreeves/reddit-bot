import subprocess
import pull_images
import Errors

def upload_video(filepath, subreddit, title):
    '''
    Spawns a child process and communicates to it via stdin and stdout
    Calls get_auth_token to parse url and retreive token
    '''

    # Spawn subprocess to upload videos, set up communication
    print(str(filepath), str(subreddit), str(title))
    p = subprocess.Popen(['python3', 'youtube_child.py', str(filepath), str(subreddit), str(title)], 
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

    if type(codein) == Errors.BotError:
        codein.log()
        p.communicate(input='\n'.encode())[0]
        return

    
    # Send to the child 
    output = p.communicate(input=codein.encode())[0]
    print(output.decode('utf-8'))