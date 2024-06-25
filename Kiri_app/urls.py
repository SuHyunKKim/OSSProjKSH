from django.conf import settings
from django.urls import include, path, re_path
from rest_framework import routers, permissions
from . import views #views.py import
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from Kiri_app import routing
from .views import ChatRoomListViewSet, ChatViewSet, UserViewSet

#API 명세서 자동 생성 drf-yasg
#swagger 정보 설정, 관련 엔드 포인트 추가
#swagger 엔드포인트는 DEBUG Mode에서만 노출

schema_view = get_schema_view(
    openapi.Info(
        title="Kiri API",
        default_version='v1',
        description="Kiri API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kimsteven728@gmail.com"),
        license=openapi.License(name="BSD License"),
    )
)

router = routers.DefaultRouter()
router.register('AppUser', views.UserViewSet)
router.register('ChatRoom', views.ChatRoomListViewSet)
# KSH: 채팅방 라우터 추가
router.register('Chat', views.ChatViewSet)
# KSH: 채팅 라우터 추가


# KSH: ProfileViewSet 추가
router.register('Profile', views.ProfileViewSet)
# KSH: UserPrefViewSet 추가
router.register('UserPref', views.UserPrefViewSet)
# KSH: MatchViewSet 추가
router.register('Match', views.MatchViewSet)


# KSH: ReportViewSet 추가
router.register('Report', views.ReportViewSet)
# KSH: BlockViewSet 추가
router.register('Block', views.BlockViewSet)



#swagger을 통한 path 추가
if settings.DEBUG:
    urlpatterns = [
        path('', include(router.urls)),
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')

    ]
    urlpatterns += [
        path('signup/', views.UserViewSet.signup, name='user-signup'),
        path('login/', views.UserViewSet.login_api, name='user-login'),
        path('get_user_id/', views.UserViewSet.get_user_id, name='get-user-id'),
        
        
        # 채팅방 리스트 링크, 채팅 내역 저장 링크, 채팅 내역 불러오기 링크 필요
        path('chatroomcreate/', views.ChatRoomListViewSet.chatroomcreate, name='chatroomcreate'),
        path('chatroomlist/', views.ChatRoomListViewSet.chatroomlist, name='chatroomlist'),
        path('getchathistory/', views.ChatRoomListViewSet.getchathistory, name='getchathistory'),

        path('savemessage/', views.ChatViewSet.savemessage, name='savemessage'),


        # KSH: ProfileViewSet 추가
        path('profilecreate/', views.ProfileViewSet.profilecreate, name='profilecreate'),
        path('profileupdate/', views.ProfileViewSet.profileupdate, name='profileupdate'),
        # KSH: UserPrefViewSet 추가
        path('userprefcreate/', views.UserPrefViewSet.userprefcreate, name='userprefcreate'),
        path('userprefupdate/', views.UserPrefViewSet.userprefupdate, name='userprefupdate'),

        # KSH: MatchViewSet 추가
        path('matching/', views.MatchViewSet.matching, name='matching'),
        path('getmatchresult/', views.MatchViewSet.getmatchresult, name='getmatchresult'),
        path('matchrequest/', views.MatchViewSet.matchrequest, name='matchrequest'),
        path('matchaccept/', views.MatchViewSet.matchaccept, name='matchaccept'),
        path('matchreject/', views.MatchViewSet.matchreject, name='matchreject'),


        # KSH: ReportViewSet 추가
        path('reportuser/', views.ReportViewSet.reportuser, name='reportuser'),
        # KSH: BlockViewSet 추가
        path('blockuser/', views.BlockViewSet.blockuser, name='blockuser'),
        path('getblocklist/', views.BlockViewSet.getblocklist, name='getblocklist'),

        # path('ws', include('Kiri_app.routing'))
        # path('ws', include(routing.websocket_urlpatterns))
    ]

from django.urls import re_path
from Kiri_app import routing as chat_routing

websocket_urlpatterns = chat_routing.websocket_urlpatterns

urlpatterns += websocket_urlpatterns