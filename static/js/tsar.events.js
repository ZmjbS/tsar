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

/* Add functions that apply to elements on the page */
$(document).ready(function(){

// Serialise the input data and submit the form.
// TODO: It's probably best to use a class to select this rather than have it apply to all forms where this script is included.
		console.log('tsar.events.js read');
	$('form').submit(function() {
		console.log('serialising');
		json = JSON.stringify($(this).serializeJSON());
		csrf = $.cookie('csrftoken');
		console.log('CSRF: '+csrf);
		console.log('JSON: '+json);
		var posting = $.post("/vidburdur/nyskraning/vista", {'csrfmiddlewaretoken': csrf, 'data': json});
		posting.done(function(data) {
			console.log('posting done!');
			response = JSON && JSON.parse(data) || $.parseJSON(data);
			switch (response['type']) {
				case 'success':
					console.log('SUCCESS!!!');
					console.log('response[type]: '+response['type']);
					console.log('response[event_id]: '+response['event_id']);
					location.href = "/vidburdur/"+response['event_id'];
					//print_result('Viðburður númer '+data+' búinn til eða lagaður.','alert-success');
					break;
				case 'error':
					console.log('ERROR.');
					print_result(response['message'], 'alert-error');
					break;
				default:
					console.log('response: '+data);
					console.log('response[type]: '+response['type']);
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
		if (type) {
			//$('#results').removeClass()
			$('#results').addClass('alert '+type)
		}
	}

}); // end document ready
