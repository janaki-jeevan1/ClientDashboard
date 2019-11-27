jQuery(document).ready(function() {

    /*
        Background slideshow
    */
    $('.top-content').backstretch("assets/img/backgrounds/1.jpg");

    $('#top-navbar-1').on('shown.bs.collapse', function(){
    	$('.top-content').backstretch("resize");
    });
    $('#top-navbar-1').on('hidden.bs.collapse', function(){
    	$('.top-content').backstretch("resize");
    });

    /*
        Wow
    */
    new WOW().init();

		// otp
		$(".otp_field").hide();
		$(".password_Field").show();
		$('#login_via_otp').on('change', function() {
				if($('#login_via_otp').prop('checked')){
					$(".otp_field").show();
					$(".password_Field").hide();
				}else{
					$(".otp_field").hide();
					$(".password_Field").show();
				}

		});

});
