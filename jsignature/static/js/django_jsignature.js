

$(document).ready(function() {

  function dopreview() {
      var sigdiv = $(this).find('.jsign-container');
      var datapair = sigdiv.jSignature("getData", "image"); 
      var i = new Image();
      i.src = "data:" + datapair[0] + "," + datapair[1];
      $('#preview-'+ sigdiv.attr('id')).empty().append($(i).css('width', 'auto').css('height', 25));
  }
  function native_input(jsign) {
      return $('#id_native_' + jsign.attr('id').split(/_(.+)/)[1]);
  }
  function svg_input(jsign) {
      return $('#id_' + jsign.attr('id').split(/_(.+)/)[1]);
  }

  function endswith(s, suffix) {
      return s.indexOf(suffix, s.length - suffix.length) !== -1;
  }

  $(".jsign-wrapper").not('.ro').each(function(){

      c = $(this).clone().css('width', '800px').appendTo(document.body).show();
      var jsign = c.find('.jsign-container');
      jsign.jSignature(jsign.data('config'));
      var initial = native_input(jsign).val();
      if(initial && !endswith(initial, ',')) 
          jsign.jSignature("setData", initial, 'base30');
      dopreview.call(c[0]);
      c.hide().remove();

      var name = $('#id_' + $(this).data('signatory-field') + '_text').val();
      $(this).dialog({
          title: name || 'Signature',
          resizeable: false,
          width: '800px',
          height: 'auto',
          modal: true,
          autoOpen: false,
          close: function () {
              var jsign = $(this).find('.jsign-container');
              var native_data = String(jsign.jSignature('getData', 'base30'));
              var svg_data = JSON.stringify(jsign.jSignature('getData', 'svg'));

              if(native_data.length == 0 || endswith(native_data, ',')) {
                  svg_data = native_data = '';
              }
              native_input(jsign).val(native_data);
              svg_input(jsign).val(svg_data);              
              dopreview.call(this);
          },
          open: function() {
              $(this).dialog("option", "position", "center");
              
              var jsign = $(this).find('.jsign-container');
              jsign.empty();

              jsign.jSignature(jsign.data('config'));                            
              var initial = native_input(jsign).val();
              if(initial) jsign.jSignature("setData", 'data:' + initial);
          }
      });
  });

  /* Bind clear button */
  $(".jsign-wrapper .jsign_reset_btn").on("click", function(e) {
      $(this).closest('.jsign-wrapper').find('.jsign-container').jSignature('reset');
  });

  /* Bind ok button */
  $(".jsign-wrapper .jsign_ok_btn").on("click", function(e) {
      $(this).closest('.jsign-wrapper').dialog('close');
  });

  /* Bind sign button */
  $(".jsign_btn").on("click", function(e) {
      $('#'+$(this).data('jsign-id')).closest('.jsign-wrapper').dialog("option", "position", "center").dialog('open');
  });

  $(".jsign-preview").not('.ro').on("click", function(e) {
      $('#' + $(this).attr('id').replace('preview-', '')).closest('.jsign-wrapper').dialog('open');
  });
});
