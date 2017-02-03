#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
source auth.cgi
if($status) exit $status
# --------------------------------------------------------------------------------

#Check the user is logged in
if("$usertype" != "admin") then
  echo "Location: index.cgi?ERROR=You are not allowed to do that"
  echo ""
  exit 0
endif

echo "Cache-Control: private"
echo "Content-Type: application/json"
echo ""
xmlsql -d logbook --smiley=smiley --xml << 'END' | axl --json-out -
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xml>
  <sql table='todo' select='distinct site' where='site like "${search}%"' limit='5' order='site'>
    <field><![CDATA[<output name='site'>]]></field>
  </sql>
</xml>
'END'
