from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from Jinstagram import settings


# Create your models here.
class User(AbstractBaseUser):
    """
        유저 프로파일 사진
        유저 닉네임     -> 화면에 표기되는 이름
        유저 이름       -> 실제 사용자 이름
        유저 이메일주소 -> 회원가입할때 사용하는 아이디
        유저 비밀번호 -> 디폴트 쓰자
    """
    RANKING_SEED = '1'
    RANKING_SPROUT = '2'
    RANKING_SEEDLING = '3'
    RANKING_TREE = '4'
    RANKING_FLOWER = '5'
    RANKING_CHOICES = [
        (RANKING_SEED, 'Seed'),
        (RANKING_SPROUT, 'Sprout'),
        (RANKING_SEEDLING, 'Seedling'),
        (RANKING_TREE, 'Tree'),
        (RANKING_FLOWER, 'Flower'),
    ]

    ROLE_ADMIN = 'A'
    ROLE_USER = 'U'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User')
    ]
    role = models.CharField(max_length=1, choices = ROLE_CHOICES, default = ROLE_USER)
    ranking = models.CharField(max_length=1, choices = RANKING_CHOICES, default = RANKING_SEED)
    profile_image = models.TextField()  # 프로필 이미지
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    sum_time = models.IntegerField(default = 0)
    residence = models.CharField(max_length = 200, default = '')
    lat = models.DecimalField(max_digits = 10,decimal_places= 6, default=0)
    lng = models.DecimalField(max_digits = 10,decimal_places= 6, default=0)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followings')
    # https://han-py.tistory.com/161 팔로우 기능 구현

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = "User"
