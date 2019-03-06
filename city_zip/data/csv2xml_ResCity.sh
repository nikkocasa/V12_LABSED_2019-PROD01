#!/bin/bash
# Id Externe,name,INSEE,Area / Id Externe,long,lat,ZIP / Id Externe
# __export__.res_city_fr-00001,AAST,64001,__export__.res_state_area_fr64,-0.0459145851164,43.3625245098,__export__.res_zip_fr-64460

file_in=$1
file_out=$2

echo '<?xml version="1.0" encoding="utf-8"?>' > $file_out
echo '<odoo>' >> $file_out
echo '    <data noupdate="1">' >> $file_out

while IFS=$',' read -r -a arry
do
	echo '        <record id="'${arry[0]}'" model="res.country.state">' >> $file_out
	echo '            <field name="name">'${arry[1]}'</field>' >> $file_out
	echo '            <field name="insee_code">'${arry[2]}'</field>' >> $file_out
	echo '            <field name="area_id">'${arry[3]}'</field>' >> $file_out
	echo '            <field name="long">'${arry[4]}'</field>' >> $file_out
	echo '            <field name="lat">'${arry[5]}'</field>' >> $file_out
	# this is for concataning the zip_ids in a single string with ',' separation
	ids=()
	sep=','

	for (( i=6; i<${#arry[@]}; i++ ));
	do
	        ids+=${arry[$i]} #concataning queue of line 
	        j=$(($i + 1))
	# not finishing line by a sep
	if [[ "$j" -lt "${#arry[@]}"  ]]
	then
	        ids+=$sep
	fi
	done
	#echo $ids
	
	echo '            <field name="zip_ids">'${ids}'</field>' >> $file_out
	echo '        </record>'  >> $file_out
done < $file_in
echo '    </data>'  >> $file_out
echo '</odoo>'  >> $file_out
echo 'Done'
