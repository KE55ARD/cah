#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
setenv existing `sql -d cah 'SELECT COUNT(*) FROM users WHERE username="$username"' OR email="$email"`
if("$password" == "$confirm" && ("$code" == "1ddf2556" || "$code" == "1DdF2556") && "$existing" == 0) then
  sql -d cah 'INSERT INTO users (username,password,forename,surname,email,gender,joined) values ("$username",password("$password"),"$forename","$surname","$email","$gender",now())'
  echo "Location: login.cgi?username=$username&password=$password"
  echo ""
else
  echo "Location: index.cgi?ERROR=Oops,%20something%20went%20wrong,%20please%20try%20again"
  echo ""
endif
