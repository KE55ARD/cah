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

setenv site "cah"

echo "Cache-Control: private"
echo "Content-Type: text/html"
echo ""
xmlsql -d cah -- top.html - bottom.html << 'END'
<IF usertype>
  <h3>My account</h3>
  <div class='row'>
    <div class='col-xs-6 col-md-4'><a href='editpw.cgi' class='btn btn-primary btn-block'>Change password</a></div>
    <div class='col-xs-6 col-md-4'><a href='editemail.cgi' title='$useremail' class='btn btn-primary btn-block'><IF useremail=''>PLEASE SET EMAIL ADDRESS</IF><IF ELSE>Change email address</IF></a></div>
  </div>
  <IF usertype='admin'>
    <hr>
    <h4>Edit card</h4>
    <form action='editcard.cgi' class='form-inline'>
      <input type='number' name='cardid' class='form-control' placeholder='Card ID' size='3'>
      <input type='number' name='pick' class='form-control' placeholder='Pick x cards' title='Pick this many white cards when this card is played' size='1' min='1' max='5'>
      <div class='input-group'>
        <input type='text' name='text' class='form-control' placeholder='Card text' size='50'>
        <div class='input-group-btn'><button type='submit' class='btn btn-success'><span class='fa fa-save smgr'></span>Save</button></div>
      </div>
    </form>
    <hr>
    <h4>Tasks</h4>
    <include src='../cfm/todo.html'>
    <hr>
    <sql table='users' order='joined' select='count(*) as users'><SET users='$users'></sql>
    <h4>Users (<output name='users'>)</h4>
    <table class='padcells'>
      <sql table='users' order='joined'>
        <tr>
          <td><output name='ID'></td>
          <td><output name='username'></td>
          <td><output name='forename'> <output name='surname'></td>
          <td><a href='mailto:$email' class='btn btn-primary btn-sm'><span class='fa fa-envelope smgr'></span> <output name='email'></a></td>
          <td><a href='resetpw.cgi?user=$ID' class='btn btn-primary btn-sm'><span class='fa fa-lock smgr'></span> Reset password</a></td>
        </tr>
      </sql>
    </table>
  </IF>
</IF>
<IF ELSE>
  <div class='center'>
    <div class='row'>
      <div class='col-xs-6'>
        <form action='login.cgi' method='post' class='inline'>
          <input type='hidden' name='game' />
          <div class='header'>Login</div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-user'></span></span><input type='text' name='username' class='form-control' placeholder='Username' autofocus ></div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-lock'></span></span><input type='password' name='password' class='form-control' placeholder='Password'></div>
          <button type='submit' class='btn btn-secondary mt-1'><span class='fa fa-sign-in smgr'></span>Login</button>
        </form><IF loginerror><p class='error'>There was an error with your login, please try again</p></IF>
      </div>
      <div class='col-xs-6'>
        <form action='register.cgi'>
          <div class='header'>Register</div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-user'></span></span>
          <input type='text' name='forename' class='form-control' placeholder='Forename'></div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-user'></span></span>
          <input type='text' name='surname' class='form-control' placeholder='Surname'></div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-user'></span></span>
          <input type='text' name='username' class='form-control' placeholder='Username'></div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-lock'></span></span>
          <input type='password' name='password' class='form-control' placeholder='Password'></div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-check'></span></span>
          <input type='password' name='confirm' class='form-control' placeholder='Confirm password'></div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-envelope'></span></span>
          <input type='text' name='email' class='form-control' placeholder='Email'></div>
          <div class='center'><select name='gender' title='Gender'><option value='he'>Male</option><option value='she'>Female</option></select></div>
          <div class='center pad5'><img src='images/code.png' alt='code'></div>
          <div class='input-group'><span class='input-group-addon'><span class='fa fa-qrcode'></span></span>
          <input type='text' name='code' class='form-control' placeholder='Enter code above'></div>
          <button type='submit' class='btn btn-secondary mt-1'><span class='fa fa-plus smgr'></span>Register</button>
        </form><IF regerror><p class='error'>There was an error with your registration, please try again</p></IF>
      </div>
    </div>
  </div>
</IF>
'END'
