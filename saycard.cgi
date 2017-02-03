#!/projects/tools/bin/envcgi /bin/csh -f
set noglob

if(! $?ID) then
  setenv ID "$PATH_INFO:t"
endif

setenv cards `sql -d cah 'SELECT COUNT(*) FROM cards WHERE ID="$ID"'`

if(! -e "sounds/${ID}.${type}" && "$cards" == 1) then
  setenv text `sql -d cah 'SELECT text FROM cards WHERE ID="$ID"'`
  setenv text `echo "$text" | sed 's/"//g' | sed 's/\\!//g' | sed -r 's/(_+)/blank/g'`
  echo "$text" | text2wave > "sounds/${ID}.wav"
  ffmpeg -i "sounds/${ID}.wav" -acodec libvorbis "sounds/${ID}.ogg"
  ffmpeg -i "sounds/${ID}.wav" -acodec libmp3lame "sounds/${ID}.mp3"
endif
echo "Location: sounds/${ID}.${type}"
echo ""

