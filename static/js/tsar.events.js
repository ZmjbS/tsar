/*
 * tsar.events.js
 * Functions for the TSAR events module: https://github.com/ZmjbS/tsar/
 *
 */

	$('.delete-role-entry').live('click',(function(){
		role_id = $(this).attr('id');
		role_title = $(this).parents('.role_entry').find('.role_entry-title').html();
		$(this).parents('.role_entry').fadeOut(300).slideUp({ duration: 500, queue: false });
		$(this).parents('.role_entry').remove();
		$('#role-dropdown').append('<li id="'+role_id+'" class="role-dropdown-item"><a>'+role_title+'</a></li>');
	}));

function change_event_response(button) {
	/*
		Changes the response of a user.

		The responses (attending, absent and unclear) can be changed
		(to attending or absent) by activating the edit interface. That
		pops up small icons to click on to change the response.

		This function does the dirty work of passing the information on
		to the view for processing and updating the interface so that
		all the numbers add up and the members lists are correct.
	*/

	/* Collect the data on the response */
	member_id    = $(button).data('member_id');
	eventrole_id = $(button).data('eventrole_id');
	action       = $(button).data('action'); // action is either "absent" or "attend"

	/* DEBUG
	console.log('member_id:    '+member_id);
	console.log('eventrole_id: '+eventrole_id);
	console.log('action:       '+action);
	*/

	/* DEBUG
	console.log('posting');
	*/

	// Begin by posting the information to the view:
	var posting = $.post("/vidburdur/svaranytt", {'member_id': member_id, 'eventrole_id': eventrole_id, 'action': action, });
	/* DEBUG
	console.log('posted');
	*/

	// With the posting done, let's update the interface:
	posting.done(function(data, node) {
		/* DEBUG
		console.log('posting done:');
		*/

		// Retrieve the data object from the view:
		obj = JSON && JSON.parse(data) || $.parseJSON(data);

		// Remove the entry from the old list
		$('#role_'+obj.role_id+'_member_'+obj.user_id+'_entry').remove();

		// Add an entry to the new list
		switch (action) {
			case 'attend':
				$('#role_'+obj.role_id+'_attending_members').prepend('<li id="role_'+obj.role_id+'_member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'">'+obj.user_name+'</a><span class="change-response attending edit-interface icon-remove-sign pull-right" data-member_id="'+obj.user_id+'" data-eventrole_id="'+obj.eventrole_id+'" data-action="absent" data-status="attending"></span></li>')
				if ($('#attending_roles').siblings('.form-edit-icon').data('toggle_state') == 'hidden') {
					$('#role_'+obj.role_id+'_member_'+obj.user_id+'_entry').children('.change-response.edit-interface').css('display','none');
				}
// TODO: Update the attendance icons if the response belongs to the current member
//			$('.role_'+obj.role_id+'_status_icon').removeClass('icon-ban-circle icon-circle-blank invited');
//			$('.role_'+obj.role_id+'_status_icon').addClass('icon-ok-circle');
				break;
			case 'absent':
				$('#role_'+obj.role_id+'_absent_members').prepend('<li id="role_'+obj.role_id+'_member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'">'+obj.user_name+'</a><span class="change-response absent edit-interface icon-plus-sign pull-right" data-member_id="'+obj.user_id+'" data-eventrole_id="'+obj.eventrole_id+'" data-action="attend" data-status="absent"></span></li></li>')
				if ($('#absent_roles').siblings('.form-edit-icon').data('toggle_state') == 'hidden') {
					$('#role_'+obj.role_id+'_member_'+obj.user_id+'_entry').children('.change-response.edit-interface').css('display','none');
				}
// TODO: Update the attendance icons if the response belongs to the current member
//			$('.role_'+obj.role_id+'_status_icon').removeClass('icon-ok-circle icon-circle-blank invited');
//			$('.role_'+obj.role_id+'_status_icon').addClass('icon-ban-circle');
				break;
		}
		
		// Fix the total number of attendees.
		status=$(button).data('status');
		console.log(status);
		$('#total_'+status).text(parseInt($('#total_'+status).text()-1));

		switch (action) {
			case 'attend':
				number=parseInt($('#total_attending').text());
				number++
				$('#total_attending').text(number);
				break;
			case 'absent':
				number=parseInt($('#total_absent').text());
				number++
				$('#total_absent').text(number);
				break;
		}
		

	});

};

/* Add functions that apply to elements on the page */
$(document).ready(function(){

	// Serialise the input data and submit the form.
	// TODO: It's probably best to use a class to select this rather than have it apply to all forms where this script is included.
	console.log('tsar.events.js read');
	$('form').submit(function() {
		/*
			This function submits events to the events view for creation.
		*/
		/* DEBUG
		console.log('serialising');
		*/
		json = JSON.stringify($(this).serializeJSON());
		csrf = $.cookie('csrftoken');
		/* DEBUG
		console.log('CSRF: '+csrf);
		console.log('JSON: '+json);
		*/

		// Post the data
		var posting = $.post("/vidburdur/nyskraning/vista", {'csrfmiddlewaretoken': csrf, 'data': json});
		posting.done(function(data) {
			/* DEBUG
			console.log('posting done!');
			*/
			// Retrieve the response from the view.
			response = JSON && JSON.parse(data) || $.parseJSON(data);
			console.log(response);
			switch (response['type']) {
				case 'success':
					// if successful, change the location to the event URI:
					/* DEBUG
					console.log('SUCCESS!!!');
					console.log('response[type]: '+response['type']);
					console.log('response[event_id]: '+response['event_id']);
					*/
					location.href = "/vidburdur/"+response['event_id'];
					break;
				case 'error':
					// if there was an error, print the result.
					/* DEBUG
					*/
					console.log('ERROR.');
					print_result(response['message'], 'alert-danger');
					break;
				default:
					// This should never happen...
					/* DEBUG
					console.log('response: '+data);
					console.log('response[type]: '+response['type']);
					*/
					print_result('Unfamiliar response: '+response['type']+'. Message: '+response['message'], 'alert-error');
					break;
			}
		})
		.fail(function() { console.log("error"); })
		.always(function() { console.log("finished"); });
		return false;
	});

	function print_result(message,type){
		$('#results').slideDown()
		$('#results').html(message)
		console.log(type);
		// Now change the style accordingly:
		if (type) {
			$('#results').addClass(type)
		}
	}

}); // end document ready
