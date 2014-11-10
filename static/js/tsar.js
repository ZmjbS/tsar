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
					$('#event_'+$(button).attr('id')+'_status_icon').removeClass('fa-circle');
					$('#event_'+$(button).attr('id')+'_status_icon').addClass('fa-check-square');

					//$('#testaa').show();
					$('#e_'+$(button).attr('id')).show();
					$(button).data("action", "checkout");
					$('#'+$(button).attr('id')).removeClass('fa-sign-in');
					$('#'+$(button).attr('id')).addClass('fa-sign-out');
				};

				if (action == 'checkout') {
					$('#'+$(button).attr('id')).hide();
					$('#event_'+$(button).attr('id')+'_status_icon').css('color', 'red');
				};
			break;
		}
	});
	return false;
};

function getnews(sel, url, num) {
	/* Takes three arguments:
	 *   sel - the selector where the unordered list of items should be added
	 *   url - the URL of the RSS stream
	 *   num - the number of news items that should be returned (optional)
	 */
	num = typeof num !== 'undefined' ? num : 8;
	var newsdata = $.get("/news/", { url: url, num: num, }, function(data) {
		obj = JSON && JSON.parse(data) || $.parseJSON(data);
		console.log( "success"+data);
		console.log(obj);
		console.log( "success"+obj[0].title);
		list = ""
		for (count in obj) {
			entry = obj[count]
			console.log(entry.title)
			list = list+'<li><a href="'+ entry.link +'">'+ entry.title +'</a> <time datetime="'+entry.published+'">'+ entry.published_parsed +'</time></li>';
		}
		$(sel).html('<ul>'+list+'</ul>');
		})
		.done(function() {
			console.log( "second success" );
		})
		.fail(function() {
			console.log( "error" );
		})
		.always(function(data) {
			obj = JSON && JSON.parse(data) || $.parseJSON(data);
			console.log( "finished" );
		});
		console.log('posted')
}

$(document).ready(function(){
//$('.nav a[href*="' + location.pathname + '"][class!="noselect"]').addClass('selected');
	$('.nav li a[href="' + location.pathname + '"][class!="noselect"]').addClass('selected');
	$('.nav li a[href="' + location.pathname + '"][class!="noselect"]').parent().addClass('active');
	//console.log(location.pathname.split("/")[2]);
	//console.log(location.pathname.split("/")[1]);
	//console.log(location.pathname);
});
