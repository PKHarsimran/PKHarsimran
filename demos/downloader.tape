Output profile/downloader-demo.gif
Source demos/terminal.tape
Set Columns 54
Set Rows 22
Hide
Type@1ms "export PS1=''; clear"
Enter
Type@1ms "python3 scripts/profile_demos.py downloader --record"
Enter
Wait+Screen@30s /GUIDED CLI RUN/
Show
Screenshot profile/downloader-capture.png
Wait+Screen@45s /OFFLINE MIRROR VERIFIED/
Sleep 5s
