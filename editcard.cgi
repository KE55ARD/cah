#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
# THIS STUFF GETS forename AND username BASED ON COOKIE
unsetenv usertype
if($?HTTP_SESSION) then
  setenv usertype `sql -d cah 'SELECT user FROM users WHERE session="$HTTP_SESSION"'`
  if("$usertype" == "") unsetenv usertype
  setenv username `sql -d cah 'SELECT username FROM users WHERE session="$HTTP_SESSION"'`
  setenv userid `sql -d cah 'SELECT ID FROM users WHERE session="$HTTP_SESSION"'`
  setenv useremail `sql -d cah 'SELECT email FROM users WHERE session="$HTTP_SESSION"'`
endif
# --------------------------------------------------------------------------------
if("$usertype" != "admin") then
  echo "Location: index.cgi?ERROR=You%20are%20not%20allowed%20to%20do%20that"
  echo ""
  exit 0
endif

if("$text" != "") then
  sql -d cah 'UPDATE cards SET text="$text" WHERE ID="$cardid"'
endif
if("$pick" != "" && "$pick" != 0) then
  sql -d cah 'UPDATE cards SET pick="$pick" WHERE ID="$cardid"'
endif

echo "Location: index.cgi?SUCCESS=Card%20$cardid%20changed"
echo ""
