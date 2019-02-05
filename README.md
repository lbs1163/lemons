# 2018 Lemons Renewal
## Developer
* lbs1163
* mmj4594
* posko17
* anpandapoapper
* jelee999
* kimsj0302
* choisium

## Development Environment
### Basic
* web server: nginx
* middleware: uwsgi
* web framework: django
* database: sqlite(now) / postgresql (will be)

### pip list
* django==1.11.12
* django_crontab==0.7.1
* lxml==4.2.1
* requests==2.18.4

## Deploy Process
* 우선 깃에서 변경사항을 다운로드 받아옴  
`git pull`  
* 모든 커멘드는 virtual environment 안에서 동작해야함.  
`workon lemons`  
* 다음, static파일을 모두 root 디렉토리의 static으로 옮겨야 함(장고 기본 스테틱 파일도 옮겨야 함)  
`./manage.py collectstatic`  
* 혹여나 다른 pip 설치가 필요하다면 반드시 **requirements.txt**에 패키지명과 버전을 넣고 다음 커멘드를 실행하여 설치  
`pip install -r requirements.txt`  
