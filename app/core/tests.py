from django.urls import reverse
from rest_framework.test import APITestCase
from .api.serializers import *
from .models import *

class VideoListTestCase(APITestCase):

    def setUp(self):
        self.video_stat = YTstats.objects.create(video_id='Mefr3Ftg',viewCount='35467',likeCount='2467',favoriteCount='8765',commentCount='87675',tags='2022,bangla,bangla song,viral')
        self.video_perf = YTperf.objects.create(vid=self.video_stat,performance='0.89876')

    def test_video_list(self):
        response = self.client.get("/api/list-of-videos/")
        self.assertEqual(response.status_code, 200)
    
    def test_video_list_reverse(self):
        response = self.client.get(reverse("list-of-videos"))
        self.assertEqual(response.status_code, 200)



class SearchViewTestCase(APITestCase):

    def setUp(self):
        self.video_stat = YTstats.objects.create(video_id='Mefr3Ftg',viewCount='35467',likeCount='2467',favoriteCount='8765',commentCount='87675',tags='2022,bangla,bangla song,viral')
        self.video_perf = YTperf.objects.create(vid=self.video_stat,performance='0.89876')

    def test_search_No_content(self):
        data={'q':'Bermuda','f':''}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 204)

    def test_search_No_content_incomplete_keywords(self):
        data={'q':'B','f':''}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 204)

    def test_only_query(self):
        data={'q':'2022','f':''}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 200 )

    def test_query_with_asc(self):
        data={'q':'2022','f':'ASC'}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 200 )

    def test_query_with_desc(self):
        data={'q':'2022','f':'DESC'}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 200 )

    def test_only_asc_order(self):
        data={'q':'','f':'ASC'}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 200 )

    def test_only_desc_order(self):
        data={'q':'','f':'DESC'}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 200 )

    def test_both_param_empty(self):
        data={'q':'','f':''}
        response = self.client.get("/api/search/",data)
        self.assertEqual(response.status_code, 200)
