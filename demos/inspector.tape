Output profile/inspector-demo.gif
Source demos/terminal.tape
Set Columns 54
Set Rows 24
Hide
Type@1ms "export PS1=''; clear"
Enter
Type@1ms "python3 scripts/profile_demos.py inspector --record"
Enter
Wait+Screen@30s /GUIDED CLI RUN/
Show
Sleep 12s
Screenshot profile/inspector-capture.png
Wait+Screen@45s /CASE VERIFIED/
Sleep 5s
