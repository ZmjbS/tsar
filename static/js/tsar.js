/*
 * tsar.js
 * Functions for TSAR: https://github.com/ZmjbS/tsar/
 *
 */


function checkin(button, pagetype) {

	action = $(button).data('action');
	member_id = $(button).data('member');
	event_id = $(button).data('eventid');
	role_id = $(button).data('roleid');
	event_role_id = $(button).data('eventroleid');

	//eventrole = $(button).attr('id').substring(7);
	/*
	console.log('action: '+action);
	console.log('eventrole: '+eventrole);
	console.log($(button).parent().data('eventrole'));*/
	console.log('before init');
	var node='init';
	console.log('before post');
	// Submit the response via an AJAX POST:
   	var posting = $.post("/checkin/add", {'action': action, 'member_id': member_id, 'event_id': event_id, 'role_id': role_id, 'event_role_id': event_role_id,});


	console.log('after post');

    posting.done(function(data, node) {
		obj = JSON && JSON.parse(data) || $.parseJSON(data);

		action_r = obj.action_r
		//eventrole = $(button).attr('id').substring(7);
		//eventrole = $(button).parent().data('eventrole');

		console.log('responding ----------------------');
		console.log('Page is: '+action_r);

		switch ( pagetype ) {
			case "Checkin":
				if (action == 'attend') {
					$('#event_'+$(button).attr('id')+'_status_icon').css('color', 'rgb(70, 136, 71)');
				};
			break;
		}
	});
	return false;
};
