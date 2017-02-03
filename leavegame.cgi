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

setenv owner `sql -d cah 'SELECT owner FROM games WHERE ID="$game"'`
setenv ownertime `sql -d cah 'SELECT sent FROM invites WHERE user="$turn" AND game="$game"'`
#If the owner of the game is running this and they have specified a user to remove, then allow them to specify which user leaves, otherwise the user running this is leaving
if($?thisuser && "$owner" == "$userid") then
  setenv user "$thisuser"
  setenv thisusername `sql -d cah 'SELECT username FROM users WHERE ID="$thisuser"'`
  setenv message "$thisusername was removed from the game :("
else
  setenv user "$userid"
  setenv message "$username left the game :("
endif

#Who's go is it now, and at what time were they invited
setenv turn `sql -d cah 'SELECT turn FROM games WHERE ID="$game"'`
setenv turntime `sql -d cah 'SELECT sent FROM invites WHERE user="$turn" AND game="$game"'`

#Return current cards in play
sql -d cah 'UPDATE deck SET state="inhand" WHERE game="$game" AND colour="white" AND state="inplay"'

#Remove user from the game
sql -d cah 'DELETE FROM invites WHERE user="$user" AND game="$game"'
sql -d cah 'INSERT INTO chat (msg,game,user,sent) values ("$message","$game","0",now())'

#Work out who gets the next black card
setenv nextturn `sql -d cah 'SELECT user FROM invites WHERE sent>"$turntime" AND game="$game" order by sent limit 1'`
if("$nextturn" == "") then
  setenv nextturn `sql -d cah 'SELECT user FROM invites WHERE game="$game" order by sent limit 1'`
endif

#Move the black card onto the next user if the leaver had the black card
if("$turn" == "$user") then
  sql -d cah 'UPDATE games SET turn="$nextturn" WHERE ID="$game"'
  sql -d cah 'UPDATE deck SET user="$nextturn",state="inplay",selected=now() WHERE game="$game" AND state="inplay" AND colour="black" AND ID!="718" order by rand() limit 1'
endif

#Work out who the next game owner would be
setenv nextowner `sql -d cah 'SELECT user FROM invites WHERE sent>"$ownertime" AND game="$game" order by sent limit 1'`
if("$nextowner" == "") then
  setenv nextowner `sql -d cah 'SELECT user FROM invites WHERE game="$game" order by sent limit 1'`
endif

#Change the game owner if the owner is leaving
if("$owner" == "$user") then
  sql -d cah 'UPDATE games SET owner="$nextowner" WHERE ID="$game"'
endif

echo "Location: play.cgi"
echo ""
