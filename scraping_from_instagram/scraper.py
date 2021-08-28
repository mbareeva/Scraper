from instabot import Bot
import json
import time

## Login to the Instagram account ##
bot = Bot()
bot.login(username = "jacob1223steiner",  password = "123456jacob") #insert your login and password for Instagram
usersFinal = []

## Open file with a list of usernames. Afterwards, extract
# the profile information (username, full name, biography) 
# and media information (likes and captions) for users.
with open('../usernames.json') as json_file:
  usernames = json.load(json_file)
  for username in usernames:
    print(username)
    time.sleep(10);
    user_id = bot.get_user_id_from_username(username)
    user_info = bot.get_user_info(user_id)
    time.sleep(5);
    last_user_medias = bot.get_user_medias(username, filtration = None) # array of media_id. each media_id = media_pk_user_id
    user_media_content = [];
    for i in last_user_medias:
      media_id = i
      media_info_all = bot.get_media_info(media_id)[0] #json obj
      #print(media_info_all)
      if media_info_all is not None and media_info_all.get("caption") is not None:
        if media_info_all.get("caption").get("text") is not None:
          media_info_essentials = {"caption": media_info_all.get("caption").get("text"), "likes": media_info_all.get("like_count"), "commentsCount": media_info_all.get("comment_count")}
          user_media_content.append(media_info_essentials)
    if not isinstance(user_info, bool):
      user_info_essentials = {
        "fullname": user_info.get("full_name") if user_info.get("full_name") is not None else "",
        "biography": user_info.get("biography") if user_info.get("biography") is not None else "",
        "followers_count": user_info.get("follower_count") if user_info.get("follower_count") is not None else "",
        "follows_count": user_info.get("following_count") if user_info.get("following_count") is not None else "",
        "website": user_info.get("external_url") if user_info.get("external_url") is not None else "",
        "profileCategory": user_info.get("account_type") if user_info.get("account_type") is not None else "",
        "specialisation": user_info.get("category") if user_info.get("category") is not None else "",
        "location": user_info.get("city_name") if user_info.get("city_name") is not None else "",
        "username": username,
        "role": "influencer",
        "latestMedia": user_media_content
      }
      usersFinal.append(user_info_essentials);

with open("final_info.json", "rt") as f:
  data = json.load(f);
with open("final_info.json", "at") as f:
  json.dump(data + usersFinal, f);

bot.logout()