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
if(! $?usertype) then
  echo "Location: index.cgi?ERROR=You%20are%20not%20logged%20in"
  echo ""
  exit 0
endif

setenv owner `sql -d cah 'SELECT owner FROM games WHERE ID="$game"'`
if("$userid" == "$owner" || "$usertype" == "admin") then
  sql -d cah 'DELETE FROM games WHERE ID="$game"'
  sql -d cah 'DELETE FROM deck WHERE game="$game"'
  sql -d cah 'DELETE FROM packs WHERE game="$game"'
  sql -d cah 'DELETE FROM chat WHERE game="$game"'
  sql -d cah 'DELETE FROM invites WHERE game="$game"'
endif

echo "Location: play.cgi"
echo ""
