/*
 * tsar.events.js
 * Functions for the TSAR events module: https://github.com/ZmjbS/tsar/
 *
 */

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
			if (isNaN(parseInt(data))) {
				$('#event_id').val(data);
				print_result('Error: '+data,'alert-error');
			} else {
				console.log('Is a number. Redirecting...');
				location.href = "/vidburdur/"+data;
		//		print_result('Viðburður númer '+data+' búinn til. Sjá <a href="/vidburdur/'+data+'">síðu viðburðarins</a>','alert-success');
			}
		})
		.fail(function() { console.log("error"); })
		.always(function() { console.log("finished"); });
		return false;
	});

}); // end document ready
