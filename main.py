from tkinter import *
from datetime import datetime
import time
import random
from InstagramAPI import InstagramAPI

'''
For buttons:

pady = height
padx = width
fg = text color (for colors use "blue" or "#000000")
bg = button color
columnspan = how many columns


For entry boxes:

width = width
fg = text color
bg = background color
borderwidth = borderwidth

Entry(root).insert(0,'text') = have preset text (but user has to delete it)
'''

root = Tk()
root.title("Aurora 3.1.0")
root.iconbitmap('icon.ico')

error_msg = None
sleeping = False #sleeps if during interval between actions or paused button is active
paused = False #pause boolean is only for the pause button
auto_commented_posts = [] #IDs of posts the bot has already autocommented on

def sleeep(rate):
    rate = int(rate)
    bottom = rate * 0.75
    top = rate * 1.25
    value = random.uniform(bottom,top)
    time.sleep(value)

f = open('config.txt','r')
config_text = f.read()
config_text = config_text[config_text.find('\n')+1:len(config_text)]
config_text_array = []

#breaks the raw text file into an array
i = 0
try:
    while i < 9:
        if i == 8:
            config_text_array.append(config_text)
        else:
            config_text_array.append(config_text[0:config_text.find('\n')])
            config_text = config_text[config_text.find('\n')+1:len(config_text)]
        i+=1
except:
    error_msg = 'congif.txt has wrong setup configuration.'
#removes the words such as "follow break" and just leaves the setting
setting_array = []
i = 0
try:
    while i < 9:
        front_index = config_text_array[i].find('<')+1
        back_index = config_text_array[i].find('>')
        setting_array.append(config_text_array[i][front_index:back_index])
        i+=1
except:
    error_msg = 'congif.txt has wrong setup configuration.'

setting_dict = {
    "access_code":setting_array[0],
    "username":setting_array[1],
    "password":setting_array[2],
    "follow_break":setting_array[3],
    "like_break":setting_array[4],
    "comment_break":setting_array[5],
    "unfollow_break":setting_array[6],
    "category":setting_array[7],
    "custom_comment":setting_array[8]
}


#---------------error checking---------------
access_codes = ['adminpass','1234qwerasdf']
#check access code
if setting_dict['access_code'] != '' and setting_dict['access_code'] not in access_codes:
    error_msg = 'Incorrect access code. Leave blank if not applicable.'
#check username
if setting_dict['access_code'] != '' and setting_dict['username'] not in allowed_users:
    error_msg = 'User @' + str(setting_dict['username']) + ' not authorized.'
#check password
valid = False
api = InstagramAPI(setting_dict['username'],setting_dict['password'])
api.login()
result = api.LastJson
try:
    msg = result['message']
except:
    valid = True
if valid == False:
    error_msg = 'Incorrect Password'
#check follow break
valid = False
try:
    hi = int(setting_dict['follow_break'])
except:
    error_msg = 'Follow Break is not an integer'
#check like break
valid = False
try:
    hi = int(setting_dict['like_break'])
except:
    error_msg = 'Like Break is not an integer'
#check comment break
valid = False
try:
    hi = int(setting_dict['comment_break'])
except:
    error_msg = 'Comment Break is not an integer'
#check unfollow break
valid = False
try:
    hi = int(setting_dict['unfollow_break'])
except:
    error_msg = 'Unfollow Break is not an integer'
#check category
valid = False
try:
    hi = int(setting_dict['category'])
    if hi < 1 or hi > 11:
        error_msg = 'Category is not between 1 and 11.'
except:
    error_msg = 'Category is not an integer. Check README.txt for key'


if error_msg != None:
    hi = 3

#initializes the top left menu w the info that's going to contain info from config.txt
username = Label(root, text = 'Account: ',anchor = W, width = 25)
follow_break = Label(root, text = 'Follow Break: ', anchor = W, width = 25)
like_break = Label(root, text = 'Like Break: ', anchor = W, width = 25)
comment_break = Label(root, text = 'Comment Break: ', anchor = W, width = 25)
unfollow_break = Label(root, text = 'Unfollow Break: ', anchor = W, width = 25)
#adds on the settings from config.txt if there are no errors
if error_msg == None:
    username = Label(root, text = 'Account: @' + setting_dict['username'],anchor = W, width = 25)
    follow_break = Label(root, text = 'Follow Break: ' + setting_dict['follow_break'] + ' m', anchor = W, width = 25)
    like_break = Label(root, text = 'Like Break: ' + setting_dict['like_break'] + ' m', anchor = W, width = 25)
    comment_break = Label(root, text = 'Comment Break: ' + setting_dict['comment_break'] + ' m', anchor = W, width = 25)
    unfollow_break = Label(root, text = 'Unfollow Break: ' + setting_dict['unfollow_break'] + ' m', anchor = W, width = 25)


#puts the top left menu on the screen
username.grid(row = 0, column = 0,sticky = W + E)
follow_break.grid(row = 1, column = 0,sticky = W + E)
like_break.grid(row = 2, column = 0,sticky = W + E)
comment_break.grid(row = 3, column = 0,sticky = W + E)
unfollow_break.grid(row = 4, column = 0,sticky = W + E)

spacer = Label(root, text = ' ',anchor = W, width = 25)
spacer.grid(row = 6, column = 0,sticky = W + E)


clicked = StringVar()
clicked.set('Select a task')

drop = OptionMenu(root, clicked, "Follow/Unfollow Celebs","Follow Users","Like Posts",'Comment on Hashtag', 'Comment on New Posts', 'Unfollow All Users')
drop.config(width = 22)
drop.grid(row = 5, column = 0, sticky = W)

def generate_hashtags():
    out = ''
    if error_msg == None:
        if setting_dict['category'] == '1':
            out = ['#meme #funny #lol #love #humor #lmao #comedy #dankmemes #instagood #hilarious #dank #like4like #joke #funnymemes #photooftheday #laugh #lmfao #haha #likeforlike #nochill #savage #fun #like #funnyshit #followme #follow #memesdaily #instagram #wtf #jokes']
        if setting_dict['category'] == '2':
            out = ['#artist #love #instagood #design #drawing #fashion #tattoo #artwork #beautiful #photooftheday #illustration #ink #photography #style #tattoos #sketch #picoftheday #painting #beauty #inked #instaart #happy #model #girl #arte #follow #creative #amazing #draw #tattooartist']
        if setting_dict['category'] == '3':
            out = ['#football #futbol #messi #neymar #ronaldo #cr7 #sports #futebol #realmadrid #like4like #nike #worldcup #barcelona #sport #adidas #championsleague #fifa #fútbol #goal #fitness #instagood #gym #calcio #love #cristiano #laliga #cristianoronaldo #adidasfootball #nikefootball #chelsea']
        if setting_dict['category'] == '4':
            out = ['#nba #ballislife #sports #nike #basketballneverstops #cavs #lebronjames #bball #cleveland #espn #football #striveforgreatness #sneakers #cavaliers #clevelandcavaliers #kobebryant #dunk #lakers #theland #fitness #basket #sneakerhead #hoops #warriors #kicks #soccer #ohio #kobe #ballers #cavsnation']
        if setting_dict['category'] == '5':
            out = ['#mlb #beisbol #venezuela #sports #baseballislife #rd #dr #peloterosrd #dom #dominicana #do #football #repdom #repost #dominicano #athlete #yankees #basketball #peloterosmlb #worldseries #dodgers #colombia #sportwebpublicidad #love #strikeoutvzla #miami #milb #talentoswp #lvbp #soccer']
        if setting_dict['category'] == '6':
            out = ['#fashion #style #design #love #lifestyle #interiordesign #instagood #travel #architecture #interior #home #decor #photooftheday #beautiful #homedecor #inspiration #luxurylifestyle #luxurylife #art #decoration #picoftheday #house #interiors #photography #dubai #blogger #beauty #cars #happy #ootd']
        if setting_dict['category'] == '7':
            out = ['#travelgram #instagood #photooftheday #love #instatravel #wanderlust #nature #photography #trip #vacation #traveling #adventure #beautiful #travelphotography #fashion #picoftheday #lifestyle #travelling #travelblogger #happy #summer #holiday #beach #explore #blogger #luxury #ig #amazing #style #tourism']
        if setting_dict['category'] == '8':
            out = ['#tech #apple #instagood #iphone #smartphone #design #photooftheday #science #innovation #gaming #pc #ios #game #electronics #geek #video #gadget #instatech #videogames #gamers #computer #samsung #mobile #iphone8 #gadgets #android #phone #games #engineering #techie']
        if setting_dict['category'] == '9':
            out = ['#gamer #videogames #ps4 #xbox #playstation #game #games #gamergirl #pc #xboxone #nintendo #gamers #cod #instagamer #callofduty #geek #youtube #leagueoflegends #cosplay #nerd #artwork #pokemon #fanart #meme #overwatch #instagaming #pcgaming #memes #anime #lol']
        if setting_dict['category'] == '10':
            out = ['#gaming #callofduty #xbox #ps4 #funny #cod #meme #lol #gamer #xboxone #games #mario #gamergirl #memes #game #pc #dank #gamers #pokemon #blackops #littleclub #skyrim #overwatch #minecrafters #wow #pewdiepie #pubg #pikachu #sonic #doritos']
        if setting_dict['category'] == '11':
            out = ['#car #carporn #carswithoutlimits #carsofinstagram #luxury #supercars #bmw #speed #stance #amazingcars247 #instacar #sportscar #exoticcars #auto #supercar #audi #racing #turbo #carlifestyle #mercedes #exotic #horsepower #ferrari #lamborghini #instacars #carstagram #race #porsche #drive #amazing']

    temp = out
    out = ''
    for hashtag in temp:
        out = out + ' ' + hashtag


    f = open('generated hashtags.txt','r')
    file_words = f.read()
    f.close()
    f = open('generated hashtags.txt','w')
    file_words = file_words + '\n\n' + out
    f.writelines(file_words)
    f.close()

hashtag_button = Button(root, text = 'Generate Hashtags', command = generate_hashtags)
hashtag_button.grid(row = 6, column = 0, sticky = W)
#e = Entry(root)
#e.grid(row = 0,column = 0)
paused = False
def pause_command():
    done = False
    if pause_button['text'] == 'Play':
        paused = True
        pause_button.config(text = 'Pause')
        done = True
    if pause_button['text'] == 'Pause' and done == False:
        paused = False
        pause_button.config(text = 'Play')
        

pause_button = Button(root, text = 'Pause', command = pause_command, width = 5, anchor = W)
pause_button.grid(row = 7, column = 0, sticky = W)

#def myClick():
#    hello = "hello" + e.get()
#    myLabel = Label(root, text = hello)
#    myLabel.grid(row = 2,column = 1)


#myButton = Button(root, text = "Enter your name",command = myClick,padx = 10, pady = 10)
#myButton.grid(row = 1,column = 0)

quit_button = Button(root, text = "Exit", command = root.quit, fg = 'black', bg = 'red')
quit_button.grid(row = 8,column = 0, sticky = W)


recent_actions = []

listbox_holder = Frame(root)

#Now we're going to set-up the listbox and the scrollbar
recent_actions_box = Listbox(listbox_holder, width = 50, fg = '#1FFF00', bg = 'black')
scrollybar = Scrollbar(listbox_holder, orient=VERTICAL)
recent_actions_box.config(yscrollcommand=scrollybar.set)
scrollybar.config(command=recent_actions_box.yview)
#Let's pack them into our frame
scrollybar.pack(side=RIGHT, fill=Y)
recent_actions_box.pack()

#Now let's get our main window squared away
listbox_holder.grid(row=0, column=1, rowspan = 20)

for item in recent_actions:
    recent_actions_box.insert(END, item)

def load():
    out = {
        '1':['therock','kyliejenner','kendalljenner','kevinhart4real','cristiano','chrishemsworth','robertdowneyjr','leomessi','justinbieber','jlo','kimkardashian','kourtneykardash','iamcardib','snoopdogg','kingjames','champagnepapi','postmalone','krisjenner','arianagrande','selenagomez','dualipa','camila_cabello','billieeilish','taylorswift','gigihadid','ddlovato'],
        '2':[],
        '3':[],
        '4':[],
        '5':[],
        '6':[],
        '7':[],
    }
    
    random.shuffle(out['1'])
    out_combined = []
    for i in range(0,len(out['1']),1):
        out_combined.append(out['1'][i])
        out_combined.append(out['1'][i])
    out['1'] = out_combined

    category_str = ''
    if setting_dict['category'] == '1':
        category_str = 'memes'
    if setting_dict['category'] == '2':
        category_str = 'art'
    if setting_dict['category'] == '3':
        category_str = 'soccer'
    if setting_dict['category'] == '4':
        category_str = 'basketball'
    if setting_dict['category'] == '5':
        category_str = 'baseball'
    if setting_dict['category'] == '6':
        category_str = 'luxury'
    if setting_dict['category'] == '7':
        category_str = 'travel'
    if setting_dict['category'] == '8':
        category_str = 'technology'
    if setting_dict['category'] == '9':
        category_str = 'gaming'
    if setting_dict['category'] == '10':
        category_str = 'minecraft'
    if setting_dict['category'] == '11':
        category_str = 'cars'

    #users to follow
    username = ''
    category = category_str
    if category == 'memes':
        username = 'daquan'
    if category == 'art':
        username = 'art'
    if category == 'soccer':
        username = 'soccerbible'
    if category == 'basketball':
        username = 'basketball'
    if category == 'baseball':
        username = 'mlb'
    if category == 'luxury':
        username = 'luxury_listings'
    if category == 'travel':
        username = 'travelandleisure'
    if category == 'technology':
        username = 'technology'
    if category == 'gaming':
        username = 'gamingzar'
    if category == 'minecraft':
        username = 'minecraftkool'
    if category == 'cars':
        username = 'exotic_performance'

    api.searchUsername(username)
    result = api.LastJson
    username_id = result['user']['pk']
    #get most recent post
    user_posts = api.getUserFeed(username_id)
    result = api.LastJson
    media_id = result['items'][0]['id']
    #get likers
    api.getMediaLikers(media_id)
    users = api.LastJson['users']
    users_list = []
    for user in users:
        users_list.append({'pk':user['pk'], 'username':user['username']})

    out['2'] = users_list
    


    sleeep(2)
    #get posts to like
    api.getHashtagFeed(category_str)
    result = api.LastJson
    result = result['items']
    outt = []
    for post in result:
        try:
            media_id = post['caption']['media_id']
            username = post['user']['username']
            #outt.append(media_id)
            outt.append({'media_id':media_id, 'username':username})
        except:
            asdfafdslkjafdsafdsadsf = 'asdffdasfasd'
    out['3'] = outt

    sleeep(2)
    #get posts to comment, same as posts to like because it gets the post ID to comment on
    out['4'] = outt




    sleeep(2)
    #get users to unfollow
    api.getSelfUsersFollowing()
    result = api.LastJson
    following_users = []
    for user in result['users']:
        following_users.append({'pk':user['pk'],'username':user['username']})
    out['6'] = following_users

    return out



task_num_key = {
    'Follow/Unfollow Celebs':'1',
    'Follow Users':'2',
    'Like Posts':'3',
    'Comment on Hashtag':'4',
    'Comment on New Posts':'5',
    'Unfollow All Users':'6',
    'Generate Hashtags':'7'
}
tasks = None
if error_msg == None:
    tasks = load()

if error_msg == None:
    recent_actions_box.insert(0, 'Successfully Logged In')

accs_to_scan = ['daquan','memes','rap','nbamemes','9gag','sarcasm_only','betches','memequeen','do_or_drink','fuckjerry','thefatjewish','funnymemes','ladbible']
last_action_time = 0
celeb_last_action = 'unfollow'
def main_loop():
    global tasks
    global celeb_last_action

    f = open('other.txt','r')
    file_words = f.read()
    f.close()
    #f = open('other.txt','w')
    last_action_time = file_words[file_words.find(':')+1:len(file_words)]
    last_action_time = float(last_action_time)
    #file_words = file_words + '\n\n' + out
    #f.writelines(file_words)
    #f.close()

    if pause_button['text'] == 'Play':
        paused = True
    if pause_button['text'] == 'Pause':
        paused = False

    #print(clicked.get())
    task_num = 0
    try:
        task_num = task_num_key[clicked.get()]
    except:
        task_num = 0
    
    #set the wait time between actions depending on the action
    wait_time = 3600 #like this so certain functions, such as generating hashtags, only happens once
    if task_num == '1' or task_num == '2':
        wait_time = int(setting_dict['follow_break']) * 60
    if task_num == '3':
        wait_time = int(setting_dict['like_break']) * 60
    if task_num == '4':
        wait_time = int(setting_dict['comment_break']) * 60
    if task_num == '5':
        wait_time == 10 * 60 #wait time between scanning all accs
    if task_num == '6':
        wait_time = int(setting_dict['unfollow_break']) * 60
    


    sleeping = False
    if error_msg != None:
        sleeping = True
    if time.time() - last_action_time < wait_time:
        sleeping = True
    if paused == True:
        sleeping = True


    if sleeping == False and error_msg == None:
        if task_num == '1':
            just_followed = False
            if celeb_last_action == 'unfollow':
                username = tasks['1'][0]
                api.searchUsername(username)
                result = api.LastJson
                user_id = result['user']['pk']
                api.follow(user_id)
                recent_actions_box.insert(0,'Followed @' + tasks['1'][0])
                celeb_last_action = 'follow'
                just_followed = True
                tasks['1'].pop(0)
                f = open('other.txt','w')
                file_words = file_words[0:file_words.find(':')+1]
                file_words = file_words + str(time.time())
                f.writelines(file_words)
                f.close()
            if celeb_last_action == 'follow' and just_followed == False:
                username = tasks['1'][0]
                api.searchUsername(username)
                result = api.LastJson
                user_id = result['user']['pk']
                api.unfollow(user_id)
                recent_actions_box.insert(0,'Unfollowed @' + tasks['1'][0])
                celeb_last_action = 'unfollow'
                tasks['1'].pop(0)
                f = open('other.txt','w')
                file_words = file_words[0:file_words.find(':')+1]
                file_words = file_words + str(time.time())
                f.writelines(file_words)
                f.close()
        if task_num == '2':
            user_id = tasks['2'][0]['pk']
            api.follow(user_id)
            recent_actions_box.insert(0,'Followed @' + tasks['2'][0]['username'])
            tasks['2'].pop(0) #removes the first element
            f = open('other.txt','w')
            file_words = file_words[0:file_words.find(':')+1]
            file_words = file_words + str(time.time())
            f.writelines(file_words)
            f.close()
        if task_num == '3':
            post_id = tasks['3'][0]['media_id']
            api.like(post_id)
            recent_actions_box.insert(0,'Liked @'+tasks['3'][0]['username'] + '\'s post')
            tasks['3'].pop(0)
            f = open('other.txt','w')
            file_words = file_words[0:file_words.find(':')+1]
            file_words = file_words + str(time.time())
            f.writelines(file_words)
            f.close()
        if task_num == '4':
            post_id = tasks ['4'][0]['media_id']
            api.comment(post_id,setting_dict['custom_comment'])
            recent_actions_box.insert(0,'Commented on @'+tasks['3'][0]['username'] + '\'s post')
            tasks['4'].pop(0)
            f = open('other.txt','w')
            file_words = file_words[0:file_words.find(':')+1]
            file_words = file_words + str(time.time())
            f.writelines(file_words)
            f.close()
        #auto comment on new posts
        if task_num == '5':

            accs = ['daquan','memes','rap','nbamemes','9gag','sarcasm_only','betches','memequeen','do_or_drink','fuckjerry','thefatjewish','funnymemes','ladbible']
            posts = []
            for account in accs:
                api.searchUsername(account)
                result = api.LastJson
                try: #try because it sometimes, though not often, just randomly not work
                    username_id = result['user']['pk']
                    username = result['user']['username']
                    user_posts = api.getUserFeed(username_id)
                    result = api.LastJson
                    result = result['items']
                    latest = result[0]
                    post_id = latest['pk']
                    if post_id not in auto_commented_posts:
                        posts.append(post_id)
                except:
                    asdf = 2

            for post in posts:
                sleeep(2)
                api.comment(post, setting_dict['custom_comment'])
                recent_actions_box.insert(0,'Autocommented on a new post')
                auto_commented_posts.append(post_id)
        
            f = open('other.txt','w')
            file_words = file_words[0:file_words.find(':')+1]
            file_words = file_words + str(time.time())
            f.writelines(file_words)
            f.close()
        if task_num == '6':
            user_id = tasks['6'][0]['pk']
            api.unfollow(user_id)
            recent_actions_box.insert(0,'Unfollowed @' + tasks['6'][0]['username'])
            tasks['6'].pop(0)
            f = open('other.txt','w')
            file_words = file_words[0:file_words.find(':')+1]
            file_words = file_words + str(time.time())
            f.writelines(file_words)
            f.close()


    if error_msg == None and sleeping == False:
        if len(tasks['1']) <= 1:
            tasks = load()
        if len(tasks['2']) <= 1:
            tasks = load()
        if len(tasks['3']) <= 2:
            tasks = load()
        if len(tasks['4']) <= 3:
            tasks = load()
        if len(tasks['6']) <= 5:
            tasks = load()


    root.after(2000, main_loop)  # reschedule event in 2 seconds

root.after(2000, main_loop)
root.mainloop()