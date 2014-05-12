#!bin/bash

membership=1
GroupNum=23

function assign_group() {
# We want to assign group numbers but with different probabilities:
# Bækistöðvarhópur		8
	group[1]=8
# Tölvuhópur				3
	group[2]=3
# Bílahópur					33
	group[3]=33
# Búðahópur					26
	group[4]=26
# Eftirbátar				19
	group[5]=19
# Léttsveit					26
	group[6]=26
# Fjallahópur				52
	group[7]=52
# Leitarhundar				3
	group[8]=3
# Leitartæknihópur		46
	group[9]=46
# Sjúkrahópur				41
	group[10]=41
# Sleðahópur				14
	group[11]=14
# Snjóbílshópur			12
	group[12]=12
# Stjórn					7
	group[13]=7
# Undanfarar				18
	group[14]=18
# Vélhjólahópur			4
	group[15]=4
# Þriðja bylgjan			68
	group[16]=68
# #17
	group[17]=0
# Fótboltahópur			19
	group[18]=19
# Flugeldanefnd			10
	group[19]=10
# Húsnæðisnefnd			4
	group[20]=4
# Hengilsnefnd			4
	group[21]=4
# Nýliðar					20
	group[22]=20
# Vinnuhópur				224
#	group[23]=224

	total=0
	for num in ${!group[@]}
	do 
		let "total+=${group[$num]}"
		membership[$num]=$total
		#echo $total
	done
	#echo $total

	r=$RANDOM
	#echo $r
	let "r%=$total"
	#echo $r

	if ((0<$r && $r<=${membership[1]}))
	then
		echo 1
	elif ((${membership[1]}<$r && $r<=${membership[2]}))
	then
		echo 2
	elif ((${membership[2]}<$r && $r<=${membership[3]}))
	then
		echo 3
	elif ((${membership[3]}<$r && $r<=${membership[4]}))
	then
		echo 4
	elif ((${membership[4]}<$r && $r<=${membership[5]}))
	then
		echo 5
	elif ((${membership[5]}<$r && $r<=${membership[6]}))
	then
		echo 6
	elif ((${membership[6]}<$r && $r<=${membership[7]}))
	then
		echo 7
	elif ((${membership[7]}<$r && $r<=${membership[8]}))
	then
		echo 8
	elif ((${membership[8]}<$r && $r<=${membership[9]}))
	then
		echo 9
	elif ((${membership[9]}<$r && $r<=${membership[10]}))
	then
		echo 10
	elif ((${membership[10]}<$r && $r<=${membership[11]}))
	then
		echo 11
	elif ((${membership[11]}<$r && $r<=${membership[12]}))
	then
		echo 12
	elif ((${membership[12]}<$r && $r<=${membership[13]}))
	then
		echo 13
	elif ((${membership[13]}<$r && $r<=${membership[14]}))
	then
		echo 14
	elif ((${membership[14]}<$r && $r<=${membership[15]}))
	then
		echo 15
	elif ((${membership[15]}<$r && $r<=${membership[16]}))
	then
		echo 16
	elif ((${membership[16]}<$r && $r<=${membership[17]}))
	then
		echo 17
	elif ((${membership[17]}<$r && $r<=${membership[18]}))
	then
		echo 18
	elif ((${membership[18]}<$r && $r<=${membership[19]}))
	then
		echo 19
	elif ((${membership[19]}<$r && $r<=${membership[20]}))
	then
		echo 20
	elif ((${membership[20]}<$r && $r<=${membership[21]}))
	then
		echo 21
	elif ((${membership[21]}<$r && $r<=${membership[22]}))
	then
		echo 22
#	elif ((${membership[22]}<$r && $r<=${membership[23]}))
#	then
#		echo 23
	fi

}

echo '['

# Generates a total of 100 memberships with various numbers of group memberships.
membership_num=1
for ((member=1;$member<=10;member++))
do
	group_list=()
	# Ten members with four groups
	for ((i=1;$i<=4;i++))
	do
		until [[ ! ${group_list[@]} =~ $group_num ]]
		do
			group_num=$(assign_group)
		done
	#	echo "group num "$group_num
		group_list=("${group_list[@]}" "$group_num")
	#	echo "group list "${group_list[@]}

		#echo $member $i $membership_num $group_num
		echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": '$group_num', "is_manager": false, "date_joined": "2013-08-14"}}',
		let "membership_num+=1"
	done
	echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": 23, "is_manager": false, "date_joined": "2013-08-14"}}',
	let "membership_num+=1"
done
for ((member=11;$member<=20;member++))
do {
	group_list=()
	# Ten members with three groups
	for ((i=1;$i<=3;i++))
	do { 
		until [[ ! ${group_list[@]} =~ $group_num ]]
		do
			group_num=$(assign_group)
		done
		group_list=("${group_list[@]}" "$group_num")
		echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": '$group_num', "is_manager": false, "date_joined": "2013-08-14"}}',
		let "membership_num+=1"
	} done
	echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": 23, "is_manager": false, "date_joined": "2013-08-14"}}',
	let "membership_num+=1"
} done
for ((member=21;$member<=40;member++))
do {
	group_list=()
	# Twenty members with two groups
	for ((i=1;$i<=2;i++))
	do { 
		until [[ ! ${group_list[@]} =~ $group_num ]]
		do
			group_num=$(assign_group)
		done
		group_list=("${group_list[@]}" "$group_num")
		echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": '$group_num', "is_manager": false, "date_joined": "2013-08-14"}}',
		let "membership_num+=1"
	} done
	echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": 23, "is_manager": false, "date_joined": "2013-08-14"}}',
	let "membership_num+=1"
} done
for ((member=41;$member<=100;member++))
do {
	# Sixty members with one group
	group_num=$(assign_group)
	echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": '$group_num', "is_manager": false, "date_joined": "2013-08-14"}}',
	let "membership_num+=1"
	echo '{"pk": '$membership_num', "model": "groups.membership", "fields": {"member": '$member', "group": 23, "is_manager": false, "date_joined": "2013-08-14"}}',
	let "membership_num+=1"
} done

echo ']'
