
function timeNow() {
      var d = new Date(),
          h =  d.getHours()>12?(d.getHours()-12):d.getHours(),
          m = (d.getMinutes()<10?'0':'') + d.getMinutes();
          l = (d.getHours()>12)?' a.m.':' p.m.'
      return h + ':' + m+l;
}
var m = new Audio('/static/music3.mp3');
$('#chat-form').on('submit', function(event){
    event.preventDefault();
    $.ajax({
        url : '/chat/post/',
        type : 'POST',
        data : { msgbox : $('#chat-msg').val(), to: $('#to').val(), },
        success : function(json){
            $('#chat-msg').val('');
            $('#msg-list').append('<div id = "spacing"></div>');
            $('#msg-list').append('<li class="text-right list-group-item">' + json.msg +'<span class = "time">'+timeNow()+'</span>'+ '</li>');
            $('#msg-list').append('<div id = "spacing"></div>');
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
});
function toggle_online(status) {
	if(status) {
		var c = document.getElementById('on');
		c.innerHTML = 'online';
		c.style.color = 'green';
	}
	else {
		var c = document.getElementById('on');
		c.innerHTML = 'offline';
		c.style.color = 'red';
	}
}

function getMessages(){
    if (!scrolling) {
        $.get('/chat/messages?count='+($('li.text-left')).length+'&to='+$('#to').val(), function(messages){
        	//alert(messages.length);
        	if (messages.length!=63 && messages.length!=62)
        	{	
        		m.play();
                $('#msg-list').append('<div id = "spacing"></div>');
            	$('#msg-list').append('<li class="text-right list-group-item">' + messages+ '<span class = "time">'+timeNow()+'</span> </li>');
                $('#msg-list').append('<div id = "spacing"></div>');
            	var chatlist = document.getElementById('msg-list-div');
            	chatlist.scrollTop = chatlist.scrollHeight;
        	}
        	else {
        		if(messages.length==62) {
        			toggle_online(true);
        		}
        		else {
        			toggle_online(false);
        		}
        	}
        });
    }
    scrolling = false;
}
var scrolling = false;
$(function(){
    $('#msg-list-div').on('scroll', function(){
        scrolling = true;
    });

    var event_msg = new EventSource('/chat/messages?count='+($('li.text-left')).length+'&to='+$('#to').val());
    event_msg.onopen = function () {
        console.log('Connected');
    }
    event_msg.onmessage = function (e) {
        messages = JSON.parse(e.data)
        console.log(messages)
        if (messages.data === true)
        	{	
        		m.play();
                $('#msg-list').append('<div id = "spacing"></div>');
            	$('#msg-list').append('<li class="text-left list-group-item">' + messages.msg+ '<span class = "time">'+timeNow()+'</span> </li>');
                $('#msg-list').append('<div id = "spacing"></div>');
            	var chatlist = document.getElementById('msg-list-div');
            	chatlist.scrollTop = chatlist.scrollHeight;
        	}
        	else {
        		toggle_online(messages.online)
        	}
    }
    event_msg.onerror = function (e) {
        console.log(e)
    }
    //refreshTimer = setInterval(getMessages,700);
});

$(document).ready(function() {
     $('#send').attr('disabled','disabled');
     $('#chat-msg').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
 });

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function give_spacing() {
    var d = document.getElementsByClassName("list-group-item")[0];
    var x = document.getElementById("spacing");
    x.style.height = d;
    alert(d.offsetHeight);
}
