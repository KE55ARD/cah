#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
# THIS STUFF GETS forename AND username BASED ON COOKIE
unsetenv usertype
if($?HTTP_SESSION) then
  setenv usertype `sql -d cah 'SELECT user FROM users WHERE session="$HTTP_SESSION"'`
  if("$usertype" == "") unsetenv usertype
  setenv userid `sql -d cah 'SELECT ID FROM users WHERE session="$HTTP_SESSION"'`
  setenv useremail `sql -d cah 'SELECT email FROM users WHERE session="$HTTP_SESSION"'`
endif
# --------------------------------------------------------------------------------

if(! $?usertype) then
  echo "Location: index.cgi?ERROR=You%20are%20not%20logged%20in"
  echo ""
  exit 0
endif

sql -d cah 'UPDATE users SET refresh="$timer" WHERE session="$HTTP_SESSION"'
echo "Status: 204"
echo ""
