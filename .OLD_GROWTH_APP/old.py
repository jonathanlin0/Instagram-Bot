#!usr/bin/env python

import pprint
from InstagramAPI import InstagramAPI
from time import sleep
from datetime import datetime
from random import seed
from random import randint
import time
import random
from colorama import Fore, Back, Style, init
import sys
from contextlib import contextmanager
import os
import os.path
import pygame
init(convert=True)


following_users = []

def get_likes_list(username,rate,category):
    username = str(username)
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
    return users_list

def follow_users(category,rate):


    users_list = get_likes_list(username,rate,'TBD')
    follow_ctr = 1

    api.getSelfUsersFollowing()
    result = api.LastJson
    for user in result['users']:
        following_users.append(user['pk'])

    for user in users_list:
        if follow_ctr % 60 == 0:
            print('Temporary sleeping for 40 minutes')
            sleeep(2400)

        if not user['pk'] in following_users:
            api.follow(user['pk'])
            temp = "Followed @" + user['username']
            i = len(temp)
            while i < 40:
                temp = temp + ' '
                i += 1
            print(temp + '|   ' + str(follow_ctr))
            follow_ctr += 1
            sleeep(rate)

def follow_celebs(rate):
    celeb_list_to_follow = ['therock','kyliejenner','kendalljenner','kevinhart4real','cristiano','chrishemsworth','robertdowneyjr','leomessi','justinbieber','jlo','kimkardashian','kourtneykardash','iamcardib','snoopdogg','kingjames','champagnepapi','postmalone','krisjenner','arianagrande','selenagomez','dualipa','camila_cabello','billieeilish','taylorswift','gigihadid','ddlovato']
    celeb_list_followed = []
    random.shuffle(celeb_list_to_follow)
    action_counter = 1
    while 0 < 1:
        '''
        for user in celeb_list_to_follow:
            api.searchUsername(user)
            result = api.LastJson
            user_id = result['user']['pk']
            api.follow(user_id)
            print('Followed: ' + str(user) + '   |   ' + str(action_counter))
            celeb_list_to_follow.remove(user)
            celeb_list_followed.append(user)
            action_counter += 1
            time.sleep(rate)
        for user in celeb_list_followed:
            api.searchUsername(user)
            result = api.LastJson
            user_id = result['user']['pk']
            api.unfollow(user_id)
            print('Unfollowed: ' + str(user) + '   |   ' + str(action_counter))
            celeb_list_to_follow.append(user)
            celeb_list_followed.remove(user)
            action_counter += 1
            time.sleep(rate)
        '''
        if len(celeb_list_to_follow) == 0:
            for user in celeb_list_followed:
                celeb_list_to_follow.append(user)
                celeb_list_followed.remove(user)
            print('Temporarily sleeping for 40 min')
            time.sleep(2400)
        for user in celeb_list_to_follow:
            api.searchUsername(user)
            result = api.LastJson
            user_id = result['user']['pk']
            api.follow(user_id)
            out = str(user)
            temp = 20 - len(out)
            i = 0
            while i < temp:
                out = out + ' '
                i += 1
            out = out + '  '
            print('Followed: ' + out + '|   ' + str(action_counter))
            action_counter += 1
            sleeep(rate)

            api.searchUsername(user)
            result = api.LastJson
            user_id = result['user']['pk']
            api.unfollow(user_id)
            out = str(user)
            temp = 20 - len(out)
            i = 0
            while i < temp:
                out = out + ' '
                i += 1
            print('Unfollowed: ' + out + '|   ' + str(action_counter))
            action_counter += 1
            sleeep(rate)

            celeb_list_followed.append(str(user))
            celeb_list_to_follow.remove(str(user))



def like_posts(category,rate):
    print('Liking Posts Procedure Starting...')
    api.getHashtagFeed(category)
    result = api.LastJson
    posts = []
    result = result["items"]
    counter = 1
    for x in result:
        post = x
        post = post['caption']
        api.like(post['media_id'])
        print('Liked ' + str(counter) + ' posts')
        counter += 1
        sleep(rate)

def auto_comment(category,rate):
    print('')
    comment_text = input('What would you like your comment to be: ')
    print('Auto Commenting Starting...')
    api.getHashtagFeed(category)
    result = api.LastJson
    posts = []
    result = result["items"]
    counter = 1
    for x in result:
        post = x
        post = post['caption']
        media_id = post['media_id']
        api.comment(media_id,comment_text)
        print('Commented on ' + str(counter) + ' posts')
        counter += 1
        sleep(rate)

def new_posts_comment():
    print('')
    comment = input('What would you like to comment: ')
    comment_texts = [comment,comment]
    if comment == '###':
        comment_texts = ['I hate all the bots on insta while im here tryna grind fr and post quality content','Pubity blocked me because I post better content than him','daquan blocked me because I post better content than him','If you like spongebob and love to laugh, please check out my page!','Check my page out for daily, funny spongebob memes','Follow me for great and funny spongebob memes!','If you like spongebob memes, give me a follow!','I post funny spongebob memes, please check my page out!']
        print('Access code received (commenting from first person)')
    if comment == '##':
        comment_texts = ['pubity blocked @le_spongebob because he is posting better content than him','daquan blocked @le_spongebob because he is posting better content than him','I normally dont do shoutouts, but the content on @le_spongebob \'s is just too good to pass up','Check out @le_spongebob for some awesome spongebob memes','@le_spongebob posts awesome, daily spongebob memes','if you like spongebob and memes, consider following @le_spongebob']
        print('Access code received (commenting from third person)')
    if comment == '#':
        comment_texts = ['@le_spongebob is the fastest acceptor in the world! Go request the refresh!','I heard @le_spongebob is the fastest acceptor in the world, try to go request then refresh!','i heard that @le_spongebob is the fastest follow request acceptor in the world! just request the refresh!']
        print('Access code received (commenting about autoacceptance)')

    print('')
    print('Starting Scanning...')
    commented_posts = [2293446456341557219, 2293299520585278092, 2293448003444079251, 2293449969423381300, 2293879720469985623, 2294555536055725841, 2294781000674690067, 2294785664255680219, 2294786090648086919, 2294817925348441104, 2294820182469982001, 2294823642477173604, 2294824895518779019, 2294826170778527876, 2294826985513754683]
    accounts = ['memeslair','teacherpranks','daquan','memes','rap','nbamemes','2.718281828459045235360287420','9gag','sarcasm_only','betches','memequeen','do_or_drink','fuckjerry','thefatjewish','funnymemes','ladbible']

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    comment_ctr = 1
    scan_ctr = 1
    start_time = time.time()
    while True:
        for acc in accounts:
            if scan_ctr % 100 == 0:
                print('Temporary sleeping for 10 minutes')
                sleeep(600)
            time.sleep(2)

            scan_ctr += 1

            api.searchUsername(acc)
            result = api.LastJson
            
            try:
                username_id = result['user']['pk']
                username = result['user']['username']

                with suppress_stdout():
                    user_posts = api.getUserFeed(username_id)
                result = api.LastJson

                result = result['items']
                latest = result[0]
                comment_cnt = latest['comment_count']
                post_id = latest['pk']
        
                random.shuffle(comment_texts)
                random.shuffle(comment_texts)
                random.shuffle(comment_texts)

                if not int(post_id) in commented_posts:
                    if comment_cnt < 15:
                        with suppress_stdout():
                            api.comment(post_id,comment_texts[0])
                        commented_posts.append(post_id)
                        comment_ctr += 1

                        out = 'Commented on ' + str(username) + "'s post"
                        i = 0
                        temp = 40 - len(out)
                        while i < temp:
                            out = out + ' '
                            i += 1
                        out = out + '|    ' + str(comment_ctr)

                        #delete previous 3 lines to get rid of counter and then print 3 extra lines for the timer to get rid of
                        '''
                        sys.stdout.write(CURSOR_UP_ONE)
                        sys.stdout.write(ERASE_LINE)
                        sys.stdout.write(CURSOR_UP_ONE)
                        sys.stdout.write(ERASE_LINE)
                        sys.stdout.write(CURSOR_UP_ONE)
                        sys.stdout.write(ERASE_LINE)
                        print(out)
                        print('temp')
                        print('temp')
                        print('temp')
                        

                        if len(commented_posts) % 5 == 0:
                            print('-------------')
                            print('Updated list: ')
                            print(commented_posts)
                            print('-------------')
                        '''
            except:
                hi = 1
            
            end_time = time.time()
            time_elapsed = end_time - start_time
            time_elapsed_str = str(time_elapsed)
            if time_elapsed_str.find(".") > -1:
                time_elapsed_str = time_elapsed_str[0:time_elapsed_str.find(".")]
            time_elapsed = int(time_elapsed_str)

            secs = time_elapsed
            mins = secs // 60
            secs = secs % 60
            hours = mins // 60
            mins = mins % 60
            s_str = 'seconds'
            m_str = 'minutes'
            h_str = 'hours'
            if secs == 1:
                s_str = 'second'
            if mins == 1:
                m_str = 'minute'
            if hours == 1:
                h_str = 'hour'

            if scan_ctr > 1:
                sys.stdout.write(CURSOR_UP_ONE)
                sys.stdout.write(ERASE_LINE)
                sys.stdout.write(CURSOR_UP_ONE)
                sys.stdout.write(ERASE_LINE)
                sys.stdout.write(CURSOR_UP_ONE)
                sys.stdout.write(ERASE_LINE)
            str_time = 'Time Elapsed: ' + str(hours) + ' ' + h_str + ' | ' + str(mins) + ' ' + m_str + ' | ' + str(secs) + ' ' + s_str
            str_scans = str(scan_ctr) + ' accounts scanned'
            str_comments = 'Commented ' + str(comment_ctr) + ' times'
            print(str_time)
            print(str_scans)
            print(str_comments)
            
            


def unfollow_users(rate):
    api.getSelfUsersFollowing()
    result = api.LastJson
    followingUsers = []
    whitelisted = ['teacherpranks','pubity']
    for user in result['users']:
        following_users.append({'pk':user['pk'],'username':user['username']})
    action_ctr = 1
    for user in following_users:
        if not user['username'] in whitelisted:
            if action_ctr % 60 == 0:
                print('Temporary sleeping for 40 min')
                sleeep(2400)
            api.unfollow(user['pk'])
            out = "Unfollowed @" + user['username']
            i = 0
            temp = 40 - len(out)
            while i < temp:
                out = out + ' '
                i += 1
            out = out + '|    ' + str(action_ctr)
            print(out)
            action_ctr += 1
            sleeep(rate)


def get_my_profile_details():
    api.getSelfUsernameInfo()
    result = api.LastJson
    #formatted_json = pprint.pformat(result)
    #print(formatted_json)
    username = result['user']['username']
    full_name = result['user']['full_name']
    followers = result['user']['follower_count']
    print({'Username': username, 'Full Name': full_name, 'Followers': followers})

def get_my_feed():
    image_urls = []
    api.getSelfUserFeed()
    result = api.LastJson
    if 'items' in result.keys():
        for item in result['items'][:5]:
            if 'image_version2' in item.keys():
                image_url = item['image_versions2']['candidates'][1]['url']
                image_urls.append(image_url)
    print(image_urls)
'''
def get_not_follow_back():
    following = []
    followers = []
    api.getSelfUsersFollowing()
    result = api.LastJson
    out = []
    for user in result['users']:
        following.append(user['username'])
    api.getSelfUsernameInfo()
    username = api.LastJson
    username = username['user']
    username = username['pk']
    api.getTotalSelfFollowers()
    result = api.LastJson
    for user in result['users']:
        followers.append(user['username'])
    for user in following:
        if not user in followers:
            out.append(user)
    print(len(out))
    out = ' '.join(out)
    print(out)
    print('-------')
    print(len(following))
    print(following)
    print(len(followers))
    print(followers)
'''       

def generate_hashtags(num):
    hashtag_1 = ['memes','funnymemes','pubity','funny','lmfao','lmao','lol','textposts','memepage','dankmemes','savagememes','humor','cringe','dank','depression','like4like','likeforlike']
    hashtag_2 = ['meme','funnymeme','humor','jokes','haha','savage','edgy','edgymemes','relatable','memeoftheday','dankmeme','savagememe','nochill','nochillmemes','coronavirusmemes','hilariousmemes']
    hashtag_3 = ['follow4follow','f4f','followforfollow','relatablememe','relatablememes','tiktok','tiktoks','funnytiktoks','niche','triggered','followformemes','coronavirus','corona']
    hashtag = []
    hashtag.extend(hashtag_1)
    hashtag.extend(hashtag_2)
    hashtag.extend(hashtag_3)
    random.shuffle(hashtag)
    random.shuffle(hashtag)
    hashtag = hashtag[0:num]
    out_list = []
    for ht in hashtag:
        temp = '#' + ht
        out_list.append(temp)
    out = ' '.join(out_list)
    print(out)

def execute_function(function):
    temp = [1,2,3,4,6]
    print('')
    rate = 0
    if function in temp:
        rate = get_int_input([0,5000],'How many minutes would you like between actions')
        rate = rate*60            
    print('')

    if function == 1:
        follow_celebs(rate)

    if function == 2:
        follow_users(get_acc_from_category(get_category()),rate)

    if function == 3:
        like_posts(get_category(),rate)

    if function == 4:
        auto_comment(get_category(),rate)

    #if function == 4:
    #    get_not_follow_back()

    if function == 5:
        new_posts_comment()
        
    if function == 6:
        unfollow_users(rate)

    if function == 7:
        generate_hashtags(get_int_input([1,30],'How many hashtags do you want'))

    if function == 8:
        test_module()

def get_category():
    print(" [1] Memes")
    print(" [2] Art")
    print(" [3] Soccer")
    print(" [4] Basketball")
    print(" [5] Baseball")
    print(" [6] Luxury")
    print(" [7] Travel")
    print(" [8] Technology")
    print(" [9] Gaming")
    print("[10] Minecraft")
    print("[11] Cars")
    category = get_int_input([1,11],'What Category Would You Like To Target (enter a number 1-11): ')
    categories = ['memes','art','soccer','basketball','baseball','luxury','travel','technology','gaming','minecraft','cars']
    return categories[category -1]

def get_acc_from_category(category):
    out = ''

    if category == 'memes':
        out = 'daquan'
    if category == 'art':
        out = 'art'
    if category == 'soccer':
        out = 'soccerbible'
    if category == 'basketball':
        out = 'basketball'
    if category == 'baseball':
        out = 'mlb'
    if category == 'luxury':
        out = 'luxury_listings'
    if category == 'travel':
        out = 'travelandleisure'
    if category == 'technology':
        out = 'technology'
    if category == 'gaming':
        out = 'gamingzar'
    if category == 'minecraft':
        out = 'minecraftkool'
    if category == 'cars':
        out = 'exotic_performance'

    return out

def sleeep(rate):
    rate = int(rate)
    bottom = rate * 0.75
    top = rate * 1.25
    value = random.uniform(bottom,top)
    time.sleep(value)

def get_int_input(range,question):
    valid = False
    number = input(question + ': ')
    if type(number) == int:
        if number >= range[0] and number <= range[1]:
            valid = True
    while valid == False:
        try:
            number = int(number)
            if number >= range[0] and number <= range[1]:
                valid = True
            else:
                number = input('Please enter a number between ' + str(range[0]) + ' and ' + str(range[1]) + ': ')
        except:
            number = input('Error. Please try again: ')
    return number

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def test_module():

    api.searchUsername('jonathan__lin')
    result = api.LastJson
    print(result)
    
    '''
    print('one')
    with suppress_stdout():
        print('two')
    
    print('asdf')
    print('1')
    print('2')
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    print('2')
    '''

    '''
    api.getSelfUsersFollowing()
    api.getSelfUsersFollowing()
    result = api.LastJson
    followingUsers = []
    whitelisted = ['teacherpranks','pubity']
    for user in result['users']:
        following_users.append({'pk':user['pk'],'username':user['username']})
    out = ''
    for user in following_users:
        out = out + ', ' + user['username']
    out = out[2:len(out)]
    print(out)
    '''

pygame.init()
error_msg = 'No Errors.'

#create screen
screen = pygame.display.set_mode((500,500))

# Title and Icon
pygame.display.set_caption("Aurora 3.0.0")
#icon = pygame.image.load('icon.jpg')
#pygame.display.set_icon(icon)

#text
font = pygame.font.SysFont('arial',30)

def show_title_left(text, x, y, color):
    font = pygame.font.Font('freesansbold.ttf',20)
    text = font.render(text,True,color)
    screen.blit(text, (x,y))

def show_text_left(text, x, y, color):
    font = pygame.font.Font('freesansbold.ttf',15)
    text = font.render(text,True,color)
    screen.blit(text, (x,y))

def show_title_right(text, x, y, color):
    font = pygame.font.Font('freesansbold.ttf',20)
    text = font.render(text,True,(0,0,0))
    text_rect = text.get_rect()
    text_rect.right = x
    text_rect.bottom = y
    screen.blit(text,text_rect)

def show_text_right(text, x, y, color):
    font = pygame.font.Font('freesansbold.ttf',15)
    text = font.render(text,True,(0,0,0))
    text_rect = text.get_rect()
    text_rect.right = x
    text_rect.bottom = y
    screen.blit(text,text_rect)

def button_text(text,y):
    font = pygame.font.Font('freesansbold.ttf',15)
    button_text = font.render(text,True,(225,225,225))
    text_rect = button_text.get_rect()
    text_rect.centery = y
    text_rect.right = 485
    screen.blit(button_text, text_rect)

def button_line(y):
    font = pygame.font.Font('freesansbold.ttf',15)
    button_text = font.render('|',True,(225,225,225))
    text_rect = button_text.get_rect()
    text_rect.centery = y
    text_rect.left = 275
    screen.blit(button_text,text_rect)

def action_console(text,y,font_size):
    font = pygame.font.Font('freesansbold.ttf',font_size)
    text = font.render(text,True,(0,0,0))
    text_rect = text.get_rect()
    text_rect.centery = y
    text_rect.left = 7
    screen.blit(text,text_rect)

def action_console_line(surface,y):
    pygame.draw.line(surface,(158,158,158),(7,y),(75,y),1)

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

button_areas = {
    #[top x, top y, bottom x, bottom y]
    "1":{"top_left_x":270,"top_left_y":128,'bottom_right_x':493,'bottom_right_y':168},
    "2":{"top_left_x":270,"top_left_y":178,'bottom_right_x':493,'bottom_right_y':218},
    "3":{"top_left_x":270,"top_left_y":228,'bottom_right_x':493,'bottom_right_y':268},
    "4":{"top_left_x":270,"top_left_y":278,'bottom_right_x':493,'bottom_right_y':318},
    "5":{"top_left_x":270,"top_left_y":328,'bottom_right_x':493,'bottom_right_y':368},
    "6":{"top_left_x":270,"top_left_y":378,'bottom_right_x':493,'bottom_right_y':418},
    "7":{"top_left_x":270,"top_left_y":428,'bottom_right_x':493,'bottom_right_y':468}
}

button_areas1 = {
    '1':{'topx':270,'topy':128,'bottomx':493,'bottomy':168}
}

f.close()

start_time = time.time()

follow_ctr = 0
like_ctr = 0
comment_ctr = 0
task = 'Please Select A Task'
mouse_x = 0
mouse_y = 0
allowed_users = ['brleksven','stepbrowiz.cs','25kpullups','st0rmhut','baseballgod62','zexidd','cuxerrr','memesmarketplace','follow_le_spongebob','danielee9203','dont_.read_my_bio__','ig_scanner','jonathan__lin','le_spongebob','strikly_fortnite','useless_memezz','dankdiddlydoodlememes','arno___barton','lmaoooosam','alaadinbtw','rocky_mods','lustfall','hurtinful','tyler.theintern']
error = True
auto_commented_posts = []

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


task_num = 0


def preload():
    out = {
        '1':['therock','kyliejenner','kendalljenner','kevinhart4real','cristiano','chrishemsworth','robertdowneyjr','leomessi','justinbieber','jlo','kimkardashian','kourtneykardash','iamcardib','snoopdogg','kingjames','champagnepapi','postmalone','krisjenner','arianagrande','selenagomez','dualipa','camila_cabello','billieeilish','taylorswift','gigihadid','ddlovato'],
        '2':[],
        '3':[],
        '4':[],
        '5':[],
        '6':[],
        '7':[],
    }
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
    username = get_acc_from_category(category_str)
    out['2'] = get_users_to_follow(username)
    
    sleeep(2)
    #get posts to like
    out['3'] = get_hashtag_posts(category_str)

    sleeep(2)
    #get posts to comment
    out['4'] = get_hashtag_posts(category_str)
    
    #sleeep(2)
    #comment on new posts

    sleeep(2)
    #unfollow all users
    api.getSelfUsersFollowing()
    result = api.LastJson
    following_users = []
    for user in result['users']:
        following_users.append({'pk':user['pk'],'username':user['username']})
    out['6'] = following_users

    sleeep(2)
    #generate hashtags
    if category_str == 'memes':
        out['7'] = ['#meme #funny #lol #love #humor #lmao #comedy #dankmemes #instagood #hilarious #dank #like4like #joke #funnymemes #photooftheday #laugh #lmfao #haha #likeforlike #nochill #savage #fun #like #funnyshit #followme #follow #memesdaily #instagram #wtf #jokes']
    if category_str == 'art':
        out['7'] = ['#artist #love #instagood #design #drawing #fashion #tattoo #artwork #beautiful #photooftheday #illustration #ink #photography #style #tattoos #sketch #picoftheday #painting #beauty #inked #instaart #happy #model #girl #arte #follow #creative #amazing #draw #tattooartist']
    if category_str == 'soccer':
        out['7'] = ['#football #futbol #messi #neymar #ronaldo #cr7 #sports #futebol #realmadrid #like4like #nike #worldcup #barcelona #sport #adidas #championsleague #fifa #fútbol #goal #fitness #instagood #gym #calcio #love #cristiano #laliga #cristianoronaldo #adidasfootball #nikefootball #chelsea']
    if category_str == 'basketball':
        out['7'] = ['#nba #ballislife #sports #nike #basketballneverstops #cavs #lebronjames #bball #cleveland #espn #football #striveforgreatness #sneakers #cavaliers #clevelandcavaliers #kobebryant #dunk #lakers #theland #fitness #basket #sneakerhead #hoops #warriors #kicks #soccer #ohio #kobe #ballers #cavsnation']
    if category_str == 'baseball':
        out['7'] = ['#mlb #beisbol #venezuela #sports #baseballislife #rd #dr #peloterosrd #dom #dominicana #do #football #repdom #repost #dominicano #athlete #yankees #basketball #peloterosmlb #worldseries #dodgers #colombia #sportwebpublicidad #love #strikeoutvzla #miami #milb #talentoswp #lvbp #soccer']
    if category_str == 'luxury':
        out['7'] = ['#fashion #style #design #love #lifestyle #interiordesign #instagood #travel #architecture #interior #home #decor #photooftheday #beautiful #homedecor #inspiration #luxurylifestyle #luxurylife #art #decoration #picoftheday #house #interiors #photography #dubai #blogger #beauty #cars #happy #ootd']
    if category_str == 'travel':
        out['7'] = ['#travelgram #instagood #photooftheday #love #instatravel #wanderlust #nature #photography #trip #vacation #traveling #adventure #beautiful #travelphotography #fashion #picoftheday #lifestyle #travelling #travelblogger #happy #summer #holiday #beach #explore #blogger #luxury #ig #amazing #style #tourism']
    if category_str == 'technology':
        out['7'] = ['#tech #apple #instagood #iphone #smartphone #design #photooftheday #science #innovation #gaming #pc #ios #game #electronics #geek #video #gadget #instatech #videogames #gamers #computer #samsung #mobile #iphone8 #gadgets #android #phone #games #engineering #techie']
    if category_str == 'gaming':
        out['7'] = ['#gamer #videogames #ps4 #xbox #playstation #game #games #gamergirl #pc #xboxone #nintendo #gamers #cod #instagamer #callofduty #geek #youtube #leagueoflegends #cosplay #nerd #artwork #pokemon #fanart #meme #overwatch #instagaming #pcgaming #memes #anime #lol']
    if category_str == 'minecraft':
        out['7'] = ['#gaming #callofduty #xbox #ps4 #funny #cod #meme #lol #gamer #xboxone #games #mario #gamergirl #memes #game #pc #dank #gamers #pokemon #blackops #littleclub #skyrim #overwatch #minecrafters #wow #pewdiepie #pubg #pikachu #sonic #doritos']
    if category_str == 'cars':
        out['7'] = ['#car #carporn #carswithoutlimits #carsofinstagram #luxury #supercars #bmw #speed #stance #amazingcars247 #instacar #sportscar #exoticcars #auto #supercar #audi #racing #turbo #carlifestyle #mercedes #exotic #horsepower #ferrari #lamborghini #instacars #carstagram #race #porsche #drive #amazing']
    #prints the hashtags onto the README.txt file
    f = open('README.txt','r')
    file_words = f.read()
    f.close()
    f = open('README.txt','w')
    file_words = file_words + '\n\n' + str(out['7'][0])
    f.writelines(file_words)
    f.close()

    random.shuffle(out['1'])

    return out

def get_users_to_follow(username):
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
    out = users_list
    return out

def get_hashtag_posts(hashtag):
    api.getHashtagFeed(hashtag)
    result = api.LastJson
    result = result['items']
    out = []
    for post in result:
        try:
            media_id = post['caption']['media_id']
            out.append(media_id)
        except:
            asdfafdslkjafdsafdsadsf = 'asdffdasfasd'
    return out

def auto_comment_new():
    accounts = ['daquan','memes','rap','nbamemes','9gag','sarcasm_only','betches','memequeen','do_or_drink','fuckjerry','thefatjewish','funnymemes','ladbible']
    for account in accounts:
        api.searchUsername(account)
        result = api.LastJson
        try: #try because it sometimes, though not often, just randomely not work
            username_id = result['user']['pk']
            username = result['user']['username']
            user_posts = api.getUserFeed(username_id)
            result = api.LastJson
            result = result['items']
            latest = result[0]
            post_id = latest['pk']
            if post_id not in auto_commented_posts:
                api.comment(post_id,setting_dict['custom_comment'])
                auto_commented_posts.append(post_id)
        except:
            asdf = 2

def wait_time_generator(sleep_length):
    rate = int(sleep_length)
    bottom = rate * 0.75
    top = rate * 1.25
    return random.uniform(bottom,top)



screen.fill((255,255,255))
master_tasks = ''
if error != 'No Errors.':
    master_tasks = preload()

running = True
sleeping = False
last_run_time = time.time() #last_run_time holds in time.time() when the last time an action was done
wait_time = 0 #depending on the task, how many seconds between actions
last_mins = 0
celeb_last_action = 'unfollow'
recent_actions = ['Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity','Example activity']
last_break = time.time()
paused = False
#---------------------game loop--------------------------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255,255,255))
    something_changed = False


    #red if there's an error. Green if there are no errors
    if error_msg != 'No Errors.':
        show_text_left('Potential Error: ' + error_msg,7,480,(225,0,0))
    else:
        show_text_left('Logged in successfully. ' + error_msg,7,480,(0,225,0))


    #top left info menu
    show_text_left("Account: @"+str(setting_dict["username"]), 7, 10, (0,0,0))
    show_text_left("Follow Break: "+str(setting_dict["follow_break"] + ' m'), 7, 27, (0,0,0))
    show_text_left("Like Break: "+str(setting_dict["like_break"] + ' m'), 7, 44, (0,0,0))
    show_text_left("Comment Break: "+str(setting_dict["comment_break"] + ' m'), 7, 61, (0,0,0))
    show_text_left("Unfollow Break: "+str(setting_dict["unfollow_break"] + ' m'), 7, 78, (0,0,0))

    #calculate time elapsed for top right stopwatch
    end_time = time.time()
    time_elapsed = end_time - start_time
    time_elapsed_str = str(time_elapsed)
    if time_elapsed_str.find(".") > -1:
        time_elapsed_str = time_elapsed_str[0:time_elapsed_str.find(".")]
    time_elapsed = int(time_elapsed_str)
    secs = time_elapsed
    mins = secs // 60
    secs = secs % 60
    hours = mins // 60
    mins = mins % 60
    s_str = str(secs) + "s"
    m_str = str(mins) + 'm'
    h_str = str(hours) + 'h'
    show_text_right('Time elapsed: ' + h_str + ' ' + m_str,493,25,(0,0,0))
    if mins != last_mins:
        something_changed = True
    last_mins = mins

    #function display on top right
    show_text_right('Current Task: '+task,493,42,(0,0,0))


    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

    #function buttons on right side of screen
    button_number = 0

    button_number += 1
    pygame.draw.rect(screen,(0,102,204),[270,128,223,40]) #blue rectangle
    button_text("Follow/Unfollow Celebs",128+20) #text on button
    button_line(128+20) #line on left of button
    if mouse_x > button_areas[str(button_number)]['top_left_x'] and mouse_x < button_areas[str(button_number)]['bottom_right_x']:
        if mouse_y > button_areas[str(button_number)]['top_left_y'] and mouse_y < button_areas[str(button_number)]['bottom_right_y']:
            task = "Following/Unfollowing Celebs"
            task_num = 1
            something_changed = True
            paused = False
    
    button_number += 1
    pygame.draw.rect(screen,(0,102,204),[270,178,223,40])
    button_text("Follow Users",178+20)
    button_line(178+20)
    if mouse_x > button_areas[str(button_number)]['top_left_x'] and mouse_x < button_areas[str(button_number)]['bottom_right_x']:
        if mouse_y > button_areas[str(button_number)]['top_left_y'] and mouse_y < button_areas[str(button_number)]['bottom_right_y']:
            task = "Following Users"
            task_num = 2
            something_changed = True
            paused = False
    
    button_number += 1
    pygame.draw.rect(screen,(0,102,204),[270,228,223,40])
    button_text("Like Posts",228+20)
    button_line(228+20)
    if mouse_x > button_areas[str(button_number)]['top_left_x'] and mouse_x < button_areas[str(button_number)]['bottom_right_x']:
        if mouse_y > button_areas[str(button_number)]['top_left_y'] and mouse_y < button_areas[str(button_number)]['bottom_right_y']:
            task = "Liking Posts"
            task_num = 3
            something_changed = True
            paused = False
    
    button_number += 1
    pygame.draw.rect(screen,(0,102,204),[270,278,223,40])
    button_text("Comment on Hashtag",278+20)
    button_line(278+20)
    if mouse_x > button_areas[str(button_number)]['top_left_x'] and mouse_x < button_areas[str(button_number)]['bottom_right_x']:
        if mouse_y > button_areas[str(button_number)]['top_left_y'] and mouse_y < button_areas[str(button_number)]['bottom_right_y']:
            task = "Commenting on Hashtag"
            task_num = 4
            something_changed = True
            paused = False
    
    button_number += 1
    pygame.draw.rect(screen,(0,102,204),[270,328,223,40])
    button_text("Comment on New Posts",328+20)
    button_line(328+20)
    if mouse_x > button_areas[str(button_number)]['top_left_x'] and mouse_x < button_areas[str(button_number)]['bottom_right_x']:
        if mouse_y > button_areas[str(button_number)]['top_left_y'] and mouse_y < button_areas[str(button_number)]['bottom_right_y']:
            task = "Commenting on New Posts"
            task_num = 5
            something_changed = True
            paused = False
    
    button_number += 1
    pygame.draw.rect(screen,(0,102,204),[270,378,223,40])
    button_text("Unfollow All Users",378+20)
    button_line(378+20)
    if mouse_x > button_areas[str(button_number)]['top_left_x'] and mouse_x < button_areas[str(button_number)]['bottom_right_x']:
        if mouse_y > button_areas[str(button_number)]['top_left_y'] and mouse_y < button_areas[str(button_number)]['bottom_right_y']:
            task = "Unfollowing All Users"
            task_num = 6
            something_changed = True
            paused = False
    
    button_number += 1
    pygame.draw.rect(screen,(0,102,204),[270,428,223,40])
    button_text("Generate Hashtags",428+20)
    button_line(428+20)
    if mouse_x > button_areas[str(button_number)]['top_left_x'] and mouse_x < button_areas[str(button_number)]['bottom_right_x']:
        if mouse_y > button_areas[str(button_number)]['top_left_y'] and mouse_y < button_areas[str(button_number)]['bottom_right_y']:
            task = "Generating Hashtags"
            task_num = 7
            something_changed = True
            paused = False
    

    sleeping = True
    #checks whether the code should be sleeping or not
    if time.time() - last_run_time >= wait_time:
        sleeping = False
    else:
        sleeping = True

    #sleeps for 23 minutes for every 37 mins run
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    minutes = current_time[current_time.find(':')+1:len(current_time)]
    minutes = minutes[0:minutes.find(':')]
    minutes = int(minutes)
    if minutes >= 37:
        sleeping = True

    

    if paused == True:
        sleeping = True
    
    if error_msg == 'No Errors.' and sleeping == False:

        #wait times depending on task
        if task_num == 1 or task_num == 2:
            wait_time = wait_time_generator(int(setting_dict['follow_break']) * 60)
        if task_num == 3:
            wait_time = wait_time_generator(int(setting_dict['like_break']) * 60)
        if task_num == 4:
            wait_time = wait_time_generator(int(setting_dict['comment_break']) * 60)
        if task_num == 5:
            wait_time = wait_time_generator(30)
        if task_num == 6:
            wait_time = wait_time_generator(int(setting_dict['unfollow_break']) * 60)


        #action executer center
        if task_num == 1:
            just_followed = False
            if celeb_last_action == 'unfollow':
                username = master_tasks['1'][0]
                api.searchUsername(username)
                result = api.LastJson
                user_id = result['user']['pk']
                api.follow(user_id)
                recent_actions.insert(0,'Followed @' + master_tasks['1'][0])
                celeb_last_action = 'follow'
                sleeping = True
                something_changed = True
                last_run_time = time.time()
                just_followed = True
            if celeb_last_action == 'follow' and just_followed == False:
                username = master_tasks['1'][0]
                api.searchUsername(username)
                result = api.LastJson
                user_id = result['user']['pk']
                api.unfollow(user_id)
                recent_actions.insert(0,'Unfollowed @' + master_tasks['1'][0])
                celeb_last_action = 'unfollow'
                master_tasks['1'].pop(0)
                sleeping = True
                something_changed = True
                last_run_time = time.time()
        if task_num == 2:
            user_id = master_tasks['2'][0]['pk']
            api.follow(user_id)
            recent_actions.insert(0,'Followed @' + master_tasks['2'][0]['username'])
            master_tasks['2'].pop(0) #removes the first element
            sleeping = True
            something_changed = True
            last_run_time = time.time()
        if task_num == 3:
            post_id = master_tasks['3'][0]
            api.like(post_id)
            recent_actions.insert(0,'Liked a post')
            master_tasks['3'].pop(0)
            sleeping = True
            something_changed = True
            last_run_time = time.time()
        if task_num == 4:
            post_id = master_tasks ['4'][0]
            api.comment(post_id,setting_dict['custom_comment'])
            recent_actions.insert(0,'Commented on a post')
            master_tasks['4'].pop(0)
            sleeping = True
            something_changed = True
            last_run_time = time.time()
        if task_num == 5:
            auto_comment_new()
            recent_actions.insert(0,'Autocommented on a new post')
            sleeping = True
            something_changed = True
            last_run_time = time.time()
        if task_num == 6:
            user_id = master_tasks['6'][0]['pk']
            api.unfollow(user_id)
            recent_actions.insert(0,'Unfollowed @' + master_tasks['6'][0]['username'])
            master_tasks['6'].pop(0)
            sleeping = True
            something_changed = True
            last_run_time = time.time()


        #if any particular of the tasks lists empty: preload again
        if len(master_tasks['1']) <= 2:
            master_tasks = preload()
        if len(master_tasks['2']) <= 2:
            master_tasks = preload()
        if len(master_tasks['3']) <= 2:
            master_tasks = preload()
        if len(master_tasks['4']) <= 2:
            master_tasks = preload()


    #the "current state" of RUNNING or PAUSED depends soley on whether the pause button is active, not action breaks or scheduled breaks
    #pause button
    pygame.draw.rect(screen,(225,0,0),[270,78,223,40])
    #button line
    font = pygame.font.Font('freesansbold.ttf',15)
    text = font.render('|',True,(0,0,0))
    text_rect = text.get_rect()
    text_rect.centery = 98
    text_rect.left = 275
    screen.blit(text,text_rect)
    #button 'pause' text
    text = font.render('Pause',True,(0,0,0))
    text_rect = text.get_rect()
    text_rect.centery = 98
    text_rect.right = 485
    screen.blit(text,text_rect)
    #mouse detection
    if mouse_x > 270 and mouse_x < 493:
        if mouse_y > 78 and mouse_y < 118:
            paused = True
    if paused == False:
        #top right status
        font = pygame.font.Font('freesansbold.ttf',15)
        text = font.render('Current State: RUNNING',True,(0,0,0))
        text_rect = text.get_rect()
        text_rect.centery = 51
        text_rect.right = 493
        screen.blit(text,text_rect)
        something_changed = True
    if paused == True:
        #top right status
        font = pygame.font.Font('freesansbold.ttf',15)
        text = font.render('Current State: PAUSED',True,(0,0,0))
        text_rect = text.get_rect()
        text_rect.centery = 51
        text_rect.right = 493
        screen.blit(text,text_rect)
        something_changed = True


    #rectangle outline
    if paused == True:
        pygame.draw.rect(screen,(0,0,0),[270,78,223,40],4)
    if paused == False:
        if task_num == 1:
            pygame.draw.rect(screen,(0,0,0),[270,128,223,40],4)
        if task_num == 2:
            pygame.draw.rect(screen,(0,0,0),[270,178,223,40],4)
        if task_num == 3:
            pygame.draw.rect(screen,(0,0,0),[270,228,223,40],4)
        if task_num == 4:
            pygame.draw.rect(screen,(0,0,0),[270,278,223,40],4)
        if task_num == 5:
            pygame.draw.rect(screen,(0,0,0),[270,328,223,40],4)
        if task_num == 6:
            pygame.draw.rect(screen,(0,0,0),[270,378,223,40],4)
        if task_num == 7:
            pygame.draw.rect(screen,(0,0,0),[270,428,223,40],4)



    #recent actions console
    action_console('Recent Activity',148,20)
    pygame.draw.line(screen,(0,0,0),(7,160),(130,160),2)
    action_console(recent_actions[0],172,15)
    action_console_line(screen,184)
    action_console(recent_actions[1],196,15)
    action_console_line(screen,208)
    action_console(recent_actions[2],220,15)
    action_console_line(screen,232)
    action_console(recent_actions[3],244,15)
    action_console_line(screen,256)
    action_console(recent_actions[4],268,15)
    action_console_line(screen,280)
    action_console(recent_actions[5],292,15)
    action_console_line(screen,304)
    action_console(recent_actions[6],316,15)
    action_console_line(screen,328)
    action_console(recent_actions[7],340,15)
    action_console_line(screen,352)
    action_console(recent_actions[8],364,15)
    action_console_line(screen,376)
    action_console(recent_actions[9],388,15)
    action_console_line(screen,400)
    action_console(recent_actions[10],412,15)
    action_console_line(screen,424)
    action_console(recent_actions[11],436,15)

    

    if something_changed == True or time_elapsed <= 5:
        pygame.display.update()

    sleeping = True




#------------old console based interface----------------
#can still access if you press the top right X button of the GUI window


print(f'''{Fore.RESET}{Fore.CYAN}{Style.BRIGHT}{Back.BLACK} ''')
print("")
print('                                           ')
print('        /\                                 ')
print('       /  \  _   _ _ __ ___  _ __ __ _     ')
print("      / /\ \| | | | '__/ _ \| '__/ _` |    ")
print("     / ____ \ |_| | | | (_) | | | (_| |    ")
print("    /_/    \_\__,_|_|  \___/|_|  \__,_|    ")
print("       The Best IG Bot For The Buck        ")
print("                                           ")
print(f'''{Fore.RESET}{Fore.RED}{Style.NORMAL}  ''')
print('   By: GlassTea')
print('   Contact: https://lnky.in/glasstea')
print('   Released 4/21/2020')
print('   Version  2.0.5')
print(f'''{Fore.RESET}{Fore.YELLOW}{Style.BRIGHT}  ''')
print("********************************************")
print(f'''{Fore.RESET}{Fore.GREEN}{Style.BRIGHT}  ''')

access_codes = ['adminpass','1234qwerasdf']
access_code = input("Access code (hit enter if not applicable): ")
using_access_code = False
valid = False
if access_code in access_codes:
    valid = True
    using_access_code = True
if access_code == '':
    valid = True
while valid == False:
    access_code = input("Access code failed, please try again or hit enter: ")
    if access_code == '':
        valid = True
    if access_code in access_codes:
        valid = True
        using_access_code = True

username = input("Username: ")
valid = False
if username in allowed_users or using_access_code == True:
    valid = True
while valid == False:
    username = input("Sorry, your username is not cleared to use this program, please try again: ")
    if username in allowed_users:
        valid = True

password = input("Password: ")
print('Attempting to log in...')
valid = False
api = InstagramAPI(username,password)
api.login()
result = api.LastJson
try:
    msg = result['message']
except:
    valid = True
while valid == False:
    password = input("Incorrect Password, please try again: ")
    print('Attempting to log in...')
    api = InstagramAPI(username,password)
    api.login()
    result = api.LastJson
    try:
        msg = result['message']
    except:
        valid = True
        print('Successfully logged into @'+username)
api.USER_AGENT = 'Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1200; Xiaomi; HM lsW; armani; qcom; en_US)'

print("")
print("[1] Auto Follow/Unfollow Celebrities")
print("[2] Auto Follow Users")
print("[3] Auto Like Posts")
print("[4] Auto Comment on Hashtags")
print("[5] Auto Comment on New Posts")
print("[6] Unfollow All Users")
#print("[4] Find users who don't follow back")
print("[7] Generate Hashtags")
print("[8] Test Module")
print('')
function = get_int_input([1,8],'What would you like to do')
'''
print('')
print('')
print('[1] Meme Community')
print('[2] Art Community')
print('[3] Luxury Community')
print('[4] Motivation Community')
print('[5] Gaming Community')
print('')
category = input('Which audience would you like to target (input a number): ')
if type(category) == int:
    category = int(category)
    valid = True
else:
    while valid == False:
        try:
            category = int(category)
            if category < 6:
                valid = True
            else:
                category = input('Error. Please enter a number between 1-5: ')
        except:
            category = input('Error. Number invalid, please try again: ')
temp = ['memes','art','luxury','motivation','gaming']
category_str = temp[category-1]
'''
input_int = int(function)
execute_function(input_int)

print('')
print('')
print('')
print('')
asdlfkj = input('Press enter to close window')