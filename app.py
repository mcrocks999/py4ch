'''
/**
 * py4ch
 * 4chan CLI
 * Written for Python 3.6.2
 * Created by Insertish
 */
'''
import sys, html, urllib.request, io, base64, os
print('py4ch\n4chan CLI\nWritten for Python 3.6.2\nCreated by Insertish\n\n')
try:
    import requests
except:
    print("Oh no! Requests isn't installed! :(")
    y = input("Would you like to install it [Y/N]? ").lower()
    if (y=='y'):
        try:
            import pip
        except:
            print('Could not find pip! Can\'t install!')
            imput('Press any key to continue..')
        pip.pip.main(['install','requests'])
        print('\n\n')
        import requests
    else: sys.exit(0)
def download(post, board):
    try:
        try:
            print('Downloading',str(post['tim'])+post['ext'])
            d = ''
            if (os.path.isdir('./dl')): d='./dl/'
            urllib.request.urlretrieve('https://i.4cdn.org/'+board+'/'+str(post['tim'])+post['ext'],d+str(post['tim'])+post['ext'])
            print('Downloaded!')
        except:
            print('Failed to download',str(post['tim'])+post['ext'])
    except:
        print('No file was attached!')
def view_image(post, board):
    try:
        try:
            image_url = 'https://i.4cdn.org/'+board+'/'+str(post['tim'])+post['ext']
            import tkinter as tk
            root = tk.Tk()
            root.title(image_url)
            w = post['w']+20
            h = post['h']+20
            x = 20
            y = 20
            root.geometry("%dx%d+%d+%d" % (w, h, x, y))
            image_byt = urllib.request.urlopen(image_url).read()
            image_b64 = base64.encodestring(image_byt)
            photo = tk.PhotoImage(data=image_b64)
            cv = tk.Canvas(bg='white')
            cv.pack(side='top', fill='both', expand='yes')
            cv.create_image(10, 10, image=photo, anchor='nw')
            root.mainloop()
        except:
            print('Failed to render',str(post['tim'])+post['ext'])
    except:
        print('No file was attached!')
def cmd_help():
    print('py4ch Usage:\nquit - exit py4ch\nlist - get available boards\nboard <board> [page] - get threads from board\nthread <board> <thread> [reply] [save==\'y\'] - shows the specified thread or reply\nviewer <board> <thread> - gets a thread and loops through all the replies')
def cmd_list():
    r = requests.get('https://a.4cdn.org/boards.json')
    if (r.status_code==200):
        boards = r.json()['boards']
        print('Available boards:')
        for i in boards:
            print('/',i['board'],'/ - ',i['title'],sep='')
    else:
        print('Failed to get boards! [',r.status_code,']',sep='')
def cmd_board(args):
    if (len(args)<1): return print('Please specify a board!')
    r = requests.get('https://a.4cdn.org/'+args[0]+'/catalog.json')
    if (r.status_code==200):
        catalog = r.json()
        page = 1
        if (len(args)>1):
            try:
                page = int(args[1])
            except:
                print('Encountered error processing page no. continuing anyways..')
        if (page>len(catalog) or page < 1): return print('Invalid page number!')
        threads = catalog[page-1]['threads']
        print('Threads on /',args[0],'/',sep='')
        for i in threads:
            try:
                s = ''
                try:
                    s=' -  ['+i['ext']+']'
                except:
                    s=' -  [nofile]'
                print(i['no'],' - ',i['com'][:50],s)
            except:
                print(i['no'],' -  No comment!')
        print('Page',page,'/',len(catalog))
    else:
        print('Failed to get any threads! [',r.status_code,']',sep='')
def print_post(post, board):
    print('No:',post['no'])
    print('At:',post['now'])
    try:
        print('Sub:',post['sub'])
    except:
        print('Sub: Undefined')
    try:
        print('File: https://i.4cdn.org/',board,'/',post['tim'],post['ext'],' [',post['fsize'],' bytes]',sep='')
    except:
        print('File: No file attached!')
    try:
        print('Comment:\n',html.unescape(post['com'].replace('<br>','\n')),sep='')
    except:
        print('Comment: No comment!')
def cmd_thread(args):
    if (len(args)<1): return print('Please specify a board!')
    if (len(args)<2): return print('Please specify a thread!')
    r = requests.get('https://a.4cdn.org/'+args[0]+'/thread/'+args[1]+'.json')
    if (r.status_code==200):
        thread = r.json()['posts']
        reply = 1
        if (len(args)>2):
            try:
                reply = int(args[2])
            except:
                print('Encountered error processing reply no. continuing anyways..')
        if (reply>len(thread) or reply < 1): return print('Invalid post number!')
        print('Thread ',args[1],' on /',args[0],'/',sep='')
        print_post(thread[reply-1], args[0])
        print('Reply',reply,'/',len(thread))
        if (len(args)>3):
            if (args[3].lower()=='y'):
                download(thread[reply-1], args[0])
    else:
        print('Failed to get any threads! [',r.status_code,']',sep='')
def cmd_viewer(args):
    if (len(args)<1): return print('Please specify a board!')
    if (len(args)<2): return print('Please specify a thread!')
    r = requests.get('https://a.4cdn.org/'+args[0]+'/thread/'+args[1]+'.json')
    if (r.status_code==200):
        thread = r.json()['posts']
        print('Thread ',args[1],' on /',args[0],'/',sep='')
        y = 1
        for i in thread:
            print_post(i, args[0])
            print('Reply',y,'/',len(thread));y+=1
            s=0
            while s==0:
                q=input('Press any key to view next.. [q to exit] [s to save file] [v to view file]\n').lower()
                if (q=='q'): s = 2
                elif (q=='s'):
                    download(i, args[0])
                    print('Finished downloading!')
                elif (q=='v'):
                    view_image(i, args[0])
                    print('Finished viewing image!')
                else: s = 1
            if (s==2): break
    else:
        print('Failed to get any threads! [',r.status_code,']',sep='')
def process(args):
    c = args[0]
    if (c=='help'): cmd_help()
    elif (c=='list'): cmd_list()
    elif (c=='board'): cmd_board(args[1:])
    elif (c=='thread'): cmd_thread(args[1:])
    elif (c=='viewer'): cmd_viewer(args[1:])
    elif (c=='quit'): sys.exit(0)
    else: print('Unknown command, try `help`.')
def shell():
    r = True
    print('\npy4ch Interactive Shell\nType quit to exit\n\n')
    while (r):
        process(input('py4ch> ').lower().split(' '))
if (len(sys.argv)>1):
    process(sys.argv[1:])
else:
    print('No usage arguments specified! (try running `py4ch help`)')
    y = input('Would you like to launch the interactive shell [Y/N]? ').lower()
    if (y=='y'): shell()
    else: sys.exit(0)
