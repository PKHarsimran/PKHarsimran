Output profile/downloader-demo-mobile.gif
Source demos/terminal.tape
Set Columns 34
Set Rows 24
Hide
Type@1ms "export PS1=''; clear"
Enter
Type@1ms "python3 scripts/profile_demos.py downloader --record --compact"
Enter
Wait+Screen@30s /GUIDED CLI RUN/
Show
Wait+Screen@45s /OFFLINE MIRROR VERIFIED/
Sleep 5s
