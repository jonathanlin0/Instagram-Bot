# unfollows everyone you're following
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import json
from time import sleep
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()


USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

logger = logging.getLogger()

cl = None

def login_user():
    global cl
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                print("Successfully logged in using existing session.")
                cl.get_timeline_feed()
            except LoginRequired:
                print("Session is invalid, need to login via username and password")
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
                print("Successfully logged in using username and password.")
            login_via_session = True
        except Exception as e:
            print("Couldn't login user using session information: %s" % e)
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            print("Attempting to login via username and password. username: %s" % USERNAME)
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            print("Couldn't login user using username and password: %s" % e)
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        print("Couldn't login user with either password or session")
        raise Exception("Couldn't login user with either password or session")

def get_following_users(username):
    user_id = cl.user_id_from_username(username)
    following = cl.user_following(user_id)
    
    following_list = []
    for user in following.values():
        following_list.append(user.pk)
        # following_list.append({
        #     'user_id': user.pk,
        #     'username': user.username,
        #     'full_name': user.full_name,
        #     'profile_pic_url': str(user.profile_pic_url)
        # })
    
    return following_list

def unfollow_users(following_users):
    for user in following_users:
        user_id = user['user_id']
        cl.user_unfollow(user_id)
        print(f"Unfollowed User ID: {user_id}, Username: {user['username']}")

# login to Instagram
login_user()

# read in existing followed and unfollowed data
with open("growth/unfollowed.txt", "r") as f:
    unfollowed = f.read().split("\n")
    if unfollowed[-1] == "":
        unfollowed.pop()

with open("growth/followed.txt", "r") as f:
    followed = f.read().split("\n")
    if followed[-1] == "":
        followed.pop()

if len(followed) == 0:
    print("No users to unfollow. Grabbing users you are following.")
    followed = get_following_users(USERNAME)

# how many people we unfollowed in this batch
unfollow_cnt = 0
while len(followed) > 0:
    user_id = followed.pop()
    if user_id not in unfollowed:
        try:
            cl.user_unfollow(user_id)
            print(f"Unfollowed User ID: {user_id}")
        except Exception as e:
            print(f"Error unfollowing User ID: {user_id}")

        # update files
        unfollowed.append(user_id)
        with open("growth/unfollowed.txt", "w") as f:
            f.write("\n".join(unfollowed))
        with open("growth/followed.txt", "w") as f:
            f.write("\n".join(followed))
    
        unfollow_cnt += 1
    
    # wait to prevent ratelimiting
    wait_time = np.clip(np.random.normal(120, 30), 30, 360)
    sleep(wait_time)

    if unfollow_cnt % 30 == 0:
        print("Sleeping for 4h")
        sleep(4 * 60 * 60)