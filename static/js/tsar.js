/*
 * tsar.js
 * Functions for TSAR: https://github.com/ZmjbS/tsar/
 *
 */

function respond_to_event(button, pagetype) {
	/* The respond_to_event function extracts information about the
	 *  - action being taken (attend, absent, unclea)
	 *  - id of the eventrole to which the response is
	 *  The function takes two arguments:
	 *  - button: The button object from which the response is made (so that we can refer to its attributes), and
	 *  - pagetype: the page type (Event page, My page) so that we can update the structure and styles accordingly.
	 *  */

	/* First a bit of debuggin...
   console.log('responding ----------------------');
	console.log('Page is: '+pagetype);
	console.log('attribute: '+$(button).attr('id'))
	*/

	// extract the action and eventrole from button
	//action = $(button).attr('id').substring(0,6);
	action = $(button).attr('data-action');
	//eventrole = $(button).attr('id').substring(7);
	eventrole = $(button).parent().attr('data-eventrole');

	/* More debug
	*/
	console.log('action: '+action);
	console.log('eventrole: '+eventrole);

	var node='init';

	// Submit the response via an AJAX POST:
   var posting = $.post("/vidburdur/svara", {'action': action, 'eventrole': eventrole, });

	// DEBUG: console.log('after post');

   posting.done(function(data, node) {
		obj = JSON && JSON.parse(data) || $.parseJSON(data);
		/* DEBUG:
		console.log('posting done, let\'s format');
		console.log('Done: received '+obj);
		console.log('User:  '+obj.user_name);
		console.log('User ID:  '+obj.user_id);
		console.log('Username:  '+obj.username);
		console.log('Role ID: '+obj.role_id);
		console.log('action:  '+obj.action);
		*/

		switch ( pagetype ) {
			case "Event page":
				// If the call comes from 'templates/events/event_page.html'

				// Remove the entry from the old list
				$('#role_'+obj.role_id+'_member_'+obj.user_id+'_entry').remove();
				// Add an entry to the new list
				if (action == 'attend') {
					$('#role_'+obj.role_id+'_attending_members').prepend('<li id="role_'+obj.role_id+'_member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'">'+obj.user_name+'</a></li>')
					$('#role_'+obj.role_id+'_status_icon').removeClass('icon-ban-circle');
					$('#role_'+obj.role_id+'_status_icon').addClass('icon-ok-circle');
				} else {
					$('#role_'+obj.role_id+'_absent_members').prepend('<li id="role_'+obj.role_id+'_member_'+obj.user_id+'_entry"><a href="/felagi/'+obj.username+'">'+obj.user_name+'</a></li>')
					$('#role_'+obj.role_id+'_status_icon').removeClass('icon-ok-circle');
					$('#role_'+obj.role_id+'_status_icon').addClass('icon-ban-circle');
				}
				// ==================================================== End of "Event page"
				break;

			case "My page":
				// If the call comes from 'templates/my_page.html'
				//
				// Change the colour of the eventrole status icon -------------------------
				// DEBUG: console.log('Change eventrole status icon colour');
				if (action == 'attend') {
					$('#eventrole_'+obj.eventrole_id+'_status_icon').css('color', 'rgb(70, 136, 71)');
					$('#eventrole_'+obj.eventrole_id+'_status_icon').attr('data-status', 'attending');
				} else {
					$('#eventrole_'+obj.eventrole_id+'_status_icon').css('color', 'rgb(185, 74, 72)');
					$('#eventrole_'+obj.eventrole_id+'_status_icon').attr('data-status', 'absent');
				}

				// Change the colour of the event status icon -----------------------------
				// DEBUG: console.log('Change event status icon colour');
				var eventrole_linodes = $('#eventrole_'+obj.eventrole_id).parent().children();
				if (action == 'attend') {
					$('#eventrole_'+obj.eventrole_id+'_status_icon').parents('.event-list-item').children('.status-icon').css('color', 'rgb(70, 136, 71)');
				} else {
					// Create a set of the eventrole li-objects
					//var eventrole_linodes = $('#eventrole_'+obj.eventrole_id).parent().children();

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
						$('#eventrole_'+obj.eventrole_id+'_status_icon').parents('.event-list-item').children('.status-icon').css('color', 'rgb(185, 74, 72)');
					}
				}

				// Change the eventrole buttons -------------------------------------------
				// DEBUG: console.log('Change eventrole buttons');
				// Remove the old ones
				$('#eventrole_'+obj.eventrole_id+'_response_icons').children().remove();
				// Define the node to add
				if (action == 'attend') {
					node='<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="eventrole-absent-'+eventrole+'" data-action="absent"  class="respond-icon icon-remove-sign"></span>'
						+ '<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="eventrole-unclea-'+eventrole+'" data-action="unclear" class="respond-icon icon-question-sign"></span>';
				} else {
					node='<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="eventrole-unclea-'+eventrole+'" data-action="unclear" class="respond-icon icon-question-sign"></span>'
						+ '<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="eventrole-attend-'+eventrole+'" data-action="attend"  class="respond-icon icon-plus-sign"></span>';
				}
				// Add the new buttons
				$('#eventrole_'+obj.eventrole_id+'_response_icons').append(node);

				// Change the event buttons if there is just one eventrole ----------------
				// DEBUG: console.log(eventrole_linodes);
				if ( eventrole_linodes.length == 1 )
				{
					// Remove the old ones
					$('#eventrole_'+obj.eventrole_id+'_response_icons').parents('.event-list-item').children('.response-icons').children().remove();
					// Define the node to add
					if (action == 'attend') {
						node='<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="absent-'+eventrole+'" data-action="absent"  class="respond-icon icon-remove-sign"></span>'
							+ '<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="unclea-'+eventrole+'" data-action="unclear" class="respond-icon icon-question-sign"></span>';
					} else {
						node='<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="unclea-'+eventrole+'" data-action="unclear" class="respond-icon icon-question-sign"></span>'
							+ '<span onclick="event.stopPropagation(); respond_to_event(this, \'My page\');" id="attend-'+eventrole+'" data-action="attend"  class="respond-icon icon-plus-sign"></span>';
					}
					// Add the new buttons
					$('#eventrole_'+obj.eventrole_id+'_response_icons').parents('.event-list-item').children('.response-icons').append(node);
				}

				// ======================================================= End of "My page"
				break;

		}

     });

   return false;
};
