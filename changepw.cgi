#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
echo "Cache-Control: private"
# --------------------------------------------------------------------------------
# THIS STUFF GETS forename AND username BASED ON COOKIE
unsetenv usertype
if($?HTTP_SESSION) then
setenv usertype `sql -d cah 'SELECT user FROM users WHERE session="$HTTP_SESSION"'`
if("$usertype" == "") unsetenv usertype
setenv username `sql -d cah 'SELECT username FROM users WHERE session="$HTTP_SESSION"'`
setenv userid `sql -d cah 'SELECT ID FROM users WHERE session="$HTTP_SESSION"'`
endif
# --------------------------------------------------------------------------------
if(! $?usertype) then
echo "Status: 204"
echo ""
exit 0
endif

if("$newpw" == "$confpw") then
  sql -d cah 'UPDATE users SET password=password("$newpw") WHERE session="$HTTP_SESSION"'
  echo "Location: index.cgi?SUCCESS=Password%20changed%20successfully"
else
  echo "Location: editpw.cgi?ERROR=Passwords%20do%20not%20match"
endif
echo ""
