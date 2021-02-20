$(document).ready(function () {
	loadNav();
	adjustHeader();
});

function loadNav() {
	$("#nav-placeholder").load("nav");
}

function adjustHeader() {
	$('.header').height($(window).height());
}