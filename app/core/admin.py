from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(YTstats)
class StatsAdmin(ImportExportModelAdmin):
    list_display = ['video_id','viewCount','likeCount','favoriteCount','commentCount','tags']

@admin.register(YTperf)
class PerfAdmin(ImportExportModelAdmin):
    list_display = ['vid', 'performance']