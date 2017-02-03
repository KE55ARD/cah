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

if("$mode" == "party") then
  echo "Location: newgame.cgi?mode=normal&ERROR=Sorry,%20this%20mode%20is%20not%20yet%20available"
  echo ""
  exit 0
endif

setenv game `sql -i -d cah 'INSERT INTO games (title,mode,created,owner,turn,cards) values ("$title","$mode",now(),"$userid","$userid","$limit")'`
sql -d cah 'INSERT INTO invites (user,game,inviter,sent) values ("$userid","$game","$userid",now())'
sql -d cah 'INSERT INTO deck (card,game,user,state,colour) SELECT ID,"$game","0","deck",colour FROM cards WHERE find_in_set(pack,"$packs")'
sql -d cah 'UPDATE deck SET user="$userid",state="inplay",selected=now() WHERE game="$game" AND colour="black" order by rand() limit 1'
sql -d cah 'UPDATE deck SET user="$userid",state="inhand",selected=now() WHERE game="$game" AND colour="white" order by rand() limit $limit'

foreach f(`echo "$packs" | sed 's/ /_/g'`)
  setenv pack `echo "$f" | sed 's/_/ /g'`
  sql -d cah 'INSERT INTO packs (game,pack) values ("$game","$pack")'
end

echo "Location: game.cgi?game=$game"
echo ""
