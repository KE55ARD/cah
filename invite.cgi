#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
# THIS STUFF GETS forename AND username BASED ON COOKIE
unsetenv usertype
if($?HTTP_SESSION) then
  setenv usertype `sql -d cah 'SELECT user FROM users WHERE session="$HTTP_SESSION"'`
  if("$usertype" == "") unsetenv usertype
  setenv userid `sql -d cah 'SELECT ID FROM users WHERE session="$HTTP_SESSION"'`
  setenv myusername `sql -d cah 'SELECT username FROM users WHERE session="$HTTP_SESSION"'`
  setenv useremail `sql -d cah 'SELECT email FROM users WHERE session="$HTTP_SESSION"'`
endif
# --------------------------------------------------------------------------------

if(! $?usertype) then
  echo "Location: index.cgi?ERROR=You%20are%20not%20logged%20in"
  echo ""
  exit 0
endif

setenv owner `sql -d cah 'SELECT owner FROM games WHERE ID="$game"'`
setenv user `sql -d cah 'SELECT ID FROM users WHERE username="$username"'`
setenv email `sql -d cah 'SELECT email FROM users WHERE ID="$user" AND (active<DATE_SUB(NOW(), interval 1 hour) OR session="")'`
setenv localemail "play@cah.play.with.me.uk"
setenv invites `sql -d cah 'SELECT count(*) FROM invites WHERE user="$user" AND game="$game"'`
setenv inhand `sql -d cah 'SELECT count(*) FROM deck WHERE game="$game" AND user="$user" AND state="inhand"'`
if("$user" != "" && "$invites" == 0) then
  setenv limit `sql -d cah 'SELECT cards-$inhand FROM games WHERE ID="$game"'`
  sql -d cah 'INSERT INTO invites (user,game,inviter,sent) values ("$user","$game","$userid",now())'
  sql -d cah 'INSERT INTO chat (msg,game,user,sent) values ("$myusername invited $username to play :)","$game","0",now())'
  sql -d cah 'UPDATE deck SET user="$user",state="inhand",selected=now() WHERE game="$game" AND user=0 AND colour="white" order by rand() limit $limit'
  if("$email" != "") then
    setenv title `sql -d cah 'SELECT title FROM games WHERE ID="$game"'`
    sql -d cah 'UPDATE users SET active=now() WHERE ID="$user"'
    email -t "$email" -f "$localemail" -s "You have been invited to play a game of Cards Against Humanity" << END
$myusername invited you to play a game: "$title"

http://cah.play.with.me.uk/game.cgi?game=$game
END
  endif
  echo "Status: 204"
  echo ""
endif
if("$user" != "" && "$invites" > 0 && "$owner" == "$userid" && "$user" != "$userid") then
  echo "Location: leavegame.cgi?game=$game&thisuser=$user"
  echo ""
  exit 0
endif
