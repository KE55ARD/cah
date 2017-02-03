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
<h3>Play</h3>
<p></p>
'END'
