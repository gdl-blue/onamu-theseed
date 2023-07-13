/* 원본: https://theseed.io/js/theseed.js [(C)저작권자-https://theseed.io] */

$(function() {
    $(".spoiler-text").click(function() {
        $(this).css("background", "inherit !important");
        $(this).css("color", "inherit !important");
        $(this).css("border-radius", "inherit !important");
    });

	$("body").on("click","#regBtn",function (event) {
		event.preventDefault();
		var $ef = $("#signupForm");

		if (!$("#signupForm #agreeCheckbox").is(":checked")) {
			alert("해당 내용에 동의하십시오.");
			return;
		}

		$ef.attr({
			"method": "POST",
			"target": "",
			"action": null
		});
		window.onbeforeunload = null;
		$ef.submit();
	});
});
