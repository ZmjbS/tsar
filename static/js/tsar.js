/*
 * tsar.js
 * Functions for TSAR: https://github.com/ZmjbS/tsar/
 *
 */

/*
 * Serialises the input data and submits it to the response view which updates the MemberResponse.
 */
   $('.respond').live('click',(function() {
      console.log('responding');
		$('#response').html('Responding');
		console.log('attribute: '+$(this).attr('id'))
		action = $(this).attr('id').substring(0,6);
		eventrole = $(this).attr('id').substring(7);
		console.log('action: '+action);
		console.log('eventrole: '+eventrole);
      var posting = $.post("svara", {'action': action, 'eventrole': eventrole, });
		console.log('posted');
		object = this;
      posting.done(function(data) {
			//obj = JSON.parse(data);
			obj = JSON && JSON.parse(data) || $.parseJSON(data);
			console.log('Done: received '+obj);
			//console.log('User ID: '+obj.user_id);
			console.log('User:  '+obj.user_name);
			console.log('User ID:  '+obj.user_id);
			console.log('Username:  '+obj.username);
			console.log('Role ID: '+obj.role_id);
			console.log('action:  '+obj.action);
			// Remove the entry from the old list
			$('#member_'+obj.user_id+'_entry').remove();
			// Add an entry to the new list
			if (action == 'attend') {
				$('#attending_members').prepend('<li id="member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'">'+obj.user_name+'</a> <span id="absent-'+obj.event_role_id+'" class="respond icon-remove-sign edit-icon"></span> <span id="unclea-'+obj.role_id+'" class="respond icon-question-sign edit-icon"></span> </li>')
			} else {
				$('#absent_members').prepend('<li id="member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'">'+obj.user_name+'</a> <span id="unclea-'+obj.event_role_id+'" class="respond icon-question-sign edit-icon"></span> <span id="attend-'+obj.role_id+'" class="respond icon-plus-sign edit-icon"></span> </li>')
			}
			//console.log('Object: '+object);
			//console.log('Now let us delete '+$(object).attr('id'));
		/* TODO: Here we should somehow pass data back to the caller so that the display can be updated; attending members added to the attendance list, absent members to the absent list, uncertain back to the uncertain list, and in all cases the member removed from where they were.
 *  .... or maybe just stay there, but update the look (so that one can more easily undo that action). */
         //if (isNaN(parseInt(data))) {
          //  alert('jei!');
//print_result('Error: '+data,'alert-error');
        // } else {
          //  $('#event_id').val(data);
 //           print_result('Viðburður númer '+data+' búinn til. Sjá <a href="/vidburdur/'+data+'">síðu viðburðarins</a>','alert-success');
			//	alert('action taken')
        });
		$('#response').html('Don3!');
      return false;
   }));

