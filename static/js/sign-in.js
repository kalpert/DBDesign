(function($) {
  $(function() {
    $('#btn-sign-in').click(function() {

      $.ajax({
               url: '/signIn',
               data: $('form').serialize(),
               type: 'POST',
               success: function(response) {
                 console.log(response);
               },
               error: function(error) {
                 console.log(error);
               }
             });
    });
  });
})(jQuery);
