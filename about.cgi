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

echo "Cache-Control: private"
echo "Content-Type: text/html"
echo ""
xmlsql -d cah -- top.html - bottom.html << 'END'
<h3>About the game</h3>
<p>Playing Cards Against Humanity is pretty simple, it's mainly a case of pairing black cards (questions) with white cards (answers) in the best/funniest way possible!</p>

<br>

<h4>For example:</h4>
<div class='row center'>
  <sql table='cards' limit='1' order='rand()' where='colour="black"'>
    <div class='card black col-xs-2'><output name='text' replace '-'='_____'></div>
    <sql table='cards' limit='$pick' order='rand()' where='colour="white"'>
      <div class='card white col-xs-2'><output name='text'></div>
    </sql>
  </sql>
</div>
'END'
