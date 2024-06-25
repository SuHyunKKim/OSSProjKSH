# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

# Create your models here.
#class 모델 클래스를 설정하면 데이터베이스에 테이블이 생성된다.





#AppUser 모델 정의
class AppUser(models.Model):
    userID = models.AutoField(primary_key=True)
    iD = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    name = models.CharField(max_length=45, default='')
    studentID = models.CharField(max_length=45, default='')
    gender = models.CharField(max_length=45, default='')

    isProfile = models.BooleanField(default=False)  # 사용자 정보 입력 여부
    isUserPref = models.BooleanField(default=False)  # 선호도 정보 입력 여부
    isRestricted = models.BooleanField(default=False)  # 플랫폼 차단 여부 추가 (False: 차단 안됨, True: 차단됨)
    matchStatus = models.CharField(max_length=45, default='pending')

    def __str__(self):
        return self.iD



# KSH : 채팅방 모델 정의
class ChatRoom(models.Model): #ChatHistory 역할
    HistoryID = models.AutoField(primary_key = True) # 채팅방 ID 번호
    userID = models.ForeignKey(AppUser, related_name='chatroom_user', on_delete=models.CASCADE)
    # User - 매치 결과의 유저로 수정 필요
    userID2 = models.ForeignKey(AppUser, related_name='chatroom_user2', on_delete=models.CASCADE)
    # userID2name = models.CharField(max_length = 45, default = '')
    # AccessedTime = models.DateTimeField(auto_now_add=True) # 채팅방 메세지 시간

    def __str__(self):
        return f"ChatRoom {self.HistoryID}"

# KSH : 채팅 모델 정의
class Chat(models.Model): #Message 역할
    messageID = models.AutoField(primary_key = True)
    CHistoryID = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chats', default = -1)

    senderID = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='senders')
    receiverID = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='receivers')

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Chat {self.id} in {self.chatroom.id}"



# KSH: Profile 모델 정의 추가
class Profile(models.Model):
    profileId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='profiles')
    Embti = models.IntegerField(default=0)
    Smbti = models.IntegerField(default=0)
    Tmbti = models.IntegerField(default=0)
    Jmbti = models.IntegerField(default=0)

    firstLesson = models.IntegerField()
    smoke = models.IntegerField()
    sleepHabit = models.IntegerField()
    grade = models.IntegerField()
    shareNeeds = models.IntegerField()
    inComm = models.IntegerField()
    heatSens = models.IntegerField()
    coldSens = models.IntegerField()
    drinkFreq = models.IntegerField()
    cleanliness = models.IntegerField()
    noiseSens = models.IntegerField()
    sleepSche = models.IntegerField()
    upSche = models.IntegerField()

    def __str__(self):
        return self.userId

# KSH: UserPref 모델 정의 추가
class UserPref(models.Model):
    prefId = models.AutoField(primary_key=True)
    UuserId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='userprefs')
    UEmbti = models.IntegerField(default=0)
    USmbti = models.IntegerField(default=0)
    UTmbti = models.IntegerField(default=0)
    UJmbti = models.IntegerField(default=0)

    UfirstLesson = models.IntegerField()
    Usmoke = models.IntegerField()
    UsleepHabit = models.IntegerField()
    Ugrade = models.IntegerField()
    UshareNeeds = models.IntegerField()
    UinComm = models.IntegerField()
    UheatSens = models.IntegerField()
    UcoldSens = models.IntegerField()
    UdrinkFreq = models.IntegerField()
    Ucleanliness = models.IntegerField()
    UnoiseSens = models.IntegerField()
    UsleepSche = models.IntegerField()
    UupSche = models.IntegerField()

    def __str__(self):
        return self.UserId

# KSH: Matching 모델 정의 추가
class Match(models.Model):
    matchId = models.AutoField(primary_key = True)
    userId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='matchings')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    # related_name 참조 변경 필요
    userId1 = models.IntegerField()
    userId2 = models.IntegerField()
    userId3 = models.IntegerField()
    userId4 = models.IntegerField()
    userId5 = models.IntegerField()

    def __str__(self):
        return self.matchId



# KSH: Report 모델 정의 추가
class Report(models.Model):
    reportId = models.AutoField(primary_key = True)
    reporterId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Chat 모델에서 포린키 가져와야함 수정 필요
    reportedId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='reporters')


    def __str__(self):
        return self.reportId


# KSH: Block 모델 정의 추가
class Block (models.Model):
    blockId = models.AutoField(primary_key = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    blockerId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='blocks')
    # Chat 모델에서 포린키 가져와야함 수정 필요
    blockedId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='blockers')







    # userId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='blocks')
    # timestamp = models.DateTimeField(default = timezone.now)
    # blockerId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='blockers')
    # # Chat 모델에서 포린키 가져와야함 수정 필요
    # blockedId = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='blockers')

    def __str__(self):
        return self.blockedId
