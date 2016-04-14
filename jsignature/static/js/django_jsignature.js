

$(document).ready(function() {

  function dopreview() {
      var sigdiv = $(this).find('.jsign-container').change();
      var datapair = sigdiv.jSignature("getData", "image"); 
      var i = new Image();
      i.src = "data:" + datapair[0] + "," + datapair[1];
      $('#preview-'+ sigdiv.attr('id')).empty().append($(i).css('width', 'auto').css('height', 25));
  }

  $(".jsign-wrapper").not('.ro').each(function(){

      var name = $('#id_' + $(this).data('signatory-field') + '_text').val();
      var dlg = $(this).dialog({
          title: name || 'Signature',
          resizeable: false,
          width: 'auto',
          height: 'auto',
          modal: true,
          autoOpen: false,
          close: dopreview,
          open: function() {
              $(this).find('.jsign-container').css('width', '700px').resize();
              $(this).dialog("option", "position", "center");
          }
      });

      var jsign = $(this).find('.jsign-container');
      jsign.jSignature(jsign.data('config'));
      jsign.jSignature("setData", jsign.data('initial-value'), "native");

      dopreview.call(dlg);
  });

  /* Each time user is done drawing a stroke, update value of hidden input */
  $(".jsign-container").on("change", function(e) {
      var jSignature_data = $(this).jSignature('getData', 'svg');
      var django_field_name = $(this).attr('id').split(/_(.+)/)[1];
      $('#id_' + django_field_name).val(JSON.stringify(jSignature_data));
      $('#id_native_' + django_field_name).val(JSON.stringify($(this).jSignature('getData', 'native')));
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
