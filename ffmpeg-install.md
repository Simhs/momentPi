
# 타임랩스 이미지파일생성

### ffmpeg 라이브러리 설치방법
>> http://engineer2you.blogspot.kr/2016/10/rasbperry-pi-ffmpeg-install-and-stream.html

### 이미지를 mp4로 변환시키는 명령어
>> ffmpeg -y -f image2 -i /home/pi/screenshot/image%d.jpg -preset fast /home/pi/screenshot/testlapse.mp4
