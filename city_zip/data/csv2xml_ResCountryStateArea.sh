#!/bin/bash
# id,area_code,name,state_id/id
# __export__.res_state_area_fr01,01,Ain,__export__.res_state_fr01

file_in=$1
file_out=$2

echo '<?xml version="1.0" encoding="utf-8"?>' > $file_out
echo '<odoo>' >> $file_out
echo '    <data noupdate="1">' >> $file_out

while IFS=$',' read -r -a arry
do
	echo '        <record id="'${arry[0]}'" model="res.country.state">' >> $file_out
	echo '            <field name="code">'${arry[1]}'</field>' >> $file_out
	echo '            <field name="name">'${arry[2]}'</field>' >> $file_out
	echo '            <field name="state_id">'${arry[3]}'</field>' >> $file_out
	echo '        </record>'  >> $file_out
done < $file_in
echo '    </data>'  >> $file_out
echo '</odoo>'  >> $file_out
echo 'Done'
