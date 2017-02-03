#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
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

echo "Cache-Control: private"
echo "Content-Type: text/html"
echo ""
xmlsql -d cah -- top.html - bottom.html << 'END'
<h3>New game</h3>
<p>You (will) have 2 choices when playing. Play a normal game, or play a guest party game.</p>
<hr>
<div class='row'>
  <div class='col-xs-12 col-md-6 center'>
    <form action='newgame.cgi'><input type='submit' name='normal' value='Play normal game' class='wide btn btn-primary' title='Take the blue pill...'></form><br>
    <p>In a normal game, you invite the members you want to play with and you can all play from wherever you are (as long as you have an internet connection and a device each).</p>
  </div>
  <div class='col-xs-12 col-md-6 center'>
    <form action='newgame.cgi'><input type='submit' name='party' value='Play party game' class='wide btn btn-danger' title='Take the red pill...' disabled='true'></form><br>
    <p>In a party guest game you are the administrator of an on screen party game, where any number of people can play as long as you are physically in the same room. (Not yet available as it&#39;s still under development, sorry).</p>
  </div>
</div>
<sql table='invites' where='user="$userid"' select='COUNT(*) as invites'><SET invites='$invites'></sql>
<IF NOT invites='0'>
  <hr>
  <h3>Existing games</h3>
  <div class='row'>
    <sql table='invites' where='user="$userid"'>
      <form action='game.cgi' class='col-xs-6 col-sm-4 col-md-3'><input type='hidden' name='game' value='$game'><sql table='games' where='ID="$game"'><input type='submit' value='$title' class='wide btn btn-primary marginbot20'></sql></form>
    </sql>
  </div>
</IF>
'END'
