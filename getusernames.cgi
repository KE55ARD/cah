#!/projects/tools/bin/envcgi /bin/csh -f
set noglob
# --------------------------------------------------------------------------------
source auth.cgi
if($status) exit $status
# --------------------------------------------------------------------------------

echo "Cache-Control: private"
echo "Content-Type: application/json"
echo ""
xmlsql -d cah --xml << 'END' | axl --json-out -
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xml>
  <sql table='users' where='username like "${search}%"' limit='5' order='username'>
    <field><![CDATA[<output name='username'>]]></field>
  </sql>
</xml>
'END'
