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
if("$usertype" != "admin" && $?user) then
  echo "Location: editpw.cgi?ERROR=You%20are%20not%20allowed%20to%20do%20that"
  echo ""
  exit 0
endif

setenv newpw `openssl rand -base64 10`
setenv email `sql -d cah 'SELECT email FROM users WHERE ID="$user"'`
setenv usersname `sql -d cah 'SELECT username FROM users WHERE ID="$user"'`
setenv localemail "info@cah.play.with.me.uk"

sql -d cah 'UPDATE users SET password=password("$newpw") WHERE ID="$user"'

email -t "$email" -f "$localemail" -s "Your password has been reset" << END
Your password for user '$usersname' has been reset to:

$newpw

We recommend you change it at your earliest convenience.
END

echo "Location: index.cgi?SUCCESS=Password%20reset%20successfully"
echo ""
