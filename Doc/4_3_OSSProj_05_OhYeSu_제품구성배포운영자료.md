# A4.3 OSS 프로젝트 제품 구성, 배포 및 운영 자료  

- *자료 내용이 길어지는 경우 별도 문서로 작성하고 링크로 연결*

## 1. 프로젝트 제품 구성

- [소스 코드 Overview](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/app/src/overveiw.md)<br>
- [소스 코드 간의 기능별 연계성 설명](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/blob/main/Doc/4_4_OSSProj_05_OhYeSu_%EB%B6%80%EB%A1%9D_%EC%86%8C%EC%8A%A4%EC%BD%94%EB%93%9C%EC%97%B0%EA%B3%84%EC%84%B1.md)
  
## 2. 프로젝트 제품 배포 방법  


## 1. EC2 인스턴스 생성
### 1.1 AWS 콘솔 접속
- AWS Management Console에 로그인
- EC2 서비스로 우분투를 선택
- "Launch Instance" 버튼을 클릭

### 1.2 인스턴스 설정 후 시작
- "Review and Launch" 버튼을 클릭
- 새 키 페어 생성 후 다운로드(.pem 파일)

## 2. RDS 인스턴스 생성
### 2.1 AWS 콘솔 접속
- AWS Management Console에 로그인
- RDS 서비스로 MySQL을 선택
- "Create database" 버튼을 클릭
- 데이터베이스 설정
### 2.2 VPC 및 보안 그룹 설정
- 기본 VPC 사용
- 보안 그룹: EC2 인스턴스와 동일한 보안 그룹 사용
### 2.3 데이터베이스 생성
- "Create database" 버튼을 클릭
## 3. 안드로이드 매니페스트 보안 설정
### 3.1 Network Security 설정 추가
- `AndroidManifest.xml` 파일의 맨 위에 다음 코드를 추가:
```xml
<application
    ...
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```
### 3.2 Network Security Config 파일 생성
- res/xml/network_security_config.xml 파일을 생성
- 다음 내용을 추가:
```
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">example.com</domain>
    </domain-config>
</network-security-config>
```
## 4. API Gateway와 EC2 연동
### 4.1 API Gateway 설정
- AWS Management Console에서 API Gateway 서비스를 선택
- 새 REST API를 생성
- 리소스를 생성하고 HTTP 메서드를 설정
- Integration 타입을 HTTP로 설정하고 EC2 인스턴스의 URL을 입력
## 5. 애플리케이션 설정 파일 업데이트
### 5.1 RDS 정보 갱신
- 애플리케이션의 설정 파일(`settings.py` 등)에 RDS 인스턴스 정보를 추가:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'myusername',
        'PASSWORD': 'mypassword',
        'HOST': 'mydatabase.endpoint.rds.amazonaws.com',
        'PORT': '3306',
    }
}
```
## 6. VPC 설정 및 EC2와 RDS 연동
### 6.1 VPC 설정
- EC2와 RDS 인스턴스가 동일한 VPC에 있는지 확인
- 보안 그룹에서 인바운드 규칙을 설정하여 EC2 인스턴스에서 RDS로의 접근을 허용
## 7. PuTTY 설정
### 7.1 .pem 키를 .ppk로 변환
- PuTTYgen을 다운 및 실행
- "Load" 버튼을 클릭하고 .pem 파일을 선택
- "Save private key" 버튼을 클릭하여 .ppk 파일로 저장
### 7.2 PuTTY를 사용하여 EC2 인스턴스에 접속
- PuTTY를 실행
- 호스트 이름에 EC2 인스턴스의 퍼블릭 DNS를 입력
- Connection -> SSH -> Auth에서 변환한 .ppk 파일을 로드
- "Open" 버튼을 클릭하여 접속
## 8. 애플리케이션 배포 준비
### 8.1 디렉토리 구성 및 소스 코드 클론
- EC2 인스턴스에 접속 후 작업할 디렉토리를 생성:
```bash
mkdir /var/www/myapp
cd /var/www/myapp
```
- Git을 사용하여 소스 코드를 클론:
```bash
https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05
```
### 8.2 가상 환경 생성
- Python 가상 환경을 생성하고 활성화:
```bash
python3 -m venv venv
source venv/bin/activate
```
### 8.3 요구 사항 설치
- 필요한 패키지를 설치:
```bash
pip install -r requirements.txt
```
## 9. 2차 배포 및 Nginx 설정
### 9.1 Nginx 및 uWSGI 설치
- Nginx와 uWSGI를 설치:
```bash
sudo apt update
sudo apt install nginx
pip install uwsgi
```
### 9.2 Nginx 설정 파일 구성
- Nginx 설정 파일을 생성하고 편집:
```bash
sudo nano /etc/nginx/sites-available/myapp
```
- 다음 내용을 추가:
```nginx
server {
    listen 80;
    server_name example.com;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/myapp/myapp.sock;
    }
}
```
- 심볼릭 링크를 생성:
```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
```
- 심볼릭 링크를 생성:
```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
```
### 9.3 uWSGI 설정 파일 구성
- uWSGI 설정 파일을 생성:
```bash
nano /var/www/myapp/myapp.ini
```
- 다음 내용을 추가:
```ini
[uwsgi]
chdir = /var/www/myapp
module = myapp.wsgi:application
home = /var/www/myapp/venv
socket = /var/www/myapp/myapp.sock
chmod-socket = 666
vacuum = true
```
### 9.4 Nginx 및 uWSGI 서비스 시작
- Nginx와 uWSGI를 시작하고 활성화:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
uwsgi --ini /var/www/myapp/myapp.ini
```
## 10. HTTPS 설정 및 무중단 배포
### 10.1 SSL 인증서 설치
- Certbot을 사용하여 SSL 인증서를 설치:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
```
### 10.2 무중단 배포 설정
- Nginx 설정 파일을 편집하여 무중단 배포를 설정:
```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/myapp/myapp.sock;
    }
}
```
- Nginx를 재시작:
```bash
sudo systemctl restart nginx
```
### 10.3 SSH 키 설정
- 무중단 배포를 위해 SSH 키를 설정:
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
ssh-copy-id user@yourserver.com
```
## 11. 관련된 파일
### 11.1 config.py 파일 구성
- 프로젝트 설정을 위한 `config.py` 파일을 구성:
```python
import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
```

## 3. 프로젝트 제품 운영 방법  

## 3.1 로컬에서의 운영 방법
- 시작 가이드(사용 방법)

### Requirements
로컬 환경에서 어플리케이션을 빌드하고 실행하려면 다음이 필요함:
```
* Android Studio
* MySql 8.0
* Ngrok 0.81
```
### Installation
```
> git clone https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05.git Kiri
> cd Kiri
```
### Backend

가상환경 생성 및 의존성 패키지 설치 -> DB 구성 -> DB 원격 접속 허용 -> Django에 구성한 DB 정보 입력

```
# virtual env composing

> python -m venv [venv-name]
> ./[venv-name]/Scripts/activate
> pip install -r requirements.txt
> pip install setuptools
```

```
# DB composing

# mysql workbench에서 데이터베이스 생성 (create database 명령어; 아래사진 참고)
```
![image](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/assets/144208568/3c9ef722-80f5-490e-8c0c-da2fdcf2198f)

```
# 아래 링크 참조하여 MySql 원격 접속 설정
https://blife.tistory.com/19

< 참고 >
CREATE USER '<계정명>'@'%' IDENTIFIED BY '<패스워드>';
예) CREATE USER ‘kim’@’%’ IDENTIFIED BY ‘oooooooo’;

GRANT ALL PRIVILEGES ON <데이터베이스명>.* TO '<계정명>'@'%';
- MYSQL에서 생성한 connection 내의 schema(=database)를 데이터베이스명에 입력
- 계정명에는 위 명령어로 생성한 계정명 입력 예) kim

FLUSH PRIVILEGES;
```

```
# Kiri_prj/settings.py에 아래와 같은 형식으로 DB 정보 입력

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '[DB table 명]',
        'USER': '[DB 사용자명]',
        'PASSWORD':'[DB 암호]',
        'HOST': '127.0.0.1',
        'PORT':'3306',
        'OPTIONS':{
            'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# 가상환경 상에서 아래 코드 실행

> python manage.py makemigrations
> python manage.py migrate
> python manage.py runserver
```



### Frontend
Django 서버 주소 외부로 포워딩 -> 포워딩 주소를 API 호출에 사용할 객체가 전달될 주소로 할당


```
# Ngrok 설치 ( 아래 링크 참조 )
https://yunwoong.tistory.com/131

아래 명령어 ngrok 터미널에서 실행 ( Django 서버는 8000 포트가 default )
> ngrok http 8000
```

```
# Django와 Retrofit 객체 라우팅

# app\src\main\java\com\example\mytestapp\entitiy\ApiFactory.kt
# 아래 baseUrl [ngrok 실행후 포워딩 된 주소] 로 수정

object ApiFactory {
    val retrofit: Retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("[ngrok 실행후 포워딩 된 주소]")
            .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
            .build()
    }

    inline fun <reified T> create(): T = retrofit.create(T::class.java)
}
```

### Build
![image](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/assets/144208568/8fccba47-025c-452c-972c-326ac2b66646)
```
1. 맨 오른쪽의 망치 모양 버튼 클릭 -> app build 시작
2. build 완료 후 중간의 재생 버튼 클릭 -> 안드로이드 에뮬레이터 시작
3. 어플 자동 설치 후 실행 됨
```
## 3.2 시연 시나리오  
#### 1. 회원가입
- **목표**: 새로운 사용자 회원가입 과정을 시연
- **절차**:
  1. 웹 브라우저를 열고 회원가입 페이지로 이동
  2. 사용자 정보를 입력하고 "가입" 버튼을 클릭
  3. 회원가입 완료 메시지를 확인
#### 2. 로그인
- **목표**: 기존 사용자 로그인 과정을 시연
- **절차**:
  1. 로그인 페이지로 이동
  2. 사용자명(`oys`)과 비밀번호(`1234`)를 입력
  3. "로그인" 버튼을 클릭
  4. 로그인 성공 후 대시보드 페이지로 리디렉션됨
#### 3. 룸메이트 프로필 생성
- **목표**: 룸메이트 프로필 생성 과정을 시연
- **절차**:
  1. 프로필 생성 페이지로 이동
  2. 생활습관과 성향을 버튼 클릭 형식으로 입력
  3. "저장" 버튼을 클릭하여 프로필을 생성
#### 4. 룸메이트 선호 정보 입력
- **목표**: 룸메이트에 대한 선호 정보 입력 과정을 시연
- **절차**:
  1. 선호 정보 입력 페이지로 이동
  2. 생활습관과 성향을 버튼 클릭 형식으로 입력
  3. "저장" 버튼을 클릭하여 선호 정보를 입력
#### 5. 매칭 실행하기
- **목표**: 룸메이트 매칭 실행 과정을 시연
- **절차**:
  1. 매칭 페이지로 이동
  2. "매칭 실행" 버튼을 클릭
  3. 매칭 결과를 확인
#### 6. 추천 목록 확인하기
- **목표**: 추천된 룸메이트 목록 확인 과정을 시연
- **절차**:
  1. 추천 목록 페이지로 이동
  2. 추천된 룸메이트 목록을 확인
#### 7. 특정 사용자 선택해서 채팅방으로 이동
- **목표**: 특정 사용자 선택 후 채팅방 이동 과정을 시연
- **절차**:
  1. 추천 목록에서 특정 사용자를 선택
  2. 채팅방으로 이동된 것을 확인
#### 8. 채팅으로 서로 입장 확인 후 매칭 진행
- **목표**: 채팅방에서 서로 입장 확인 후 매칭 진행 과정을 시연
- **절차**:
  1. 채팅방에서 사용자가 서로 인사 메시지를 보냄
  2. 매칭을 진행하기 위한 대화를 나눔
  3. 매칭 진행을 위한 버튼을 클릭하여 매칭을 완료
#### 9. 채팅방 내 신고 로직 보여주기
- **목표**: 채팅방 내 사용자 신고 과정을 시연
- **절차**:
  1. 채팅방 상단 메뉴바를 클릭
  2. "신고하기" 버튼을 클릭
  3. "사용자 신고" 확인 메시지에서 "네" 버튼을 클릭
  4. 신고 사유를 선택하고 "신고하기" 버튼을 클릭
  5. 신고 완료 메시지를 확인
#### 10. 채팅방 내 차단 로직 보여주기
- **목표**: 채팅방 내 사용자 차단 과정을 시연
- **절차**:
  1. 채팅방 상단 메뉴바를 클릭
  2. "차단하기" 버튼을 클릭
  3. "사용자 차단" 확인 메시지에서 "네" 버튼을 클릭
  4. 차단 완료 메시지를 확인
#### 11. 마이페이지로 이동 (로그아웃 기능 확인)
- **목표**: 마이페이지로 이동하여 로그아웃 기능을 확인
- **절차**:
  1. 마이페이지로 이동
  2. "로그아웃" 버튼을 클릭하여 로그아웃을 확인

## 3.3 주요 기능 시퀀스 다이어그램
- 매칭 입력 시퀀스 다이어그램    
![매칭 입력 시퀀스 다이어그램](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/assets/143872214/8e098f6b-30f4-465f-a4ab-f344a3ec6eb2)
- 매칭 신청/거절 시퀀스 다이어그램
![매칭 신청/거절 시퀀스 다이어그램](https://github.com/CSID-DGU/2024-1-OSSProj-OhYeSu-05/assets/143872214/3353aa0f-4798-4c41-9a01-3e09c6a698eb)
<br></br>
