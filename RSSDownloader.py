# NOTE: This was moved to RSSfuncs and is deprecaiated


"""
Author : 
Contact: thejdunbar+github@gmail.com
PriorSource: https://github.com/securityinfive/RSSDownloader

Python script to download MP3 files from a podcast's RSS feed.
Usage:
   - Simply enter the URL for the RSS feed.
   - Enter a local directory where the mp3 files will download to.
   - Run and enter the number of files you want to download from the feed.
        - Specific number within the range of the episodes/files in the feed.
        - Enter 0 and it will download all the files in the feed.


"""
import wget
import feedparser
import glob
import os
from pathlib import Path
from os import makedirs

# RSS Feed to download and local location to download files too
# RSS_Target = <https link to the RSS feed> "https://securityinfive.libsyn.com/rss"
# local_target_dir = <local directory 'C:\foldername\target' format> "C:\Dev\PodcastArchive"

# ListOfFeeds=["https://www.manager-tools.com/podcasts/basics-rss.xml"
# ,"https://files.manager-tools.com/files/public/feeds/hall-of-fame.xml"
# ,"https://files.manager-tools.com/files/public/feeds/the-effective-manager-book.xml"
# ,"https://files.manager-tools.com/files/public/feeds/hiring.xml"
# ,"https://files.manager-tools.com/files/public/feeds/one-on-ones.xml"
# ,"https://files.manager-tools.com/files/public/feeds/feedback.xml"
# ,"https://files.manager-tools.com/files/public/feeds/coaching.xml"
# ,"https://files.manager-tools.com/files/public/feeds/delegation.xml"
# ,"https://files.manager-tools.com/files/public/feeds/new-manager.xml"
# ,"https://files.manager-tools.com/files/public/feeds/management-basics.xml"
# ,"https://files.manager-tools.com/files/public/feeds/project-management.xml"
# ,"https://files.manager-tools.com/files/public/feeds/politics.xml"
# ,"https://files.manager-tools.com/files/public/feeds/presentations.xml"]
# ListOfFeeds=["https://files.manager-tools.com/files/public/feeds/politics.xml"]
ListOfFeeds = [
    "https://files.manager-tools.com/files/public/feeds/politics.xml",
    "https://files.manager-tools.com/files/public/feeds/presentations.xml",
]


RSS_Target = "https://www.manager-tools.com/podcasts/basics-rss.xml"

# local_target_dir = "/home/blitzaction/SynologyDrive/-=LEARN=-/2021RELEARN/Podcasts/Hall-of-fame"
# RSS_Target = "https://files.manager-tools.com/files/private/feeds/fada28dae9/executive-tools-podcasts.xml"
# local_target_dir = "/home/blitzaction/SynologyDrive/-=LEARN=-/2021RELEARN/ExecutiveTools"


# tempcode

parent_dir = "/home/blitzaction/SynologyDrive/-=LEARN=-/2021RELEARN/Podcasts/"
folder = Path((RSS_Target[RSS_Target.find("feeds/") + 6 : 99])).stem.capitalize()
local_target_dir = os.path.join(parent_dir, folder)
if not os.path.exists(local_target_dir):
    os.makedirs(local_target_dir)
    print("Directory '% s' created" % folder)


def get_input(rss_len):
    how_many_downloaded = ""
    # Proper grammar
    if rss_len == 0:
        rss_text = "no"
        rss_episodes_text = "episodes"
    elif rss_len == 1:
        rss_text = "is"
        rss_episodes_text = "episode"
    elif rss_len > 1:
        rss_text = "are"
        rss_episodes_text = "episodes"

    # Prompt for how many files to download
    print(
        "There "
        + rss_text
        + " "
        + str(rss_len)
        + " "
        + rss_episodes_text
        + " in this feed."
    )
    print("RSS feeds are ordered from most recent entries first, descending order in.")
    print(
        "If an episode exists in the target directory the download will skip that file."
    )
    print("-------------------------------")
    how_many_downloaded = "0"
    # how_many_downloaded = input("How many recent episodes to download? Enter 0 for them all. - ")
    print("-------------------------------")

    return how_many_downloaded


# Error checking for the input on How_Many and if How_Many is GT rss_length
def validate_input(how_many_num, rss_len):
    # Check to see if the user input is a number
    if (how_many_num.isnumeric()) == True:
        # Check to see if it's between 0 and the max number of episodes in the feed
        if int(how_many_num) < 0 or int(how_many_num) > int(rss_len):
            print("INPUT ERROR - Please Enter A Number Between 0 And " + str(rss_len))
            validated = 0
        else:
            validated = 1
    else:
        print("INPUT ERROR - Please Enter A Number Only.")
        validated = 0

    # Return a 1 or 0, guess which means what.
    return validated


def Get_Feed(rss_to_load):
    # Load the RSS Feed
    print("Getting feed - " + rss_to_load + " please wait...")
    rss_feed_load = feedparser.parse(rss_to_load)
    rss_length = len(rss_feed_load.entries)
    print("Feed loaded.")

    # Pass back a list
    return rss_feed_load, rss_length


def Download_Files(target_dir, rss_feed, how_many_to_get):
    # Initialize the download counter
    episode_count = 1
    # Get all the mp3 files in the target directory to skip over existing files and put in a list.
    # Get all the mp3 files in the target directory and load it into a list
    os.chdir(target_dir)
    current_files = []
    for file in glob.glob("*.mp3"):
        current_files.append(file)

    # FOR LOOP THROUGH EPISODES IN FEED
    for episode in rss_feed.entries:
        entry_links = episode.links
        # second entry for the mp3 link
        # .links has the download in the second entry
        mp3_link = entry_links[1]
        mp3_href = mp3_link["href"]

        # Strip out the mp3 file from the download URL for directory search
        # Break out the / directories from the URL
        temp_mp3_link = mp3_href.split("/")
        # Get the count of the URL items, then get position of the mp3 file,
        # the mp3 file will be the last entry http://example.com/epsiode/whatever/something/episode_111.mp3
        temp_mp3_link_last = (
            len(temp_mp3_link) - 1
        )  # minus one because of the array numbering
        # MP3 filename
        temp_mp3_link = temp_mp3_link[temp_mp3_link_last]

        # Make sure the last entry is a .mp3 file
        if ".mp3" in temp_mp3_link:
            # Check to see if there are headers on the URL after .mp3, break them out to get the .mp3 file name
            # Example: http://example.com/epsiode/whatever/something/episode_111.mp3?redirect=1&name=something&where=9
            # If there is no ?, the var is already set to the proper mp3 filename.
            if "?" in temp_mp3_link:
                temp_mp3_link = temp_mp3_link.split("?")
                # Grab the first item, the second will be the headers
                temp_mp3_link = temp_mp3_link[0]

        # See if the mp3 file already exists in the target directory for download
        # If yes, skip it. If not, download it.
        if temp_mp3_link in current_files:
            print("File Exists - SKIPPING DOWNLOAD - " + temp_mp3_link)
        else:
            print("Downloading - " + str(temp_mp3_link))
            wget.download(mp3_link["href"], target_dir)

        # Iterate the entered count, break out when hit the entered file count
        # If How_Many is 0 the For loop will run to the end.
        if int(how_many_to_get) > 0:
            if str(episode_count) == str(how_many_to_get):
                print("--- DOWNLOAD COMPLETE ---")
                break
            else:
                episode_count = episode_count + 1
    # --- END FOR ---

    # Kick out Complete message when done with all episodes when input is 0
    if int(how_many_to_get) == 0:
        print("--- DOWNLOAD COMPLETE ---")


# -----------------------------------------------------------------------

# Get Started, Load the RSS and break out the feed and file count from the feed
RSS_Feed = Get_Feed(RSS_Target)
RSS_Feed_Items = RSS_Feed[0]
RSS_Feed_Count = RSS_Feed[1]

# User input for number of files to download and make sure user input is clean
is_valid = 0
while is_valid == 0:
    How_Many = get_input(RSS_Feed_Count)
    is_valid = validate_input(How_Many, RSS_Feed_Count)
else:
    if int(How_Many) == 0:
        File_Count = "All files to - "
    elif int(How_Many) == 1:
        File_Count = str(How_Many) + " file to - "
    else:
        File_Count = str(How_Many) + " files to - "
    print("Downloading " + File_Count + local_target_dir)
    Download_Files(local_target_dir, RSS_Feed_Items, How_Many)

# beep at the end
import os

beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
beep(3)

# End Of Line
