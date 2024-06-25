from django.shortcuts import render, redirect
# Create your views here.
from rest_framework import viewsets
from .serializers import UserSerializer, ChatRoomSerializer, ChatSerializer
# 시리얼라이저 profile, userpref, match, report, block 추가
from .serializers import ProfileSerializer, UPrefSerializer, MatchSerializer, ReportSerializer, BlockSerializer
from .models import AppUser, ChatRoom, Chat
# 모델 profile, userpref, match, report, block 추가
from .models import Profile, UserPref, Match, Report, Block
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import action

from django.http.response import HttpResponse
from rest_framework.response import Response
from django.utils import timezone
from django.contrib import auth

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.sessions.models import Session
import numpy as np,random

from scipy.spatial.distance import euclidean
from sklearn.metrics import jaccard_score
from .models import AppUser, Match, Profile, UserPref

import logging
logger = logging.getLogger(__name__)


from django.db.models import Q

# from django.contrib.auth import authenticate


class UserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

    #회원가입 시 호출되는 함수
    @api_view(['POST'])
    def signup(request):
        iD = request.data.get('iD')
        password = request.data.get('password')
        name = request.data.get('name')
        studentID = request.data.get('studentID')
        gender = request.data.get('gender')

        # studentid, gender 추가
        if iD and password and name and studentID and gender:
            try:
                # 회원 정보가 존재하는지 체크
                existing_user = AppUser.objects.get(iD=iD)
                return Response({'success': 'False'}, status=status.HTTP_400_BAD_REQUEST)
            except AppUser.DoesNotExist:
                # 회원 새로 생성
                user_count = AppUser.objects.count() + 1
                user = AppUser.objects.create(
                    userID=user_count, iD=iD, password=password, name=name, studentID=studentID, gender=gender
                )
                user.save()
                return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': 'False'}, status=status.HTTP_400_BAD_REQUEST)


    #로그인 시 호출되는 함수
    @api_view(['POST'])
    def login_api(request):
        iD = request.data.get('iD')
        password = request.data.get('password')

        if iD and password:
            try:
                # 로그인 성공
                existing_user = AppUser.objects.get(iD=iD, password=password)
                user_id = existing_user.iD
                request.session['user_id'] = user_id
                user_id1=request.session.get('user_id')
                print(user_id1)
                return Response({'success': True, 'user_id': user_id}, status=status.HTTP_200_OK)
            except AppUser.DoesNotExist:
                #로그인 실패
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def get_user_id(request):
        # 세션에서 사용자 ID 가져오기
        user_id = request.session.get('user_id')
        print(user_id)
        if user_id:
            return Response({'user_id': user_id}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)


    # KSH : 로그아웃 기능 구현 예정
    @api_view(['POST'])
    def logout(request):
        request.session.flush()
        return Response({'success': True}, status=status.HTTP_200_OK)




# 채팅방 생성
class ChatRoomListViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    @api_view(['POST'])
    def chatroomcreate(request):
        logger.warning(f"Received data: {request.data}")

        userID = request.data.get('userID')
        userID2 = request.data.get('userID2')

        try:
            user1 = AppUser.objects.get(iD=userID)
            user2 = AppUser.objects.get(userID=userID2)
        except AppUser.DoesNotExist:
            return Response({'success': False, 'error': 'One or both users do not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chatroom = ChatRoom.objects.get(
                Q(userID=user1, userID2=user2) | Q(userID=user2, userID2=user1)
            )
            serialized_chatroom = ChatRoomSerializer(chatroom)
            return Response({'success': True, 'chatRoom': serialized_chatroom.data}, status=status.HTTP_200_OK)

        except ChatRoom.DoesNotExist:
            room_count = ChatRoom.objects.count() + 1
            chatroom = ChatRoom.objects.create(
                HistoryID=room_count,
                userID=user1,
                userID2=user2
            )
            chatroom.save()
            serialized_chatroom = ChatRoomSerializer(chatroom)
            return Response({'success': True, 'chatRoom': serialized_chatroom.data}, status=status.HTTP_201_CREATED)

    @api_view(['GET'])
    def getchathistory(request):
        userID = request.query_params.get('userID')
        userID2 = request.query_params.get('userID2')

        if not userID or not userID2:
            return Response({"error": "Missing userID or userID2 parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user1 = AppUser.objects.get(iD=userID)
            user2 = AppUser.objects.get(userID=userID2)
        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        chats = Chat.objects.filter(
            Q(senderID=user1, receiverID=user2) | Q(senderID=user2, receiverID=user1)
        ).order_by('timestamp')

        serialized_chats = ChatSerializer(chats, many=True).data
        print(serialized_chats)
        return Response({"chatMessages": serialized_chats}, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def chatroomlist(request):
        userID = request.data.get('userID')
        userID = AppUser.objects.get(iD = userID)

        chatroom_list = ChatRoom.objects.filter(iD=userID)

        serializer = ChatRoomSerializer(chatroom_list, many=True)

        return Response(serializer.data)



class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @api_view(['POST'])
    def savemessage(request):
        CHistoryID = request.data.get('CHistoryID')
        senderID = request.data.get('senderID')

        try:
            chatroom = ChatRoom.objects.get(senderID=senderID)
            receiverID = chatroom.userID2
        except ChatRoom.DoesNotExist:
            return Response({'success': False, 'error': 'ChatRoom not found'}, status=status.HTTP_400_BAD_REQUEST)

        content = request.data.get('content')
        timestamp = request.data.get('timestamp')

        if CHistoryID and senderID and receiverID and content and timestamp:
            chat_count = Chat.objects.count() + 1
            chat = Chat.objects.create(messageID = chat_count, CHistoryID = CHistoryID,
                                       senderID = senderID, receiverID = receiverID,
                                       content = content, timestamp = timestamp)
            chat.save()

            chatroom = ChatRoom.objects.filter(HistoryID = CHistoryID)
            chatroom.update(AccessedTime=timestamp, recentMessage=content)
            chatroom.save()

            return_chat = Chat.objects.filter(timestamp = timestamp)

            # 새로운 메세지 저장시, 채팅방의 AccessedTime과 recentMessage도 업데이트
            # 새로운 메세지 자체도 반환
            return Response({'success': True, 'chat': ChatSerializer(return_chat, many=True).data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)




# KSH : ProfileViewSet 추가
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # KSH : 사용자 정보 생성 기능
    @api_view(['POST'])
    def profilecreate(request):
        logger.debug(f"Received data: {request.data}")

        userId = request.data.get('userId')
        userId = AppUser.objects.get(iD = userId)
        #userId = userId.iD

        Embti = request.data.get('Embti')
        Smbti = request.data.get('Smbti')
        Tmbti = request.data.get('Tmbti')
        Jmbti = request.data.get('Jmbti')

        firstLesson = request.data.get('firstLesson')
        smoke = request.data.get('smoke')
        sleepHabit = request.data.get('sleepHabit')
        grade = request.data.get('grade')
        shareNeeds = request.data.get('shareNeeds')
        inComm = request.data.get('inComm')
        heatSens = request.data.get('heatSens')
        coldSens = request.data.get('coldSens')
        drinkFreq = request.data.get('drinkFreq')
        cleanliness = request.data.get('cleanliness')
        noiseSens = request.data.get('noiseSens')
        sleepSche = request.data.get('sleepSche')
        upSche = request.data.get('upSche')

        required_fields = [userId, Embti, Smbti, Tmbti, Jmbti, firstLesson, smoke, sleepHabit,
                             grade, shareNeeds, inComm, heatSens, coldSens, drinkFreq,
                            cleanliness, noiseSens, sleepSche, upSche]


        if all(field is not None for field in required_fields):
            user_count = Profile.objects.count() + 1
            user_profile = Profile.objects.create(profileId = user_count, userId = userId,
                                                  Embti = Embti,
                                                  Smbti = Smbti,
                                                  Tmbti = Tmbti,
                                                  Jmbti = Jmbti,
                                                  firstLesson = firstLesson,
                                                  smoke = smoke,
                                                  sleepHabit = sleepHabit,
                                                  grade = grade,
                                                  shareNeeds = shareNeeds,
                                                  inComm = inComm,
                                                  heatSens = heatSens,
                                                  coldSens = coldSens,
                                                  drinkFreq = drinkFreq,
                                                  cleanliness = cleanliness,
                                                  noiseSens = noiseSens,
                                                  sleepSche = sleepSche,
                                                  upSche = upSche)
            user_profile.save()

            user = AppUser.objects.get(iD = userId)
            user.isProfile = True
            user.save()

            return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    # KSH : 사용자 정보 수정 기능
    @api_view(['PATCH'])
    def profileupdate(request):
        userId = request.data.get('userId')

        Embti = request.data.get('Embti')
        Smbti = request.data.get('Smbti')
        Tmbti = request.data.get('Tmbti')
        Jmbti = request.data.get('Jmbti')

        firstLesson = request.data.get('firstLesson')
        smoke = request.data.get('smoke')
        sleepHabit = request.data.get('sleepHabit')
        grade = request.data.get('grade')
        shareNeeds = request.data.get('shareNeeds')
        inComm = request.data.get('inComm')
        heatSens = request.data.get('heatSens')
        coldSens = request.data.get('coldSens')
        drinkFreq = request.data.get('drinkFreq')
        cleanliness = request.data.get('cleanliness')
        noiseSens = request.data.get('noiseSens')
        sleepSche = request.data.get('sleepSche')
        upSche = request.data.get('upSche')

        if (userId and Embti and Smbti and Tmbti and Jmbti and firstLesson and smoke and sleepHabit
                and grade and shareNeeds and inComm and heatSens and coldSens and drinkFreq
                and cleanliness and noiseSens and sleepSche and upSche):

            user_profile = Profile.objects.get(userId = userId)
            user_profile.Embti = Embti
            user_profile.Smbti = Smbti
            user_profile.Tmbti = Tmbti
            user_profile.Jmbti = Jmbti
            user_profile.firstLesson = firstLesson
            user_profile.smoke = smoke
            user_profile.sleepHabit = sleepHabit
            user_profile.grade = grade
            user_profile.shareNeeds = shareNeeds
            user_profile.inComm = inComm
            user_profile.heatSens = heatSens
            user_profile.coldSens = coldSens
            user_profile.drinkFreq = drinkFreq
            user_profile.cleanliness = cleanliness
            user_profile.noiseSens = noiseSens
            user_profile.sleepSche = sleepSche
            user_profile.upSche = upSche
            user_profile.save()

            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

# KSH : UserPrefViewSet 추가
class UserPrefViewSet(viewsets.ModelViewSet):
    queryset = UserPref.objects.all()
    serializer_class = UPrefSerializer

    # KSH : 사용자 선호도 정보 생성 기능
    @api_view(['POST'])
    def userprefcreate(request):
        logger.debug(f"Received data: {request.data}")

        UuserId = request.data.get('UuserId')
        UuserId = AppUser.objects.get(iD = UuserId)


        UEmbti = request.data.get('UEmbti')
        # USmbti = request.data.get('USmbti')
        # UTmbti = request.data.get('UTmbti')
        # UJmbti = request.data.get('UJmbti')

        UfirstLesson = request.data.get('UfirstLesson')
        Usmoke = request.data.get('Usmoke')
        UsleepHabit = request.data.get('UsleepHabit')
        Ugrade = request.data.get('Ugrade')
        UshareNeeds = request.data.get('UshareNeeds')
        UinComm = request.data.get('UinComm')
        UheatSens = request.data.get('UheatSens')
        UcoldSens = request.data.get('UcoldSens')
        UdrinkFreq = request.data.get('UdrinkFreq')
        Ucleanliness = request.data.get('Ucleanliness')
        UnoiseSens = request.data.get('UnoiseSens')
        UsleepSche = request.data.get('UsleepSche')
        UupSche = request.data.get('UupSche')

        required_fields = [UuserId, UEmbti, UfirstLesson, Usmoke, UsleepHabit,
                           Ugrade, UshareNeeds, UinComm, UheatSens, UcoldSens,
                           UdrinkFreq, Ucleanliness, UnoiseSens, UsleepSche, UupSche]

        if all(field is not None for field in required_fields):

            if UserPref.objects.filter(UuserId = UuserId).exists():
                user_pref = UserPref.objects.get(UuserId = UuserId)
                user_pref.UEmbti = UEmbti
                # user_pref.USmbti = USmbti
                # user_pref.UTmbti = UTmbti
                # user_pref.UJmbti = UJmbti

                user_pref.UfirstLesson = UfirstLesson
                user_pref.Usmoke = Usmoke
                user_pref.UsleepHabit = UsleepHabit
                user_pref.Ugrade = Ugrade
                user_pref.UshareNeeds = UshareNeeds
                user_pref.UinComm = UinComm
                user_pref.UheatSens = UheatSens
                user_pref.UcoldSens = UcoldSens
                user_pref.UdrinkFreq = UdrinkFreq
                user_pref.Ucleanliness = Ucleanliness
                user_pref.UnoiseSens = UnoiseSens
                user_pref.UsleepSche = UsleepSche
                user_pref.UupSche = UupSche

                user_pref.save()

                return Response({'success': True}, status=status.HTTP_200_OK)

            else:
                user_count = UserPref.objects.count() + 1
                user_pref = UserPref.objects.create(prefId = user_count, UuserId = UuserId,
                                                    UEmbti = UEmbti,
                                                    UfirstLesson = UfirstLesson,
                                                    Usmoke = Usmoke,
                                                    UsleepHabit = UsleepHabit,
                                                    Ugrade = Ugrade,
                                                    UshareNeeds = UshareNeeds,
                                                    UinComm = UinComm,
                                                    UheatSens = UheatSens,
                                                    UcoldSens = UcoldSens,
                                                    UdrinkFreq = UdrinkFreq,
                                                    Ucleanliness = Ucleanliness,
                                                    UnoiseSens = UnoiseSens,
                                                    UsleepSche = UsleepSche,
                                                    UupSche = UupSche)
                user_pref.save()

                user = AppUser.objects.get(iD = UuserId)
                user.isUserPref = True
                user.save()

                return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
    # KSH : 사용자 선호도 정보 수정 기능
    @api_view(['PATCH'])
    def userprefupdate(request):
        UuserId = request.data.get('UuserId')

        UEmbti = request.data.get('UEmbti')
        # USmbti = request.data.get('USmbti')
        # UTmbti = request.data.get('UTmbti')
        # UJmbti = request.data.get('UJmbti')

        UfirstLesson = request.data.get('UfirstLesson')
        Usmoke = request.data.get('Usmoke')
        UsleepHabit = request.data.get('UsleepHabit')
        Ugrade = request.data.get('Ugrade')
        UshareNeeds = request.data.get('UshareNeeds')
        UinComm = request.data.get('UinComm')
        UheatSens = request.data.get('UheatSens')
        UcoldSens = request.data.get('UcoldSens')
        UdrinkFreq = request.data.get('UdrinkFreq')
        Ucleanliness = request.data.get('Ucleanliness')
        UnoiseSens = request.data.get('UnoiseSens')
        UsleepSche = request.data.get('UsleepSche')
        UupSche = request.data.get('UupSche')


        required_fields = [UuserId, UEmbti, UfirstLesson, Usmoke, UsleepHabit,
                   Ugrade, UshareNeeds, UinComm, UheatSens, UcoldSens,
                   UdrinkFreq, Ucleanliness, UnoiseSens, UsleepSche, UupSche]

        if all(field is not None for field in required_fields):

            user_pref = UserPref.objects.get(UuserId = UuserId)
            user_pref.UEmbti = UEmbti
            # user_pref.USmbti = USmbti
            # user_pref.UTmbti = UTmbti
            # user_pref.UJmbti = UJmbti

            user_pref.UfirstLesson = UfirstLesson
            user_pref.Usmoke = Usmoke
            user_pref.UsleepHabit = UsleepHabit
            user_pref.Ugrade = Ugrade
            user_pref.UshareNeeds = UshareNeeds
            user_pref.UinComm = UinComm
            user_pref.UheatSens = UheatSens
            user_pref.UcoldSens = UcoldSens
            user_pref.UdrinkFreq = UdrinkFreq
            user_pref.Ucleanliness = Ucleanliness
            user_pref.UnoiseSens = UnoiseSens
            user_pref.UsleepSche = UsleepSche
            user_pref.UupSche = UupSche

            user_pref.save()

            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)




# KSH :  MatchViewSet 추가
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    
    # KSH : 매칭+매칭결과 저장 알고리즘
    @api_view(['POST'])
    def matching(request):
        # 사용자 iD임
        userId = request.data.get('userId')

        # 사용자 iD로 사용자 객체 가져옴
        user = AppUser.objects.get(iD=userId)
        userId = user.userID
        # 사용자 선호도 객체 가져옴
        user_pref = UserPref.objects.get(UuserId=user.userID)

        # 조건에 맞는 사용자 리스트 가져옴
        user_list = AppUser.objects.exclude(userID=userId).filter(
            gender=user.gender,
            matchStatus='pending',
            isProfile=True,
            isUserPref=True,
            isRestricted=False
        )

        print(user_list)

        # OYJ : 매칭 알고리즘 추가
        # 이진 필드와 연속 필드를 정의
        binary_fields = ['Embti', 'firstLesson', 'smoke', 'sleepHabit', 'shareNeeds', 'inComm', 'heatSens', 'coldSens']
        continuous_fields = ['grade', 'drinkFreq', 'cleanliness', 'noiseSens', 'sleepSche', 'upSche',]

        Ubinary_fields = ['UEmbti', 'UfirstLesson', 'Usmoke', 'UsleepHabit', 'UshareNeeds', 'UinComm', 'UheatSens', 'UcoldSens']
        Ucontinuous_fields = ['Ugrade', 'UdrinkFreq', 'Ucleanliness', 'UnoiseSens', 'UsleepSche', 'UupSche']


        # 자카드 유사도를 계산하는 함수
        def calculate_jaccard_similarity(user_pref, profile, Ubinary_fields, binary_fields):
            user_pref_data = [getattr(user_pref, field) for field in Ubinary_fields]  # user_pref 객체의 binary_fields 필드 값을 가져옴
            profile_data = [getattr(profile, field) for field in binary_fields]  # profile 객체의 binary_fields 필드 값을 가져옴
            return jaccard_score(user_pref_data, profile_data, average='weighted')  # average 파라미터를 추가


        # 유클리드 유사도를 계산하는 함수
        def calculate_euclidean_similarity(user_pref, profile, Ucontinuous_fields, continuous_fields):
            user_pref_data = [getattr(user_pref, field) for field in Ucontinuous_fields]  # user_pref 객체의 continuous_fields 필드 값을 가져옴
            profile_data = [getattr(profile, field) for field in continuous_fields]  # profile 객체의 continuous_fields 필드 값을 가져옴
            return euclidean(user_pref_data, profile_data)

        # 사용자 매칭을 수행하는 함수
        def match_users(user_pref, potential_matches, Ubinary_fields, Ucontinuous_fields,
                        binary_fields, continuous_fields, weight_binary=0.5, weight_continuous=0.5):
            similarities = []  # 유사도 저장을 위한 리스트 초기화
            for match in potential_matches:  # 각 잠재적 매칭 사용자에 대해 반복
                match_profile = Profile.objects.get(userId=match.userID)  # 잠재적 매칭 사용자의 프로필을 가져옴

                jaccard_sim = calculate_jaccard_similarity(user_pref, match_profile, Ubinary_fields, binary_fields)  # 자카드 유사도를 계산
                euclidean_sim = calculate_euclidean_similarity(user_pref, match_profile, Ucontinuous_fields, continuous_fields)  # 유클리드 유사도를 계산

                combined_similarity = weight_binary * jaccard_sim + weight_continuous * (1 / (1 + euclidean_sim))  # 자카드 유사도와 유클리드 유사도를 결합
                similarities.append((match, combined_similarity))  # 유사도를 잠재적 매칭 사용자와 함께 리스트에 추가

            similarities.sort(key=lambda x: x[1], reverse=True)  # 유사도에 따라 내림차순으로 정렬
            return [match for match, similarity in similarities[:5]]  # 상위 5명의 매칭 사용자를 반환

        # 상위 매칭 사용자를 찾음
        top_matches = match_users(user_pref, user_list, Ubinary_fields, Ucontinuous_fields, binary_fields, continuous_fields)
        match_resultlist = [match.userID for match in top_matches]

        if match_resultlist:
            try:
                existing_match_result = Match.objects.get(userId=user)
                existing_match_result.updateAt = timezone.now()
                existing_match_result.userId1 = match_resultlist[0]
                existing_match_result.userId2 = match_resultlist[1]
                existing_match_result.userId3 = match_resultlist[2]
                existing_match_result.userId4 = match_resultlist[3]
                existing_match_result.userId5 = match_resultlist[4]
                existing_match_result.save()

                return Response({'success': True}, status=status.HTTP_200_OK)
            except Match.DoesNotExist:
                match_count = Match.objects.count() + 1
                match_result = Match.objects.create(matchId=match_count, userId=user,
                                             createdAt=timezone.now,
                                             userId1=match_resultlist[0], userId2=match_resultlist[1],
                                             userId3=match_resultlist[2], userId4=match_resultlist[3],
                                             userId5=match_resultlist[4])
                # match_result = Match.objects.create(matchId=match_count, userId=user,
                #                                     createdAt=timezone.now, updateAt=timezone.now,
                #                                     userId1=match_resultlist[0], userId2=match_resultlist[1],
                #                                     userId3=match_resultlist[2], userId4=match_resultlist[3],
                #                                     userId5=match_resultlist[4])
                match_result.save()

                return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


    # KSH : 매칭결과 조회 기능 추가
    @api_view(['GET'])
    def getmatchresult(request):
        logger.debug(f"Received data: {request.data}")

        userId = request.query_params.get('userId')
        userId = AppUser.objects.get(iD = userId)
        userId = userId.userID

        if userId is None:
            return Response({'success': False, 'error': 'UserID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            match_result = Match.objects.get(userId=userId)

            user1 = AppUser.objects.get(userID=match_result.userId1)
            user2 = AppUser.objects.get(userID=match_result.userId2)
            user3 = AppUser.objects.get(userID=match_result.userId3)
            user4 = AppUser.objects.get(userID=match_result.userId4)
            user5 = AppUser.objects.get(userID=match_result.userId5)

            response = [{
                'matchId': str(match_result.matchId), 'userId': str(userId),
                'user1ID': str(user1.userID), 'user1Name': user1.name, 'user1StudentId': user1.studentID,
                'user2ID': str(user2.userID), 'user2Name': user2.name, 'user2StudentId': user2.studentID,
                'user3ID': str(user3.userID), 'user3Name': user3.name, 'user3StudentId': user3.studentID,
                'user4ID': str(user4.userID), 'user4Name': user4.name, 'user4StudentId': user4.studentID,
                'user5ID': str(user5.userID), 'user5Name': user5.name, 'user5StudentId': user5.studentID,
            }]
            logger.debug(f"Response data: {response}")

            return Response(response, status=status.HTTP_200_OK)

        except Match.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
        except AppUser.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)

    # KSH : 매칭 요청 기능 추가
    @api_view(['POST'])
    def matchrequest(request):
        userId = request.data.get('userId')
        userId2 = request.data.get('userId2')

        try:
            user1 = AppUser.objects.get(iD=userId)
            user2 = AppUser.objects.get(userID=userId2)

            user1.matchStatus = 'matching'
            user2.matchStatus = 'matching'

            user1.save()
            user2.save()

            return Response({'success': True}, status=status.HTTP_200_OK)
        except AppUser.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)


        # Muser = ChatRoom.objects.get(user1=userId)
        # MuserId = Muser.user2
        #
        # try:
        #     match_result = Match.objects.get(userId=userId)
        #     match_result.matchStatus = 'matching'
        #
        #     Mmatch_result = Match.objects.get(userId=MuserId)
        #     Mmatch_result.matchStatus = 'matching'
        #
        #     match_result.save()
        #     Mmatch_result.save()

    # KSH : 매칭 수락 기능 추가
    @api_view(['POST'])
    def matchaccept(request):
        userId = request.data.get('userId')
        userId2 = request.data.get('userId2')

        try:
            user1 = AppUser.objects.get(iD=userId)
            user2 = AppUser.objects.get(userID=userId2)

            user1.matchStatus = 'accepted'
            user2.matchStatus = 'accepted'

            user1.save()
            user2.save()

            return Response({'success': True}, status=status.HTTP_200_OK)
        except AppUser.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)


    # KSH : 매칭 거절 기능 추가
    @api_view(['POST'])
    def matchreject(request):
        userId = request.data.get('userId')
        userId2 = request.data.get('userId2')

        try:
            user1 = AppUser.objects.get(iD=userId)
            user2 = AppUser.objects.get(userID=userId2)

            user1.matchStatus = 'pending'
            user2.matchStatus = 'pending'

            user1.save()
            user2.save()

            return Response({'success': True}, status=status.HTTP_200_OK)
        except AppUser.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)


# KSH : ReportViewSet 추가
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    # KSH : 유저 신고 기능 추가
    @api_view(['POST'])
    def reportuser(request):
        logger.debug(f"Received data: {request.data}")

        reporterId = request.data.get('reporterId')
        reporterId = AppUser.objects.get(iD = reporterId)

        reason = request.data.get('reason')

        reportedId = request.data.get('reportedId')
        reportedId = AppUser.objects.get(userID = reportedId)



        if reporterId and reason and  reportedId:
            report_count = Report.objects.count() + 1
            report = Report.objects.create(reportId = report_count, reporterId = reporterId,
                                           reason = reason,
                                           reportedId = reportedId)
            report.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)



# KSH : BlockViewSet 추가
class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    # KSH : blockuser 함수에 차단목록 추가/삭제 기능 한곳에 구현함
    @api_view(['POST', 'DELETE'])
    def blockuser(request):
        if request.method == 'POST':
            logger.debug(f"Received data: {request.data}")
            blockerId = request.data.get('blockerID')
            blockedId = request.data.get('blockedID')

            blocker = AppUser.objects.get(iD = blockerId)
            blocked = AppUser.objects.get(userID = blockedId)


            if blocker and blocked:
                block_count = Block.objects.count() + 1
                block = Block.objects.create(blockId = block_count, blockerId = blocker, blockedId = blocked)
                block.save()
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            blockerId = request.data.get('blockerId')
            blockedId = request.data.get('blockedId')

            blocker = AppUser.objects.get(iD = blockerId)
            blocked = AppUser.objects.get(iD = blockedId)

            if blocker and blocked:
                try:
                    block = Block.objects.get(blockerId = blocker, blockedId = blocked)
                    block.delete()
                    return Response({'success': True}, status=status.HTTP_200_OK)
                except Block.DoesNotExist:
                    return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    # KSH : 차단목록 조회 기능 추가
    @api_view(['GET'])
    def getblocklist(request):
        blockerId = request.data.get('blockerId')

        blocker = AppUser.objects.get(iD = blockerId)

        try:
            block_list = Block.objects.filter(blockerId = blocker)

            block_user_list = []
            for block in block_list:
                block_user = AppUser.objects.get(userID = block)
                block_user_list.append(block_user)
                #


            return Response({'block_list': block_user_list}, status=status.HTTP_200_OK)

        # 차단한 유저가 없을 때 우선 404로 처리하였음
        except Block.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
