from django.db import models
from django.utils.translation import ugettext_lazy as _

"""
Model Creation
"""

class YTstats(models.Model):
    """
    YouTube Statistics Model Creation 
    """

    video_id = models.CharField(_('Video ID'), max_length=255, null=True, blank=True)
    viewCount = models.CharField(_('View Count'), max_length=255, null=True, blank=True)
    likeCount = models.CharField(_('Like Count'), max_length=255, null=True, blank=True)
    favoriteCount = models.CharField(_('Favorite Count'), max_length=255, null=True, blank=True)
    commentCount = models.CharField(_('Comment Count'), max_length=255, null=True, blank=True)
    tags = models.TextField(_('Tags'), null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return self.video_id

class YTperf(models.Model):
    """
    YouTube Video Performance Model
    """

    vid = models.OneToOneField(
        YTstats,
        on_delete=models.CASCADE
    )
    performance = models.CharField(_('Performance'), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return self.vid.video_id
