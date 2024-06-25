from rest_framework import serializers
from .models import AppUser, ChatRoom, Chat, Profile, UserPref, Match, Report, Block

from django.db import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ("__all__")

class ChatSerializer(serializers.ModelSerializer):
    CHistoryID = serializers.CharField()
    senderID = serializers.CharField()
    receiverID = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        model = Chat
        fields = ['CHistoryID', 'senderID', 'receiverID', 'content']

class ChatRoomSerializer(serializers.ModelSerializer):
    HistoryID = serializers.CharField()
    userID = serializers.CharField()
    userID2 = serializers.CharField()

    class Meta:
        model = ChatRoom
        fields = ("__all__")


# KSH: ProfileSerializer 추가
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("__all__")

# KSH: UserPrefSerializer 추가
class UPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPref
        fields = ("__all__")

# KSH: MatchSerializer 추가
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ("__all__")

# KSH: RoomSerializer 추가
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("__all__")

# KSH: BlockSerializer 추가
class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("__all__")