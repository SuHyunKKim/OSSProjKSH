# OverView

## 목차
1. [앱 디렉토리 구조](#앱-디렉토리-구조) 
2. [백엔드 서비스 구조](#백엔드-서비스-구조)
/ 소스코드 재활용,수정코딩,원천 코딩은 url 연결로 대체
/ [엑셀파일 첨부](https://docs.google.com/spreadsheets/d/1G2xiXtYlUwoaFolgzrr8GryXNJyTBzeQ/edit#gid=1052783101) 
3. [소스 코드 간의 연계성](#소스-코드-간의-연계성)
/ 소스코드간의 연계성 파일 따로 첨부


## 앱 디렉토리 구조

### src/main

#### java/com/example/mytestapp (UI 동작을 위한 코드 디렉토리)

##### adapter
- **[BlockRecyclerAdapter.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/adapter/BlockRecyclerAdapter.kt)**
  - RecyclerView에 차단 목록을 표시하고, 각 아이템의 차단 해제 버튼 클릭 이벤트를 처리하는 코드.
- **[ChatAdapter.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/adapter/ChatAdapter.kt), [ChatHistoryAdapter.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/adapter/ChatHistoryAdapter.kt)**
  - RecyclerView에 표시되는 채팅 메시지와 매칭 요청을 효율적으로 관리하고 동작하게 하는 코드.
- **[MatchingAdapter.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/adapter/MatchingAdapter.kt)**
  - RecyclerView에 매칭 프로필을 표시하고, 데이터가 변경될 때 갱신이 이루어지게 하는 코드.

##### chat
- **[BlockUserActivity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/chat/BlockUserActivity.kt)**
  - 다른 사용자를 차단할 수 있는 실질적인 로직이 있는 코드.
- **[ChatActivity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/chat/ChatActivity.kt), [ChatHistoryFragment.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/chat/ChatHistoryFragment.kt)**
  - 사용자 간의 채팅을 위한 코드. 메시지를 보내고, 받은 메시지를 확인할 수 있음.
- **[ReportUserActivity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/chat/ReportUserActivity.kt)**
  - 사용자 간의 신고를 위한 코드. 신고 대상 사용자의 ID를 받아와서 해당 사용자를 신고.

##### entity
- **[ApiFactory.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/entitiy/ApiFactory.kt)**
  - Retrofit 라이브러리를 사용하여 RESTful API와 통신하는 서비스 객체들을 생성하고 관리하는 코드.
  - 참고: 프로젝트 ['펀칭' 구조](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/blob/main/app/src/main/java/com/example/testapplication/entity/ApiFactory.kt) 참고 및 수정

##### match
- **[MatchingOption1Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/match/MatchingOption1Activity.kt), [MatchingOption2Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/match/MatchingOption2Activity.kt), [MatchingOption3Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/match/MatchingOption3Activity.kt), [MatchingOption4Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/match/MatchingOption4Activity.kt), [MatchingING.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/match/MatchingING.kt), [MatchingFragment.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/match/MatchingFragment.kt)**
  - 룸메이트 매칭을 위한 선호조건을 입력받고 저장하여 서버로 전달하는 코드.
  - MatchingFragment에서는 매칭 프로필을 효과적으로 표시하고, 사용자의 상호작용에 따라 동적으로 UI를 업데이트.
  - 참고: 프로젝트 ['펀칭' 코드](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/tree/main/app/src/main/java/com/example/testapplication/matching) 참고 및 수정

##### matchmaking
- **[MatchmakingActivity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/matchmaking/MatchmakingActivity.kt)**
  - 사용자 정보 조회, 매칭 요청 전송, WebSocket 연결을 통한 실시간 메시지 전송을 위한 코드.

##### model
- **[request](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/tree/main/app/src/main/java/com/example/mytestapp/model/request), [response](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/tree/main/app/src/main/java/com/example/mytestapp/model/response)**
  - 서버에 정보를 전달하거나 요청을 위한 데이터 클래스들을 정의.
  - 참고: 프로젝트 ['펀칭' 구조](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/tree/main/app/src/main/java/com/example/testapplication/model) 참고 및 수정

##### profile
- **[ProfileOption1Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/profile/ProfileOption1Activity.kt), [ProfileOption2Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/profile/ProfileOption2Activity.kt), [ProfileOption3Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/profile/ProfileOption3Activity.kt), [ProfileOption4Activity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/profile/ProfileOption4Activity.kt)**
  - 프로필 생성을 위한 옵션을 입력받고 저장하여 프로필 정보를 서버로 전달하는 코드.
  - 참고: 프로젝트 ['펀칭' 코드](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/tree/main/app/src/main/java/com/example/testapplication/create_room) 참고 및 수정

##### service
- **[KiriService.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/service/KiriService.kt)**
  - 서버에서 제공하는 특정 엔드포인트에 대한 HTTP 요청을 정의하는 API 서비스 인터페이스에 대한 코드.
  - 참고: 프로젝트 ['펀칭' 코드](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/tree/main/app/src/main/java/com/example/testapplication/service) 참고 및 수정

##### sign
- **[LoginActivity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/sign/LoginActivity.kt), [SignupActivity.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/sign/SignupActivity.kt)**
  - 회원가입을 위한 정보를 입력받고 로그인 성공 여부를 판단하는 코드.
  - 참고: 프로젝트 ['펀칭' 코드](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/tree/main/app/src/main/java/com/example/testapplication/sign) 참고 및 수정

##### ui/theme
- **[Color.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/ui/theme/Color.kt), [Theme.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/ui/theme/Theme.kt), [Type.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/ui/theme/Type.kt)**
  - 앱의 전반적인 디자인을 정의하는 코드들

##### viewmodel
- **[MatchingViewModel.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/viewmodel/MatchingViewModel.kt)**
  - 매칭 프로필 목록을 관리하는 뷰모델 정의
- **[ChatHistoryViewModel.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/viewmodel/ChatHistotyViewModel.kt), [ChatRoomViewModel.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/viewmodel/ChatRoomViewModel.kt)**
  - 채팅 기능 관련 뷰모델 정의

##### websocket
- **[WebsockerManager.kt](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/java/com/example/mytestapp/websocket/WebsocketManager.kt)**
  - 앱에서 WebSocket을 사용하여 실시간 통신(채팅)을 구현하는 코드.


##### res (앱의 화면 구성을 위한 디렉토리)
- **drawable**
  - button_rec_orange.xml, chatbox_sent.xml 등
  - 앱의 UI를 구성하는데 사용되는 여러 그래픽 리소스들을 저장.
- **font**
  - pretendard.ttf 등
  - 앱의 UI를 구성하는데 사용되는 폰트 리소스들을 저장.
- **layout**
  - [activity_login.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/layout/activity_login.xml), [activity_chat.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/layout/activity_chat.xml), [fragment_matching.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/layout/fragment_matching.xml) 등 여러 xml 파일 존재
  - 앱의 각 화면의 레이아웃을 정의하고, UI 요소들의 배치와 속성을 지정하는 XML 파일들.
  - 참고: 일부는 프로젝트 ['펀칭' 코드](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/tree/main/app/src/main/res/layout) 참고 및 수정
- **menu**
  - [chat_menu.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/menu/chat_menu.xml), [item_menu.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/menu/item_menu.xml)
  - 홈 화면의 메뉴바나 채팅의 메뉴 옵션을 정의하기 위한 xml 코드.
  - 참고: 프로젝트 ['펀칭' 코드](https://github.com/CSID-DGU/2023-1-OSSP1-criminal6-1/tree/main/app/src/main/res/menu) 참고 및 수정
- **values**
  - [array.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/values/array.xml), [colors.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/values/colors.xml), [strings.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/values/strings.xml), [themes.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/res/values/themes.xml)
  - 앱의 UI를 구성하는데 사용되는 색상 및 문자열 저장

##### [AndroidManifest.xml](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/main/AndroidManifest.xml)
- 앱의 구조와 동작 방식을 지정하여 앱의 핵심적인 구성 정보를 포함하는 파일

##### [build.gradle.kts](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/build.gradle.kts)
- 앱을 빌드하기 위한 Gradle 빌드 스크립트. 필요한 외부 라이브러리 및 모듈의 종속성들을 관리하는 파일.

## 백엔드 서비스 구조

### Django

#### Kiri_app
- **[admin.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/admin.py)**
  - Django 관리 인터페이스로 모델의 데이터를 쉽게 등록하고 관리하기 위한 코드
- **[apps.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/apps.py)**
  - Kiri앱에 대한 Django 기본 설정을 정의
- **[consumers.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/consumers.py)**
  - Django Channels를 사용하여 웹 소켓 통신을 처리하는 ChatConsumer 클래스
- **[models.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/models.py)**
  - 앱에 필요한 데이터베이스 테이블을 정의. 필요한 필드와 해당 관계 정의.
- **[routing.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/routing.py)**
  - Django Channels를 사용하여 실시간 채팅을 처리하는 WebSocket 경로 설정
- **[serializers.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/serializers.py)**
  - Django REST Framework(DRF)에서 JSON 형식으로 데이터 직렬화를 하기 위한 파일
- **[tests.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/tests.py)**
  - Django의 테스트 케이스를 정의하기 위한 파일
- **[urls.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/urls.py)**
  - Django 앱의 URL 설정을 관리 및 API 엔드포인트와 Swagger 문서를 설정
- **[views.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_app/views.py)**
  - 사용자 등록 및 로그인, 채팅 관련 기능, 사용자 프로필 관리, 매칭 기능, 신고 및 차단 기능 등 백엔드 로직 구현

#### Kiri_prj
- **[asgi.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_prj/asgi.py)**
  - HTTP 요청과 웹소켓 요청을 구분하고 라우팅을 수행하는 코드
- **[settings.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_prj/settings.py)**
  - 데이터베이스 설정, 인증, 국제화, 정적 파일 처리 등 Django 웹 프레임워크의 기본 설정을 구성
- **[urls.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_prj/urls.py)**
  - URL 경로를 관리하고, 요청을 처리하는 뷰로 라우팅하는 파일
- **[wsgi.py](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Kiri_prj/wsgi.py)**
  - Django 프로젝트 "Kiri_prj"의 WSGI 구성 정의

## 소스 코드 간의 연계성

- **[기능별 소스 코드 간의 연계성](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Doc/4_4_OSSProj_05_OhYeSu_%EB%B6%80%EB%A1%9D_%EC%86%8C%EC%8A%A4%EC%BD%94%EB%93%9C%EC%97%B0%EA%B3%84%EC%84%B1.md)**
 해당 링크를 통해 각 기능별 소스 코드 간의 연계성 확인 가능

***
## 기능 구현 여부 정리
| 기능               | 기능 설명                                    | 구현 여부 |
|--------------------|---------------------------------------------|-----------|
| 회원가입       | ID, 비밀번호, 이름, 학번, 성별 정보로 회원가입  | 구현 완료    |
| 로그인       | 회원가입 정보를 이용하여 로그인 | 구현 완료    |
| 프로필 정보 입력     | 질문지에 따라 성향과 생활습관 정보 입력 및 저장                  | 구현 완료    |
| 룸메이트 선호 정보 입력      | 질문지에 따라 룸메이트에 대한 선호 생활습관 입력                         | 구현 완료    |
| 룸메이트 추천      | 유사도 기반 매칭 알고리즘을 통한 룸메이트 5명 추천                      | 구현 완료    |
| 채팅| 추천 목록과 실시간 채팅 가능           | 구현 완료    |
| 매칭 성사      | 최종적으로 룸메이트와 매칭 가능                  | 구현 중    |
| 상대 유저 신고      | 유저 신고 가능 및 신고 사유 선택 가능          | 구현 완료    |
| 상대 유저 차단          | 유저 차단하기                       | 수정 필요    |
| 마이페이지     | 프로필 정보 수정 및 로그아웃 가능                  | 구현 완료    |

