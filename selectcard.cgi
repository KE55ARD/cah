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

setenv state `sql -d cah 'SELECT state FROM deck WHERE card="$card" AND game="$game"'`
sql -d cah 'UPDATE games SET lastmove=now() WHERE ID=$game'

if("$state" == "inplay") then

  #Grab necessary vars
  setenv blackcard `sql -d cah 'SELECT card FROM deck WHERE game="$game" AND state="inplay" AND colour="black"'`
  setenv blackcardtext `sql -d cah 'SELECT text FROM cards WHERE ID="$blackcard"'`
  setenv pick `sql -d cah 'SELECT pick FROM cards WHERE ID="$blackcard"'`
  setenv turn `sql -d cah 'SELECT turn FROM games WHERE ID="$game"'`
  setenv turntime `sql -d cah 'SELECT sent FROM invites WHERE user="$turn" AND game="$game"'`
  setenv winnersid `sql -d cah 'SELECT user FROM deck WHERE card="$card" AND game="$game"'`
  setenv winnersname `sql -d cah 'SELECT username FROM users WHERE ID="$winnersid"'`
  setenv winningtext "$blackcardtext"
  setenv cardtext ""
  foreach w(`sql -d cah 'SELECT card FROM deck WHERE game="$game" AND colour="white" AND state="inplay" AND user="$winnersid" order by selected'`)
    setenv cardid "$w"
    setenv cardtext `sql -d cah 'SELECT text FROM cards WHERE ID="$cardid"'`
    setenv winningtext `echo "$winningtext" | sed -r "s/(_+)/$cardtext/"`
  end
  if("$winningtext" == "$blackcardtext") setenv winningtext "$winningtext > $cardtext"

  #Announce winner and dispose of cards while recording winner
  sql -d cah 'INSERT INTO chat (msg,game,user,sent) values ("<b>$winnersname</b> won that round with <b>$winningtext</b>","$game","0",now())'
  sql -d cah 'UPDATE deck SET state="won",won="$blackcard" WHERE user="$winnersid" AND state="inplay" AND game="$game"'
  sql -d cah 'UPDATE deck SET won="$card",user="$winnersid" WHERE card="$blackcard" AND game="$game"'
  sql -d cah 'UPDATE deck SET state="used" WHERE game="$game" AND state="inplay"'

  #Dish out cards to those who just played
  foreach f(`sql -d cah 'SELECT user FROM invites WHERE game="$game" AND user!="$turn"'`)
    setenv user "$f"
    sql -d cah 'UPDATE deck SET user="$user",state="inhand",selected=now() WHERE game="$game" AND state="deck" AND colour="white" order by rand() limit $pick'
  end

  #Move onto the next user
  setenv nextturn `sql -d cah 'SELECT user FROM invites WHERE sent>"$turntime" AND game="$game" order by sent limit 1'`
  if("$nextturn" == "") then
    setenv nextturn `sql -d cah 'SELECT user FROM invites WHERE game="$game" order by sent limit 1'`
  endif
  sql -d cah 'UPDATE games SET turn="$nextturn" WHERE ID="$game"'
  sql -d cah 'UPDATE deck SET user="$nextturn",state="inplay",selected=now() WHERE game="$game" AND state="deck" AND colour="black" AND ID!="718" order by rand() limit 1'

else
  sql -d cah 'UPDATE deck SET state="inplay",selected=now() WHERE card="$card" AND game="$game"'
endif

echo "Status: 204"
echo ""
