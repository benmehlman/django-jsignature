

$(document).ready(function() {

  $(".jsign-container").each(function(){
      var config = $(this).data('config');
      var value = $(this).data('initial-value');
      $(this).jSignature(config);
      $(this).jSignature("setData", value, "native");
      
      function dopreview() {
          var sigdiv = $(this).find('.jsign-container').change();
          var datapair = sigdiv.jSignature("getData", "svgbase64"); 
          var i = new Image();
          i.src = "data:" + datapair[0] + "," + datapair[1];
          $('#preview-'+ sigdiv.attr('id')).empty().append($(i).css('width', 'auto').css('height', 25));
      }
 
      var dlg = $(this).closest('.jsign-wrapper').dialog({
          title: 'Signature',
          resizeable: false,
          width: 'auto',
          height: 'auto',
          modal: true,
          autoOpen: false,
          close: dopreview
      });
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
      $('#'+$(this).data('jsign-id')).closest('.jsign-wrapper').dialog('open');
  });

  $(".jsign-preview").on("click", function(e) {
      $('#' + $(this).attr('id').replace('preview-', '')).closest('.jsign-wrapper').dialog('open');
  });
});
