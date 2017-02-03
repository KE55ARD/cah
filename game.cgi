#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
unsetenv usertype
if($?HTTP_SESSION) then
  setenv usertype `sql -d cah 'SELECT user FROM users WHERE session="$HTTP_SESSION"'`
  if("$usertype" == "") unsetenv usertype
  setenv userid `sql -d cah 'SELECT ID FROM users WHERE session="$HTTP_SESSION"'`
  setenv useremail `sql -d cah 'SELECT email FROM users WHERE session="$HTTP_SESSION"'`
endif
# --------------------------------------------------------------------------------

if(! $?usertype) then
  echo "Location: index.cgi?ERROR=You%20are%20not%20logged%20in&game=$game"
  echo ""
  exit 0
endif

if(`sql -d cah 'SELECT COUNT(*) FROM games WHERE ID="$game"'` == 0 || `sql -d cah 'SELECT COUNT(*) FROM invites WHERE game="$game" AND user="$userid"'` != 1) then
  echo "Location: play.cgi?ERROR=This%20game%20does%20not%20exist%20or%20you%20are%20not%20in%20it&game=$game"
  echo ""
  exit 0
endif

setenv owner `sql -d cah 'SELECT owner FROM games WHERE ID="$game"'`

echo "Cache-Control: private"
echo "Content-Type: text/html"
echo ""

xmlsql -d cah -- top.html - bottom.html << 'END'
<script var='game'></script>
<script src='game.js'></script>
<sql table='games' where='ID="$game"'>

  <div>
    <div class='pull-right'>
      <form class='form-inline'>
        <input type='checkbox' id='speak' title='If ticked, the game will read out each new black card' style='margin-right: 10px;' />
        <select id='refreshtimer' title='Refresh timer' class='form-control ml-1'>
          <option value='1000'>1s</option>
          <option value='3000'>3s</option>
          <option value='5000' selected>5s</option>
          <option value='10000'>10s</option>
          <option value='30000'>30s</option>
        </select>
        <button type='button' class='btn btn-success' id='invitebutton' title='Add a user to this game'><span class='fa fa-user-plus'></span><span class='hidden-md-down ml-1'>Invite</span></button>
      </form>
    </div>
    <h3 id='gametitle'><output name='title'></h3>
  </div><hr>

  <div id='invite' class='right'>
    <IF userid='$owner' OR usertype='admin'>
      <form action='deletegame.cgi' class='pull-left'>
        <input type='hidden' name='game' value='$game'>
        <button type='submit' class='btn btn-danger' title='End and delete this entire game'><span class='fa fa-trash'></span><span class='hidden-md-down ml-1'>Delete Game</span></button>
      </form>
    </IF>
    <form action='invite.cgi' id='inviteform' class='form-inline'>
      <input type='hidden' name='game'>
      <div class='input-group'>
        <input type='text' name='username' class='form-control ddropsearch' script='getusernames.cgi' placeholder='Username' id='inviteusername'>
        <div class='input-group-btn'><button type='submit' class='btn btn-success' id='invitesubmit'><span class='fa fa-plus'></span><span class='hidden-md-down ml-1'>Add</span></button></div>
      </div>
    </form>
    <hr>
  </div>

  <div class='row'>
    <div id='blackdiv' class='col-xs-8 pad5'></div>
    <div id='invites' class='col-xs-4 pad5'>
      <h4>Players</h4>
      <div id='invitediv'></div>
    </div>
  </div>
  <hr>
  <div id='whitediv' class='cardrow'></div>
  <div id='mycards' class='cardrow'></div>
  <div id='chat'>
    <h4>Chat</h4>
    <form action='chat.cgi' id='chatform'>
      <div class='input-group'>
        <input type='hidden' name='game' value='$game'>
        <input type='text' name='msg' placeholder='Chat' class='form-control' autocomplete='off' autofocus>
        <span class='input-group-btn'><button type='submit' class='btn btn-success'><span class='fa fa-send'></span><span class='hidden-md-down ml-1'>Send</span></span>
      </div>
    </form>
    <div id='chatdiv'></div>
  </div>
  <div id='temp'></div>
</sql>
'END'
