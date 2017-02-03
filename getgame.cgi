#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
unsetenv usertype
if($?HTTP_SESSION) then
setenv usertype `sql -d cah 'SELECT user FROM users WHERE session="$HTTP_SESSION"'`
if("$usertype" == "") unsetenv usertype
setenv userid `sql -d cah 'SELECT ID FROM users WHERE session="$HTTP_SESSION"'`
setenv refresh `sql -d cah 'SELECT refresh FROM users WHERE session="$HTTP_SESSION"'`
endif
# --------------------------------------------------------------------------------
if(! $?usertype || `sql -d cah 'SELECT COUNT(*) FROM invites WHERE game="$game" AND user="$userid"'` != 1) then
  echo "Location: index.cgi?ERROR=You%20are%20not%20logged%20in"
  echo ""
  exit 0
endif

if(! $?chatlimit) then
  setenv chatlimit "20"
endif

echo "Cache-Control: private"
xmlsql -d cah --smiley=smiley --xml << 'END'
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xml>

  <sql table='deck' where='state!="deck" AND state!="used" AND state!="won" AND game="$game" AND colour="white"' select='count(*) as whites'><SET whites='$whites'></sql>
  <sql table='deck' where='state!="deck" AND state!="used" AND state!="won" AND game="$game" AND colour="black"' select='count(*) as blacks'><SET blacks='$blacks'></sql>
  <sql table='deck' where='state="inhand" AND game="$game" AND user="$userid"' select='count(*) as myhand'><SET myhand='$myhand'></sql>
  <sql table='deck' where='state="inhand" AND game="$game"' select='count(*) as inhand'><SET inhand='$inhand'></sql>
  <sql table='deck' where='state="inplay" AND game="$game"' select='count(*) as inplay'><SET inplay='$inplay'></sql>
  <sql table='deck' where='state="deck" AND game="$game"' select='count(*) as deck'><SET deck='$deck'></sql>
  <sql table='deck' where='colour="black" AND state="inplay" AND game="$game"'><SET blackcard='$card'></sql>
  <sql table='cards' where='ID="$blackcard"'><SET pick='$pick'></sql>
  <sql table='invites' where='game="$game"' select='count(*) as invites'><SET invites='$invites'></sql>
  <sql table='games' where='ID="$game"'><SET turn='$turn'>
  <gamestatus owner='$owner' blacks='$blacks' whites='$whites' myhand='$myhand' inhand='$inhand' inplay='$inplay' deck='$deck' turn='$turn' blackcard='$blackcard' pick='$pick' limit='$cards' invites='$invites' refresh='$refresh'><output name='title'></gamestatus>
  </sql>

  <sql table='invites left join users on invites.user=users.ID' where='game="$game"' order='sent'>
    <IF turn='$user'><SET myturn='true'></IF><IF ELSE><SET myturn='false'></IF>
    <sql table='deck' where='user="$user" AND state="won" AND game="$game"' select='count(distinct won) as won'><SET won='$won'></sql>
    <invite ID="$ID" user="$user" myturn='$myturn' won='$won'><![CDATA[<output name='username'>]]></invite>
  </sql>

  <blackcard>
    <sql table='deck left join cards on deck.card=cards.ID' where='game="$game" AND deck.colour="black" AND state="inplay"'>
      <include src='card.html'>
    </sql>
  </blackcard>

  <whitecards>
    <sql table='deck left join cards on deck.card=cards.ID' where='game="$game" AND state="inplay" AND deck.colour="white"' order='user, selected'>
      <include src='card.html'>
    </sql>
  </whitecards>

  <mycards>
    <sql table='deck left join cards on deck.card=cards.ID' where='game="$game" AND user="$userid" AND (state="inhand" OR state="played") AND deck.colour="white"' order='selected desc'>
      <include src='card.html'>
    </sql>
  </mycards>

  <sql table='chat left join users on chat.user=users.ID' where='game="$game"' limit='$chatlimit' order='sent desc'>
    <msg ID="$ID" user='$user' username='$username'><![CDATA[<output name='msg' type='safemarkup'>]]></msg>
    <sent><![CDATA[<output name='sent' type='age'> ago]]></sent>
  </sql>

</xml>
'END'
else
  echo "Status: 404"
  echo ""
  exit 0
endif
