import requests
import datetime
import re
import time
import praw
import argparse
import html.parser as htmlparser


#channel should look like channel/UC7pp40MU_6rLK5pvJYG3d0Q or user/cgpgrey/
#subreddit should like like /r/videos
parser = argparse.ArgumentParser()
parser.add_argument("--c", help="channel link, no beginning or ending slashes")
parser.add_argument("--s", help="subreddit, in /r/askreddit form")

args = parser.parse_args()

textParser = htmlparser.HTMLParser()


#setup your reddit user and password here
redditUsername = ""
redditPassword = ""

videoCheckDelay = 10

if redditUsername == "" or redditPassword == "":
	exit("You forgot to setup reddit username and pass")


if args.c:
	channelName = args.c
else:
	channelName = input("Enter channel link, no beginning or ending slashes ")
	
if args.s:
	subreddit = args.s
else:
	subreddit = input("Enter subreddit in /r/askreddit form ")
	


myYt = (channelName, subreddit)





def submit_link_post(subreddit, title, link, redditUsername, redditPassword):
	#format = submit_link_post('/r/test', "Click for reddit homepage", 'http://www.reddit.com')
	
	
	title = textParser.unescape(title)
	
	usr = redditUsername
	password = redditPassword
	r = praw.Reddit(user_agent="yt-video-poster")
	sub = r.get_subreddit(subreddit)
	r.login(usr, password, disable_warning=True)
	
	
	print("trying to submit with")
	print("----------")
	print(subreddit)
	print(title)
	print(link)
	
	
	try:
	
		sub.submit(title, url=link, resubmit=True)
	
	except Exception as e:
		logError(str(e))
		print(str(e))
	
	
	

def write_to_debug(info):
	file = open("debug.html", "w")
	file.write(info)
	file.close()

def get_date_string():
	currentTime = datetime.datetime.now()
	month = str(currentTime.month)
	day = str(currentTime.day)
	year = str(currentTime.year)
	
	hour = currentTime.hour
	if hour > 12: 
		hour = hour - 12
		
	hour = str(hour)
	
	minute = str(currentTime.minute)
	sec = str(currentTime.second)
	
	fullTimeString = month + "/" + day + "/" + year + " " + hour + ":" + minute + ":" + sec
	
	return fullTimeString


def logError(error):
	
	f = open("errors.txt", "a")
	f.write(get_date_string() + "   " +  error + "\n")
	f.close()

def download_webpage(url):
	try:
		resp = requests.get(url)
		return resp.text
	except Exception as e:
		logError("ERROR with url: " + str(url) + " " + str(e))
		print("ERROR in download_webpage " + str(e))
		return 0
		
	
	
	
def match_videos(webpage_string):
	results = re.findall(r'dir="ltr" title="(.+?)".+href="(.+?)"', webpage_string) #first () matches title, seconds () matches the /watch?=
	return results[0:1] #return first

def get_5_most_recent_videos(username):
	starturl = "https://www.youtube.com/"
	middleurl = username
	endurl = "/videos?flow=grid&sort=dd&view=0&nohtml5=False"
	
	fullUrl = starturl + middleurl + endurl
	
	webpage = download_webpage(fullUrl)
	
	return match_videos(webpage)
	


	
	
def check_for_new_videos(info, redditUsername, redditPassword):
	#info is tuple (channelUrl, subreddit to post)
	
	username = info[0]
	subreddit = info[1]
	
	
	videos = get_5_most_recent_videos(username)
	time.sleep(1)
	i = 0
	while 1:
		newvideos = get_5_most_recent_videos(username)
		
		
		if not newvideos == videos:
			print("NEW VIDEO DETECTED")
			print(newvideos[0][0], newvideos[0][1])
			videoTitle = newvideos[0][0]
			videoUrl = "http://www.youtube.com" + newvideos[0][1]
			
			
			
			submit_link_post(subreddit, videoTitle, videoUrl, redditUsername, redditPassword)
			
		else:
			print("no new video detected " + str(i))
			print(videos)
			print(newvideos)
			
		i += 1
			
			
		videos = newvideos
		time.sleep(videoCheckDelay)
			
		
		
		



	
check_for_new_videos(myYt, redditUsername, redditPassword)