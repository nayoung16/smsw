from uuid import uuid4
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark, VolunteerItem
from user.models import User
import os
from Jinstagram.settings import MEDIA_ROOT
from django.db.models import Q
from content.models import VolunteerItem


class Community(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        mainuser = User.objects.filter(email=email).first()

        if mainuser is None:
            return render(request, "user/login.html")

        feed_object_list = Feed.objects.all().order_by('-id')  # select  * from content_feed;
        feed_list = []

        volunteer_object_list = VolunteerItem.objects.all().order_by('-id')
        volunteer_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,nickname=user.nickname))
            like_count=Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked=Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked=Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(id=feed.id,
                                image=feed.image,
                                content=feed.content,
                                like_count=like_count,
                                profile_image=user.profile_image,
                                nickname=user.nickname,
                                reply_list=reply_list,
                                is_liked=is_liked,
                                is_marked=is_marked
                                ))

        for volunteer in volunteer_object_list:
            volunteer_list.append(dict(id=volunteer.id,
                                image=volunteer.volunteer_image,
                                region=volunteer.region,
                                participant=volunteer.participant,
                                ))



        return render(request, "content/community.html", context=dict(feeds=feed_list, 
                                                                    volunteers = volunteer_list,
                                                                    mainuser=mainuser))


class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        asdf = uuid_name
        content123 = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(image=asdf, content=content123, email=email)

        return Response(status=200)

class DeleteFeed(APIView):
    def delete(self, request):
        feed_id = request.data.get('feed_id', None)
        feed = Feed.objects.filter(id=feed_id).first()
        feed.delete()
        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list,
                                                                    user=user))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        print(bookmark_text)
        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)

class Search(APIView):
    volunteer_list = VolunteerItem.objects.order_by('id')

    def get(self, request):
        global volunteer_list
        print(volunteer_list)
        email = request.session.get('email', None)
        mainuser = User.objects.filter(email=email).first()
        print("get")
        return render(request, "content/search.html", context=dict(mainuser=mainuser,
                                                                    volunteer_list=volunteer_list))

    def post(self, request):
        global volunteer_list
        volunteer_list = VolunteerItem.objects.order_by('id')
        search_item = request.data.get('search_item', None)  # 검색어
        volunteer_list = volunteer_list.filter(
            description__contains=search_item
        ).distinct()
        print(volunteer_list)
        print("post")
        return render(request, 'content/search.html', context=dict(volunteer_list=volunteer_list))
    



class createVolunteerITem(APIView):
    def get(self, request):
        email = request.session.get('email', None)
        mainuser = User.objects.filter(email=email).first()
        return render(request, "content/createVolunteerItem.html", context=dict( mainuser=mainuser))

    def post(self, request):
        email = request.session.get('email', None)
        mainuser = User.objects.filter(email=email).first()
        # 일단 파일 불러

        file = request.data.get('file_give', None)
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination: 
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        region = request.data.get('region', None)
        participant = request.data.get('participant', None)
        description = request.data.get('description', None)
        date = request.data.get('date', None)
        start_time = request.data.get('start_time', None)
        end_time = request.data.get('end_time', None)
        latlng = request.data.get('latlag', None)

        print(tuple(latlng)[0])

        VolunteerItem.objects.create(
                            admin = mainuser,
                            volunteer_image=image, 
                            region = region,
                            participant = participant,
                            description = description,
                            date = date,
                            start_time = start_time,
                            end_time = end_time)

        return Response(status=200)

class DeleteVolunteer(APIView):
    def delete(self, request):
        volunteer_id = request.data.get('volunteer_id', None)
        volunteeritem = VolunteerItem.objects.filter(id=volunteer_id).first()
        volunteeritem.delete()
        return Response(status=200)

class Main(APIView):
    def get(self, request):
        return render(request, "content/main.html")