import fbdown
import wget
import os

def downlaod_videos_new(url, name):
    if "downloads/{name}" not in os.listdir():
                try:
                    os.mkdir(f'downloads/{name}/')
                except:
                    pass
                try:
                    os.mkdir(f'downloads/{name}/videos')
                except:
                    pass
    try:
        a = fbdown.get(url)
        d = fbdown.getdownlink(url)
        wget.download(d, out=f'downloads/{name}/videos/')
    except:
        print("This is Private Video.")