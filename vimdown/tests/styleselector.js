$(document).ready(function() {

	function select_style (ev) {
		// alert($(this).attr('name'));
		$("link[rel=stylesheet]").attr({href:$(this).attr('name')+'.css'});
	}//select_style()

	$('div#style_options a').click(select_style);
});
