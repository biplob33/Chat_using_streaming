$(function() {

    $('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});

});
function go(pass1,pass2,no)
	{
		if((no>1000000000)&&(no<9999999999))
		{
			if((pass1==pass2))
			{
				var f=document.getElementById('register-form');
				f.submit();
				return true;
			}
			else
			{
				alert("Password Do Not Match");
				var f=document.getElementById('password2');
				f.value='';
				var f=document.getElementById('password');
				f.value='';
				return false;
			}
		}
		else
		{
			alert("Enter a valid mobile No");
			var f=document.getElementById('Mob');
			f.value='';
			return false;
		}
	}