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

echo "Cache-Control: private"
echo "Content-Type: text/html"
echo ""
xmlsql -d cah -- top.html - bottom.html << 'END'
<IF normal><SET mode='normal'></IF>
<IF party><SET mode='party'></IF>
<h3>New game</h3>
<form action='creategame.cgi'>
  <table class='form'>
    <tr>
      <td>Mode</td>
      <td>
        <select name='mode'>
          <option value='normal'>Normal</option>
          <option value='party'>Party</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>Select packs</td>
      <td>
        <sql table='cards' select='distinct pack' where='pack!="Original" AND pack!="Expansion 3"'>
          <sql table='cards' where='pack="$pack"' select='count(*) as count'><SET count='$count'></sql>
          <input type='checkbox' name='packs' value='$pack' id='$pack' checked='true'><label for='$pack'>&nbsp;<output name='pack'> (<output name='count'>)</label><br>
        </sql>
      </td>
    </tr>
    <tr>
      <td>Name this game</td>
      <td><input type='text' name='title' autofocus></td>
    </tr>
    <tr>
      <td>White card limit</td>
      <td><input type='number' name='limit' value='10' size='2'></td>
    </tr>
    <tr>
      <td></td>
      <td><input type='submit' value='Go!' class='btn btn-default'></td>
    </tr>
  </table>
</form>
'END'
