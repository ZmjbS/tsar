/*
 * tsar.groups.js
 * Functions for the TSAR groups module: https://github.com/ZmjbS/tsar/
 *
 */

/* Add functions that apply to elements on the page */
$(document).ready(function(){

	console.log('tsar.groups.js read');
	/*
	 * Serialise the input data and submit the form.
 	 * We need to pass the group_id and a list of member_id's
 	 */
// TODO: It's probably best to use a class to select this rather than have it apply to all forms where this script is included.
	$('form').submit(function() {
		console.log('serialising');
		json = JSON.stringify($(this).serializeJSON());
		csrf = $.cookie('csrftoken');
		console.log('CSRF: '+csrf);
		console.log('JSON: '+json);
		var posting = $.post("/hopur/vista", {'csrfmiddlewaretoken': csrf, 'data': json});
		posting.done(function(data) {
			console.log('posting done!');
			response = JSON && JSON.parse(data) || $.parseJSON(data);
			switch (response['type']) {
				case 'success':
					console.log('SUCCESS!!!');
					console.log('response[type]: '+response['type']);
					//print_result('Hópurinn hefur verið uppfærður','alert-success');
					// For each recently saved entry, remove the unsaved_entry class and mark the hidden input as a member.
					$.each($('.unsaved_entry'), function() {
						console.log($(this).children('.member_name').children('a').text());
						$(this).removeClass('unsaved_entry');
						$(this).children('.member_name').children('input').val('member');
					});
					// Remove all removed entries.
					$.each($('.removed_entry'), function() {
						console.log($(this).children('.member_name').children('a').text());
						$(this).remove();
					});
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
