from .youtube_statistics import YTStats
import schedule
import time

API_KEY = "AIzaSyBXKLfnBCE39OGpOv_88eXLKTpOhFlwqV4" #add api_key here
channel_id = 'UCvBhHog2dCsBSJw0F_fdlfA' #add channel id here

class FetchData:
    """
    01. Extract Youtube video statistics and tags for each video id of a channel.
    02. Get Initial Individual Video Performance by the individual video view count divided by the channel's all videos view count median.
    """
    wait_time = 3
    yt = YTStats(API_KEY, channel_id)
    yt.get_channel_data()
    yt.get_channel_video_data()
    yt.tag()
    yt.dumpTsat()
    yt.indVideoPerformance()

    def cronTask(yt):
        """
        01. Iterate the process with 3 minutes time interval for 1 hour.
        02. Get the 1st hour performance score for each video using view count divided by the channel's all videos view count median.
        03. Scheduler will run for 1 hour and then will exit.
        """
        time_count = 20
        mT = YTStats(API_KEY, channel_id)
        mT.get_channel_data()
        mT.get_channel_video_data()
        mT.tag()
        currentState = mT.returnCurrentState()
        yt.checkStats(currentStats=currentState)
        mT.dumpTsat()
        if(mT.timeCount == time_count):
            mT.indVideoPerformance()
            return schedule.CancelJob

    schedule.every(wait_time).minutes.do(cronTask, yt=yt)

    while True:
        schedule.run_pending()
        if not schedule.jobs:
            break
        time.sleep(1)
