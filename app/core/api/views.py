from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
app_time_zone = 'Asia/Omsk'
from .serializers import *
from core.models import *
from collections import OrderedDict
from django.contrib.postgres.search import (SearchVector, SearchQuery)


class CustomPageNumber(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('count', self.page.paginator.count),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('results', data)
         ]),status=status.HTTP_200_OK)



class VideoList(APIView,CustomPageNumber):
    """Available Video List API.

    Args:
        APIView ([class]): inherits default APIView of Django REST Framework(DRF)
    """

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        """Getting Available Video list data. Authentication does not require.

        Args:
            request ([GET]): http://127.0.0.1:8000/api/list-of-videos/

        Returns:
            [json]: Multiple dictionary object in a list.
            {
                "count": 41,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "vid": {
                            "id": 83,
                            "video_id": "MeyPwC9Pt_s",
                            "viewCount": "470969",
                            "likeCount": "25368",
                            "favoriteCount": "0",
                            "commentCount": "1205",
                            "tags": "bangla song, bangla Hot song 2021, bangla song new, bangla song new 2022, Bangla New Music Video 2021, bangla new song, Bangla new song 2021, tik tok viral song, Bangla SONG, Adib, autanu, Official Music Video, bangla new song 2021, bengali song, latest songs, latest Bangla songs, latest Bengali songs, 2021, Top Hits of Autanu vines, trending, rap song, New Song autanu vines 2021, New Song 2021, Boom, Dance Music, Electronic, NUR NOBI all song, tik tok, BOMB, bomb"
                        },
                        "performance": "0.5455860802678297"
                    },
                    ...
                ]
            }
        """
        try:
            video_list = YTperf.objects.all().order_by('id')
            page = self.paginate_queryset(video_list,request)
            serializer = PerfSerializer(page, many=True)
            
            if (serializer.data):
                return self.get_paginated_response(serializer.data)
            else:
                res = {
                        "error" : "Data Not Found"
                    }
                return Response(res, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            res = {
                "error" : e.args[0]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class SearchView(APIView,CustomPageNumber):
    """Search Video API. Tags and Performance

    Args:
        APIView ([class]): inherits default APIView of Django REST Framework(DRF)
    """

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        """Getting Video data by Tags and Performance. Authentication does not require.

        Args:
            request ([GET]): http://127.0.0.1:8000/api/search/?q=2022&f=ASC
            or 
            http://127.0.0.1:8000/api/search/
            query params : 
                q : 2022,
                f : ASC

        Returns:
            [json]: Multiple dictionary object in a list.
            {
                "results": [
                    {
                    "vid": {
                        "id": 84,
                        "video_id": "WCad_qNRjGg",
                        "viewCount": "55242",
                        "likeCount": "2691",
                        "favoriteCount": "0",
                        "commentCount": "169",
                        "tags": "latest songs, latest Bangla songs, latest Bengali songs, 2021, Top Hits of Autanu vines, trending, rap song, New Song autanu vines 2021, New Song 2021, Boom Boom, Boom, BOOM BOOM BOOM, Dance Music, Electronic, kacha badam song, কাঁচা বাদাম, NUR NOBI all song, tik tok, tik tok viral song, bangla song, bangla Hot song 2021, bangla song new, bangla song new 2022, Bangla New Music Video 2021, bangla new song, Bangla new song 2021, Bangla SONG, Adib, autanu, Official Music Video"
                        },
                        "performance": "0.06399416149715895"
                    }, 
                    ...
                ]
            }
        """
        try:
            q=request.GET['q']
            f = request.GET['f']
            if q and f=='':
                vector = SearchVector('vid__tags')
                video = YTperf.objects.annotate(search=vector).filter(search=SearchQuery(q))
            elif q and f=='ASC':
                vector = SearchVector('vid__tags')
                video = YTperf.objects.annotate(search=vector).filter(search=SearchQuery(q)).order_by('performance')
            elif q and f=='DESC':
                vector = SearchVector('vid__tags')
                video = YTperf.objects.annotate(search=vector).filter(search=SearchQuery(q)).order_by('-performance')
            elif q=='' and f=='ASC':
                video = YTperf.objects.all().order_by('performance')
            elif q=='' and f=='DESC':
                video = YTperf.objects.all().order_by('-performance')
            else:
                video = YTperf.objects.all()


            page = self.paginate_queryset(video,request)
            serializer = PerfSerializer(page, many=True)
            
            if(serializer.data):
                return Response(OrderedDict([('results', serializer.data)]),status=status.HTTP_200_OK)
            else:
                res = {
                        "error" : "Data Not Found"
                    }
                return Response(res, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            res = {
                "error" : e.args[0]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
