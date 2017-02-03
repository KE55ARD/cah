#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
if(`sql -d cah 'SELECT COUNT(*) FROM users WHERE username="$username" AND password=password("$password")'` != 0) then
 sql -d cah 'UPDATE users SET session="$HTTP_SESSION" WHERE username="$username"'
endif
if($?game) then
  if("$game" != "") then
    echo "Location: game.cgi?game=$game"
  else
    echo "Location: play.cgi"
  endif
else
  echo "Location: play.cgi"
endif
echo ""
