from rest_framework import serializers
from core.models import *

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = YTstats
        fields = ('id','video_id','viewCount','likeCount','favoriteCount','commentCount','tags')

class PerfSerializer(serializers.ModelSerializer):

    vid = StatSerializer()

    class Meta:
        model = YTperf
        fields = ('vid', 'performance')