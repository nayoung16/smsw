from django.urls import path
from .views import DeleteVolunteer, Search, UploadFeed, Profile, Community, UploadReply, ToggleLike, ToggleBookmark, DeleteFeed, createVolunteerITem

app_name = 'content'

urlpatterns = [
    # path('main', Main.as_view(), name="community"),
    path('community', Community.as_view(), name="community"),
    path('profile', Profile.as_view(), name="profile"),
    path('search', Search.as_view(), name="search"),
    path('search_result', Search.as_view(), name="search_result"),

    path('createvolunteer', createVolunteerITem.as_view(), name="create_volunteer"),
    path('deletevolunteer', DeleteVolunteer.as_view()),

    path('delete_feed', DeleteFeed.as_view()),
    path('upload_feed', UploadFeed.as_view()),
    path('reply_feed', UploadReply.as_view()),
    path('like_feed', ToggleLike.as_view()),



    path('bookmark_volunteer', ToggleBookmark.as_view()),
]

