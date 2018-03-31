
# coding: utf-8

# In[1]:


import pylast
from datetime import datetime  
from datetime import timedelta 
import csv
from datetime import time
import urllib
import xmltodict
import pandas as pd
import os
from datetime import date


# In[2]:

#see which week the scrbble is in.
def get_week(scrobbled_time):
    scrobbled_time = datetime.fromtimestamp(int(scrobbled_time))
    last_friday = (scrobbled_time.date()
        - timedelta(days=scrobbled_time.weekday())
        + timedelta(days=4, weeks=-1))
    last_friday_at_00 = datetime.combine(last_friday, time(1))
    one_week = timedelta(weeks=1)
    if scrobbled_time - last_friday_at_00 >= one_week:
        last_friday += one_week
    next_thursday = last_friday + timedelta(days=6)
    return str(last_friday)+ " to "+ str(next_thursday)


# In[3]:

# save the downloaded data
def save(track_list,start,end,save_file, totalPages):
    print("Saving")
    if track_list == []:
        return
    backup_file = open('Temp.csv', 'w')
    with backup_file:
        fieldnames = ['Week','Time','Artist','Artist mbid','Title','Track mbid','Album','Album mbid','Tags','Album art','Timestamp']
        writer = csv.DictWriter(backup_file,fieldnames=fieldnames,lineterminator = '\n')
        writer.writerows(track_list)
    backup_file.close()
    try:
        combined_data = pd.DataFrame()
        combined = []
        a = pd.read_csv(save_file, header =None)
        b = pd.read_csv('Temp.csv', header =None)
        combined.append(b)
        combined.append(a)
        combined_data = pd.concat(combined, ignore_index=True)
        combined_data.to_csv(save_file,index = None, header = None)
    except Exception,e:
        print(e)
        os.rename('Temp.csv', save_file)
    log_str = "Saved page "+str(start)+" to "+str(end)+" out of "+totalPages+" pages."
    print(log_str)
    with open(username+'_log.txt','w') as config:
        config.write(log_str)


# In[4]:

# get top tags from the scrobble, by default, 3 are fetched
def get_tags(artist, track):
    url_str = 'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&api_key='+API_KEY+'&artist='+artist+'&track='+track
    page = urllib.urlopen(url_str)
    parsed_page = xmltodict.parse(page)
    try:
        tags = parsed_page['lfm']['toptags']['tag']
    except:
        tags = []
    tag_list = ''
    for i in range(3):
        try:
            tag_list = tag_list + str((tags[i]['name']).encode('utf-8')) +", "
        except:
            1
    return tag_list


# In[5]:

# fetch data from last.fm api
def get_pages(start,end,save_file):
    global last_backup
    try:
        with open(save_file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            last_backup = int(float(next(reader)[10]))
            print("Last backup on: "+ str(last_backup))
    except Exception,e:
        print(e)
        print("First backup. This may take a while.")
        last_backup = 0
    track_list = []
    page_number = start
    while page_number <= end:
        url_str = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='+username+'&api_key='+API_KEY+'&limit=50&page='+str(page_number)
        print("Downloading page: "+str(page_number))
        page = urllib.urlopen(url_str)
        parsed_page = xmltodict.parse(page)
        parsed_page = parsed_page['lfm']
        recenttracks = parsed_page['recenttracks']
        page = recenttracks['@page']
        perPage = recenttracks['@perPage']
        totalPages = recenttracks['@totalPages']
        total_scrobbles = recenttracks['@total']
        tracks_on_page = recenttracks['track']
        i = 1
        for track in tracks_on_page:
            track_details = {}
            try:
                track['@nowplaying']
            except:
                try:
                    artist = str((track['artist']['#text']).encode('utf-8'))
                except:
                    artist = ""
                track_details["Artist"] = artist
                try:
                    artist_mbid = str((track['artist']['@mbid']).encode('utf-8'))
                except:
                    artist_mbid = ""
                track_details["Artist mbid"] = artist_mbid
                try:
                    title = str((track['name']).encode('utf-8'))
                except:
                    title = ''
                track_details["Title"] = title
                try:
                    track_mbid = str((track['mbid']).encode('utf-8'))
                except:
                    track_mbid = ''
                track_details["Track mbid"] = track_mbid
                print(i,title)
                track_details["Tags"] = get_tags(artist,title)
                try:
                    album = str((track['album']['#text']).encode('utf-8'))
                except:
                    album = ''
                track_details["Album"] = album
                try:
                    album_mbid = str((track['album']['@mbid']).encode('utf-8'))
                except:
                    album_mbid = ""
                track_details["Album mbid"] = album_mbid
                try:
                    timestamp = str((track['date']['@uts']).encode('utf-8'))
                except:
                    timestamp = ''
                track_details["Timestamp"] = timestamp
                try:
                    week = get_week(timestamp)
                except:
                    week = ''
                track_details["Week"] = week
                if int(timestamp) == last_backup:
                    print("Break. Reached last backup.")
                    return track_list
                else:
                    time = str((track['date']['#text']).encode('utf-8'))
                    track_details["Time"] = time
                try:            
                    for image in track['image']:
                        if image['@size'] == 'extralarge':
                            album_art = image['#text']
                        else:
                            album_art = None
                    track_details["Album art"] = album_art
                except:
                    track_details["Album art"] = None
                track_list.append(track_details)
                i+=1
        page_number = page_number+1
    return track_list


# In[6]:

# please get your own 
def main():
    global API_KEY
    API_KEY = "YOUR_API_KEY"  # this is a sample key
    global username
    username = raw_input("Please enter your Last.FM username: ")
    save_file = username +".csv"
    url_str = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='+username+'&api_key='+API_KEY+'&limit=50'
    page = urllib.urlopen(url_str)
    parsed_page = xmltodict.parse(page)
    totalPages = parsed_page['lfm']['recenttracks']['@totalPages']
    print(str(totalPages)+" pages to backup.")
    try:
        with open(username+"_log.txt") as f:
            text = f.readline()
            integers = [int(s) for s in text.split() if s.isdigit()]
            if integers[0] == 0:
                new_pages = int(totalPages) - integers[2]
                print(str(new_pages)+ " new pages found since last backup.")
                num_of_pages = int(raw_input("Please enter the number of pages to backup each cycle: "))
                end = new_pages+1
                start = end - num_of_pages+1
                if start <=0:
                    start = 1
            else:
                end = integers[0]-1
                num_of_pages = integers[1] - integers[0] +1
                start = end-num_of_pages+1
                print("Log found. Finishing off unfinished event.")
                if start <=0:
                    start = 1
                if end <=0:
                    end = start+num_of_pages-1
    except Exception,e:
        print(e)
        num_of_pages = int(raw_input("Please enter the number of pages to backup each cycle: "))
        end = int(totalPages)
        start = end-num_of_pages+1
    n=1
    while  n<10:
        scrobbles = get_pages(start,end,save_file)
        save(scrobbles,start,end, save_file, str(totalPages))
        start = start-num_of_pages
        if start <=0:
            start = 1
            n+=1
        end = end-num_of_pages
        if end <=0:
            end = start+num_of_pages
    print("Backup finished")
    log_str = "Saved page 0 to 0 out of "+totalPages+" pages."
    with open(username+'_log.txt','w') as config:
        config.write(log_str)


# In[7]:


if __name__ == "__main__":
    main()

