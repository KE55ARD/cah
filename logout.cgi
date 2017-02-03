#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
sql -d cah 'UPDATE users SET session="" WHERE session="$HTTP_SESSION"'
echo "Location: index.cgi?game=$game"
echo ""
