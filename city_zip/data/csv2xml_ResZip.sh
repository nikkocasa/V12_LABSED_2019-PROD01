#!/bin/bash
# id,name,zip_format,zip_country/id
# __export__.res_zip_fr-01000,01000,'00000’,base.fr

file_in=$1
file_out=$2

echo '<?xml version="1.0" encoding="utf-8"?>' > $file_out
echo '<odoo>' >> $file_out
echo '    <data noupdate="1">' >> $file_out

while IFS=$',' read -r -a arry
do
	echo '        <record id="'${arry[0]}'" model="res.country.state">' >> $file_out
	echo '            <field name="name">'${arry[1]}'</field>' >> $file_out
	echo '            <field name="zip_format">'${arry[2]}'</field>' >> $file_out
	echo '            <field name="zip">'${arry[3]}'</field>' >> $file_out
	echo '            <field name="country_id">'${arry[4]}'</field>' >> $file_out
	echo '        </record>'  >> $file_out
done < $file_in
echo '    </data>'  >> $file_out
echo '</odoo>'  >> $file_out
echo 'Done'
