(function($) {
  $(function() {
    $('.header').find('.sign-up').addClass('active');

    $('#btnSignUp').click(function() {

      $.ajax({
               url: '/signUp',
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
