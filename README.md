# Youtube-To-Reddit-Bot
Scrapes youtube for new uploads from a specific user and posts them to a desired subreddit

![Screenshot](http://i.imgur.com/kGgNKEo.png)

#Usage
  * Edit the variables ```redditUsername``` and ```redditPassword``` to include a valid reddit account that is eligable to submit link posts
  * Call the function using ```python yt2reddit.py --c user/cgpgrey --r /r/askreddit``` (format must be exact same)
  * Optionally, you can set a custom delay by editing the variable videoCheckDelay (number of seconds to wait before "refreshing" the page)
