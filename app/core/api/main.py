from .youtube_statistics import YTStats
import schedule
import time

API_KEY = "AIzaSyA-DPbYvdAHukZv_PRds602JVuZE9oQbyE" #add api_key here
channel_id = 'UCvBhHog2dCsBSJw0F_fdlfA' #add channel id here

class FetchData:
    """
    Get the Youtube video statistics and tags for each video id of a channel
    """
    yt = YTStats(API_KEY, channel_id)
    yt.get_channel_data()
    yt.get_channel_video_data()
    yt.tag()
    yt.dumpTsat()
    yt.indVideoPerformance()

    def cronTask(yt):
        """
        Iterate the process with a time interval of 3 minutes for 20 times.
        At 60th minutes, the performance score for each video will be generated.
        After that, the scheduler will shut off.
        """
        mT = YTStats(API_KEY, channel_id)
        mT.get_channel_data()
        mT.get_channel_video_data()
        mT.tag()
        currentState = mT.returnCurrentState()
        yt.checkStats(currentStats=currentState)
        mT.dumpTsat()
        if(mT.timeCount == 20):
            mT.indVideoPerformance()
        return schedule.CancelJob

    schedule.every(3).minutes.do(cronTask, yt=yt)

    while True:
        schedule.run_pending()
        if not schedule.jobs:
            break
        time.sleep(1)