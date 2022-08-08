import requests
import json
from tqdm import tqdm
from itertools import count
import statistics
from ..models import *


class YTStats:
    _timeCount = count(0)
    
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None
        self.video_id = []
        self.tags = {}
        self.stats = {}
        self.tstats = {}
        self.idWithTags = []
        self.timeCount = next(self._timeCount)
        self.tstatList = []
        self.perfList = []
        


    def get_channel_data(self):
        """Extract Channel Statistics for a Channel ID"""
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        pbar = tqdm(total=1)

        json_url = requests.get(url)
        data = json.loads(json_url.text)

        try:
            data = data["items"][0]["statistics"]
        except KeyError:
            data = None
        
        self.channel_statistics = data
        pbar.update()
        pbar.close()
        return data


    def get_channel_video_data(self):
        """ 
        Extract all the video ids for youtube data api v3
        and get all the statistics and snippets of each video
        """
        channel_videos = self._get_channel_videos(limit=50)

        parts = ["snippet", "statistics"]
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
                self.video_id.append(video_id)

        self.video_data = channel_videos
        return channel_videos


    def _get_single_video_data(self, video_id, part):
        """
        Extract tags, viewCount, likeCount, favoriteCount, commentCount for a single video
        Parts are Snippet and Statistics
        """
        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text) 

        try:
            data = data['items'][0][part]
        except KeyError as e:
            data = dict()
        return data


    def _get_channel_videos(self, limit = None):
        """
        Extract all the videos of a channel and check available search pages
        """
        url =  f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date"
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)

        vid, npt = self._get_channel_videos_per_page(url)
        idx = 0
        while(npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            next_vid, npt = self._get_channel_videos_per_page(nexturl)
            vid.update(next_vid)
            idx += 1
        return vid


    def _get_channel_videos_per_page(self, url):
        """
        Extract all videos per page
        Return channel_videos, nextPageToken
        """
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()

        if 'items' not in data:
            return channel_videos, None
        
        item_data = data['items']
        nextPageToken = data.get('nextPageToken', None)

        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError as e:
                e.message, e.args

        return channel_videos, nextPageToken


    def tag(self):
        """
        Get tags from Snippet part and combine all data
        """
        if self.video_data is None:
            return

        for id in self.video_id:
            t = self.video_data[id]

            if("tags" in t.keys()):
                tempTag = {id: t["tags"]}
                combineTags = t["tags"]
            else:
                tempTag = {id: []}
                combineTags = []

            self.tags.update(tempTag)
            self.stats.update({id: {"viewCount": self.video_data[id]["viewCount"],"likeCount": self.video_data[id]["likeCount"],"favoriteCount": self.video_data[id]["favoriteCount"],"commentCount": self.video_data[id]["commentCount"]}})
            self.tstats.update({id:{"video_id": id, "tags": ", ".join(combineTags), "viewCount": self.video_data[id]["viewCount"],"likeCount": self.video_data[id]["likeCount"],"favoriteCount": self.video_data[id]["favoriteCount"],"commentCount": self.video_data[id]["commentCount"]}})


    def dumpTsat(self):
        """
        Dump tags with statistics data into a JSON file 
        and store for each video_id into PostgreSQL DB
        """
        for _, value in self.tstats.items():
            self.tstatList.append(value)

        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = channel_title.replace(" ", "_").lower()
        f_name = channel_title+'.json'
        with open(f_name, 'w') as f:
            json.dump(self.tstatList, f, indent=4)
        
        for i in self.tstatList:
            if YTstats.objects.filter(video_id=i['video_id']).exists():
                YTstats.objects.filter(video_id=i['video_id']).update(tags=i['tags'], viewCount=i['viewCount'], likeCount=i['likeCount'], favoriteCount=i['favoriteCount'], commentCount=i['commentCount'])
            else:
                YTstats.objects.create(video_id=i['video_id'], tags=i['tags'], viewCount=i['viewCount'], likeCount=i['likeCount'], favoriteCount=i['favoriteCount'], commentCount=i['commentCount'])
                
        
    def returnCurrentState(self):
        """
        Return the current state of the data
        """
        return self.stats


    def medianView(self):
        """
        Get Median of all videos of a channel
        """
        viewList = []
        for id in self.video_id:
            viewList.append(int(self.stats[id]["viewCount"]))
        viewMedian = statistics.median(viewList)
        return viewMedian


    def indVideoPerformance(self):
        """
        Return Invidiual Video Performance with viewCount of each video 
        divided by the total viewCount of all videos Median and
        Dump the result into JSON and store them for each video_id into PostgreSQL DB
        """
        viewMedian = self.medianView()
        performanceData = {}
        for id in self.video_id:
            performance = int(self.stats[id]["viewCount"])/viewMedian
            performanceData.update({id: {"vid": id, "performance": performance}})

        for _, value in performanceData.items():
            self.perfList.append(value)
        
        f_name = 'performance.json'
        with open(f_name, 'w') as f:
            json.dump(self.perfList, f, indent=4)
        
        for i in self.perfList:
            stat = YTstats.objects.get(video_id=i['vid'])
            if YTperf.objects.filter(vid=stat).exists():
                YTperf.objects.filter(vid=stat).update(vid=stat, performance=i['performance'])
            else:
                YTperf.objects.create(vid=stat, performance=i['performance'])


    def checkStats(self, currentStats):
        """
        This function checks if the count of any statistics changes over time
        """
        for id in self.video_id:
            pView = self.stats[id]["viewCount"]
            pLike = self.stats[id]["likeCount"]
            pfav = self.stats[id]["favoriteCount"]
            pComment = self.stats[id]["commentCount"]

            nView = currentStats[id]["viewCount"]
            nLike = currentStats[id]["likeCount"]
            nfav = currentStats[id]["favoriteCount"]
            nComment = currentStats[id]["commentCount"]

            if(pView != nView):
                self.stats[id]["viewCount"] = nView
            if(pLike != nLike):
                self.stats[id]["likeCount"] = nLike
            if(pfav != nfav):
                self.stats[id]["favoriteCount"] = nfav
            if(pComment != nComment):
                self.stats[id]["commentCount"] = nComment