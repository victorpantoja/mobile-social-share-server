$(function() {
    $('#hasItemAdicional').click(function() {
        var isChecked = $(this).is(':checked');
        $('#itemAdicionalCor').attr('disabled', !isChecked);
        $('#itemAdicionalTexto').attr('disabled', !isChecked);
        $('#itemAdicionalImagem').attr('disabled', !isChecked);
        $('#itemAdicionalUrl').attr('disabled', !isChecked);
    });

    $('#gerar-codigo').click(function() {
        var template = [];
        template.push('&lt;script type="text/javascript"&gt;',
        '    var glb = glb || {};',
        '    glb.barra = {');

        template.push('        exibeAssineJa: ' + $('#hasAssineJa').is(':checked').toString() + ',');
        template.push('        exibeCentral: ' + $('#hasCentral').is(':checked').toString() + ($('#hasItemAdicional').is(':checked') ? ',' : ''));
        

        if ($('#hasItemAdicional').is(':checked')) {
            template.push('        itemCustomizado: {',
            '            cor: "#' + $('#itemAdicionalCor').val().replace('#','') + '",',
            '            texto: "' + $('#itemAdicionalTexto').val() + '",',
            '            url: "' + $('#itemAdicionalUrl').val() + '"' + ($('#itemAdicionalImagem').val() ? ',' : ''));

            if ($('#itemAdicionalImagem').val()) {
                template.push('            imagem: "' + $('#itemAdicionalImagem').val() + '"');
            }

            template.push('        }');
        }

        var scriptsPerEnv = {
            'dev': 'http://barra.dev.globoi.com/nova/js/barra-globocom.min.js',
            'qa1': 'http://barra.qa01.globoi.com/nova/js/barra-globocom.min.js',
            'prod': 'http://barra.globo.com/nova/js/barra-globocom.min.js'
        };
        var cssPerEnv = {
            'dev': 'http://barra.dev.globoi.com/nova/css/barra-globocom.min.css',
            'qa1': 'http://barra.qa01.globoi.com/nova/css/barra-globocom.min.css',
            'prod': 'http://barra.globo.com/nova/css/barra-globocom.min.css'
        };
        template.push('    };',
        '    (function() {',
        '        var s = document.createElement("script"); s.type = "text/javascript"; s.async = true;',
        '        s.src = "' + scriptsPerEnv[$('.env:checked').val()] + '";',
        '        var ss = document.getElementsByTagName("script")[0]; ss.parentNode.insertBefore(s, ss);',
        '    })();',
        '&lt;/script&gt;');

        $('.previewJS').html(template.join('\n'));
        $('.previewCSS').html('&lt;link rel="stylesheet"\n href="' + cssPerEnv[$('.env:checked').val()] + '" \n type="text/css" /&gt;');

        $('.preview').show();
    });
});
