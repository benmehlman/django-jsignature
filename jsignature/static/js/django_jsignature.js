

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
  
  window.jsign_submit_prep = function jsign_submit_prep(container) {
      var native_data = String(container.jSignature('getData', 'base30'));
      var svg_data = JSON.stringify(container.jSignature('getData', 'svg'));

      if(native_data.length == 0 || endswith(native_data, ',')) {
          svg_data = native_data = '';
      }
      //alert(svg_data);
      native_input(container).val(native_data);
      svg_input(container).val(svg_data);               
  }

  window.jsign_init = function jsign_init() {
      /* this sets up the handler for the dialog popup mode, where you click on the preview and it opens a dialog for signing */
      $(".jsign-wrapper").not('.inline').each(function(){

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
                  jsign_submit_prep($(this).find('.jsign-container'));
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
          /* Bind ok button */
          $(".jsign_ok_btn", $(this)).on("click", function(e) {
              $(this).closest('.jsign-wrapper').dialog('close');
          });
          
      });

      /* this sets up the handler for the inline mode, where you sign right in place, no preview/dialog */
      $(".jsign-wrapper.inline").each(function(){

          var name = $('#id_' + $(this).data('signatory-field') + '_text').val();
          var jsign = $(this).find('.jsign-container');
          jsign.empty();

          jsign.jSignature(jsign.data('config'));                            
          var initial = native_input(jsign).val();
          if(initial) jsign.jSignature("setData", 'data:' + initial);

          $(this).closest('form').submit(function () {
              jsign_submit_prep(jsign);
          });
      });

      /* Bind clear button */
      $(".jsign-wrapper .jsign_reset_btn").on("click", function(e) {
          $(this).closest('.jsign-wrapper').find('.jsign-container').jSignature('reset');
      });

      /* Bind sign button */
      $(".jsign_btn").on("click", function(e) {
          $('#'+$(this).data('jsign-id')).closest('.jsign-wrapper').dialog("option", "position", "center").dialog('open');
      });

      $(".jsign-preview").on("click", function(e) {
          if(!$(this).hasClass('ro')) {
              $('#' + $(this).attr('id').replace('preview-', '')).closest('.jsign-wrapper').dialog('open');
          }
      });
  }
  jsign_init();
});
