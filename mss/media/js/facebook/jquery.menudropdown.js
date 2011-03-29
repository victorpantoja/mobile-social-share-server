$(function() {
	$("#cma-dados-perfil").accordion({
		// event: 'mouseover',
		active: false,
		collapsible: true,
		change: function(event, ui) {
			var $menuVisivel = $('.menu-dropdown');
			if (!$menuVisivel.is(':visible')) {
				$('.usuario').removeClass('menu-aberto').addClass('menu-fechado');
				$(this).unbind('mouseleave')
			}
		},
		changestart: function(event, ui) {
			var $menuVisivel = $('.menu-dropdown');
			if (!$menuVisivel.is(':visible')) {
				$('.usuario').removeClass('menu-fechado').addClass('menu-aberto');
				$(this).bind('mouseleave', function(){ $(this).accordion('activate',0);})
			}
			
		},

	});
});

