(function($, global) {

  $(function() {

    global.successAlert = function() {
      $.notify({
                 icon: 'glyphicon glyphicon-ok',
                 message: "Success!"
               },
               {
                 type: 'success',
                 placement: {
                   align: 'center'
                 }
               }
      );
    }

    global.failureAlert = function() {
      $.notify({
                 icon: 'glyphicon glyphicon-ok',
                 message: "Error!"
               },
               {
                 type: 'danger',
                 placement: {
                   align: 'center'
                 }
               }
      );
    }

  });
})(jQuery, window);
