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

function respond_to_event(button, pagetype) {
	/*
		Submits data to the view to create a MemberResponse.
		
		The function takes two arguments:
		 . button: The object that generates the event, and
		 . pagetype: the page type (Event page, My page) so that we can update the
			structure and styles accordingly.

		From the button, the function extracts information about:
		 . the action being taken (attend, absent, unclear),
		 . the id of the eventrole to which the response is, and
		 . the id of the member whose response is being changed.

		The function then posts this information to the view where the
		MemberResponse is taken care of. Upon success, the function then updates
		the interface, depending on whether the function is called from „my page“
		or the event_page.
	 */

	/* Collect the data on the response */
	action       = $(button).data('action'); // action is either "absent" or "attend"
	member_id    = $(button).data('member_id');
	eventrole_id = $(button).data('eventrole_id');

	// TODO: The following data holders are no longer used for this function and should probably be removed.
	//eventrole_id = $(button).parent().data('eventrole_id');
	//action = $(button).data('action');

	/* DEBUG
  	console.log('responding ----------------------');
	console.log('Page is: '+pagetype);
	console.log('attribute: '+$(button).attr('id'))
	console.log('action: '+action);
	console.log('eventrole ID: '+eventrole_id);
	*/

	// Submit the response via an AJAX POST:
	if (member_id) {
		var posting = $.post("/vidburdur/svara", {'action': action, 'eventrole_id': eventrole_id, 'member_id': member_id });
	} else {
		var posting = $.post("/vidburdur/svara", {'action': action, 'eventrole_id': eventrole_id });
	}
	/* DEBUG:
	console.log('after post');
	*/

   posting.done(function(data) {
		obj = JSON && JSON.parse(data) || $.parseJSON(data);
		console.log('posting done, let\'s format');
		/* DEBUG:
		console.log('Done: received '+obj);
		console.log('User:  '+obj.user_name);
		console.log('User ID:  '+obj.user_id);
		console.log('Username:  '+obj.username);
		console.log('Role ID: '+obj.role_id);
		console.log('action:  '+obj.action);
		*/

		switch ( pagetype ) {
			case "Event page": // ============================== Beginning of "Event page"
				// If the call comes from 'templates/events/event_page.html'

				// Remove the entry from the old list
				$('#role_'+obj.role_id+'_member_'+obj.user_id+'_entry').remove();
				// Add an entry to the new list
				if (action == 'attend') {
				   $('#role_'+obj.role_id+'_attending_members').prepend('<li id="role_'+obj.role_id+'_member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'" title="'+obj.time_responded+'">'+obj.user_name+'</a><span class="event_responder attending edit-interface fa fa-times-circle pull-right" data-member_id="'+obj.user_id+'" data-eventrole_id="'+obj.eventrole_id+'" data-action="absent" data-status="attending"></span></li>')
					if ($('#attending_roles').siblings('.form-edit-icon').data('toggle_state') == 'hidden') {
						$('#role_'+obj.role_id+'_member_'+obj.user_id+'_entry').children('.event_responder.edit-interface').css('display','none');
					}
					// If we're changing the currently logged in member response, then change the status icon.
					if (obj.cm_responding) {
						$('.role_'+obj.role_id+'_status_icon').removeClass('fa-ban-circle fa-circle-blank invited');
						$('.role_'+obj.role_id+'_status_icon').addClass('fa-ok-circle');
					}
				} else {
				   $('#role_'+obj.role_id+'_absent_members').prepend('<li id="role_'+obj.role_id+'_member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'" title="'+obj.time_responded+'">'+obj.user_name+'</a><span class="event_responder absent edit-interface fa fa-plus-circle pull-right" data-member_id="'+obj.user_id+'" data-eventrole_id="'+obj.eventrole_id+'" data-action="attend" data-status="absent"></span></li></li>')
					if ($('#absent_roles').siblings('.form-edit-icon').data('toggle_state') == 'hidden') {
						$('#role_'+obj.role_id+'_member_'+obj.user_id+'_entry').children('.event_responder.edit-interface').css('display','none');
					}
					// If we're changing the currently logged in member response, then change the status icon.
					if (obj.cm_responding) {
						$('.role_'+obj.role_id+'_status_icon').removeClass('fa-ok-circle fa-circle-blank invited');
						$('.role_'+obj.role_id+'_status_icon').addClass('fa-ban-circle');
					}
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

				// Fix the button current status:
				switch (action) {
					case 'attend':
						$('.event_responder').data('status','attending');
						break;
					case 'absent':
						$('.event_responder').data('status','absent');
						break;
				}

				// ==================================================== End of "Event page"
				break;

			case "My page": // ===================================== Beginning of My page"
				// If the call comes from 'templates/my_page.html'
				//
				// Change the colour of the eventrole status icon -------------------------
				// console.log('Change eventrole status icon colour');
				if (action == 'attend') {
					$('#eventrole_'+obj.eventrole_id+'_status_icon').removeClass('absent unclear').addClass('attending');
					$('#eventrole_'+obj.eventrole_id+'_status_icon').attr('data-status', 'attending');
				} else {
					$('#eventrole_'+obj.eventrole_id+'_status_icon').removeClass('attending unclear').addClass('absent');
					$('#eventrole_'+obj.eventrole_id+'_status_icon').attr('data-status', 'absent');
				}

				// Change the colour of the event status icon -----------------------------
				// DEBUG: console.log('Change event status icon colour');
				// Create a set of the eventrole li-objects
				var eventrole_linodes = $('#eventrole_'+obj.eventrole_id).parent().children();
				if (action == 'attend') {
					$('#eventrole_'+obj.eventrole_id+'_status_icon').parents('.event-list-item').children('.status-icon').removeClass('absent unclear').addClass('attending');
				} else {
					// Check whether the user is absent from all eventroles.
					// First, assume that this is true:
					var absent_from_all = true
					// Then iterate over the eventroles and see if we're attending any:
					for (var i = 0; i < eventrole_linodes.length; i++)
					{
						// DEBUG: console.log(i+' '+$(eventrole_linodes[i]).children('.status-icon').attr('status'));
						if ( $(eventrole_linodes[i]).children('.status-icon').attr('data-status') == 'attending' )
						{
							absent_from_all = false;
							// DEBUG: console.log('Attending at least one');
							break;
						}
					}
					// If the user is absent from all eventroles, turn the status-icon red
					if ( absent_from_all )
					{
						$('#eventrole_'+obj.eventrole_id+'_status_icon').parents('.event-list-item').children('.status-icon').removeClass('attending unclear').addClass('absent');
					}
				}

				// Change the eventrole buttons -------------------------------------------
				// Here we just change the data-action attribute but leave the buttons alone.
				// DEBUG:
				console.log('Change eventrole buttons');
				if (action == 'attend') {
					/*
					 * If we're attending, then change the attend button action to
					 * 'none' and the absent button action to 'absent'.
					 */
					if ( eventrole_linodes.length == 1 )
					{
						// If there is only one eventrole, then we also have to change the event buttons.
						$('#event-eventrole-'+eventrole_id+'-attend_button').data('action','none').removeClass('active').addClass('inactive');
						$('#event-eventrole-'+eventrole_id+'-absent_button').data('action','absent').removeClass('inactive').addClass('active');
					}
					$('#eventrole-'+eventrole_id+'-attend_button').data('action','none').removeClass('active').addClass('inactive');
					$('#eventrole-'+eventrole_id+'-absent_button').data('action','absent').removeClass('inactive').addClass('active');
				} else {
					/*
					 * Else we're absent. In that case we change the attend button
					 * action to 'attend' and the absent button action to 'none'.
					 */
					if ( eventrole_linodes.length == 1 )
					{
						$('#event-eventrole-'+eventrole_id+'-attend_button').data('action','attend').removeClass('inactive').addClass('active');
						$('#event-eventrole-'+eventrole_id+'-absent_button').data('action','none').removeClass('active').addClass('inactive');
					}
					$('#eventrole-'+eventrole_id+'-attend_button').data('action','attend').removeClass('inactive').addClass('active');
					$('#eventrole-'+eventrole_id+'-absent_button').data('action','none').removeClass('active').addClass('inactive');
				}

				// ======================================================= End of "My page"
				break;

		} // switch ( pagetype )

	}); // posting.done()

   return false;
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
