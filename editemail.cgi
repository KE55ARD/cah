#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
echo "Cache-Control: private"
echo "Content-Type: text/html"
echo ""
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

xmlsql -d cah -- top.html - bottom.html << 'END'
<IF usertype>
<form action='changeemail.cgi' method='post'>
  <div class='input-group'><span class='input-group-addon'><span class='fa fa-envelope'></span></span><input type='email' name='newemail' class='form-control' value='$useremail' placeholder='New email' autofocus /></div>
  <div class='input-group'><span class='input-group-addon'><span class='fa fa-check'></span></span><input type='email' name='confemail' class='form-control' placeholder='Confirm email' /></div>
  <br><input type='submit' value='Change Email' class='btn btn-default' />
</form>
</IF>
'END'
