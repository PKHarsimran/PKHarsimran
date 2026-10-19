Output profile/downloader-demo.gif
Set Width 900
Set Height 700
Source demos/terminal.tape
Hide
Type@1ms "export PS1=''; clear"
Enter
Type@1ms "python3 scripts/profile_demos.py downloader --record"
Enter
Wait+Screen@30s /GUIDED CLI RUN/
Show
Wait+Screen@45s /OFFLINE MIRROR VERIFIED/
Sleep 5s
