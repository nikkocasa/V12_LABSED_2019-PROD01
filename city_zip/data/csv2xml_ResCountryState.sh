#!/bin/bash
#"id","code","name","country_id/id"
#"__export__.res_state_fr01","FR-ARA ","Auvergne-Rhône-Alpes","base.fr" 
f_in=$1
out=$2
#echo '<?xml version="1.0"?>' > $file_out
#echo '<Customers>' >> $file_out
#while IFS=$',' read -r -a arry
#do
#  echo '  <Customer>' >> $file_out
#  echo '    <Name>'${arry[0]}'</Name>' >> $file_out
#  echo '    <Age>'${arry[1]}'</Age>' >> $file_out
#  echo '    <Country>'${arry[2]}'</Country>' >> $file_out
#  echo '  </Customer>' >> $file_out
#done < $file_in
#echo '</Customers>' >> $file_out


echo '<?xml version="1.0" encoding="utf-8"?>' > $out
echo '<odoo>' >> $out
echo '    <data noupdate="1">' >> $out
while IFS=$',' read -r -a arry
do
echo '        <record id="'${arry[0]}'" model="res.country.state">' >> $out
echo '            <field name="code">'${arry[1]}'</field>' >> $out
echo '            <field name="name">'${arry[2]}'</field>' >> $out
echo '            <field name="country_id">'${arry[3]}'</field>' >> $out
echo '        </record>'  >> $out
done < $f_in
echo '    </data>'  >> $out
echo '</odoo>'  >> $out
echo 'Done'
