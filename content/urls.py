from django.urls import path
from .views import DeleteVolunteer, SearchResult, UploadFeed, Profile,\
    Community, UploadReply, ToggleLike, ToggleBookmark, DeleteFeed, createVolunteerITem, \
        Main, Search, Follow, Participate, NotParticipate, detail
from . import views


app_name = 'content'

urlpatterns = [
    path('', Main.as_view(), name="main"),
    path('community', Community.as_view(), name="community"),
    path('profile', Profile.as_view(), name="profile"),
    path('search', Search.as_view(), name="search"),
    path('search_result',  SearchResultResult.as_view(), name="search_result"),

    path('createvolunteer', createVolunteerITem.as_view(), name="create_volunteer"),
    path('deletevolunteer', DeleteVolunteer.as_view()),

    path('delete_feed', DeleteFeed.as_view()),
    path('upload_feed', UploadFeed.as_view()),
    path('reply_feed', UploadReply.as_view()),
    path('like_feed', ToggleLike.as_view()),
    path('feed_detail/<int:feed_id>', detail),

    path('test', Follow.as_view(), name="test"),

    path('bookmark_volunteer', ToggleBookmark.as_view()),
    path('participate_volunteer', Participate.as_view()),
    path('not_participate_volunteer', NotParticipate.as_view()),
]

