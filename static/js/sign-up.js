(function($) {
  $(function() {
    $('.header').find('.sign-up').addClass('active');

    $('.form-signin').submit(function(e) {
      e.preventDefault();

      $.ajax({
               url: '/signUp',
               data: $('form').serialize(),
               type: 'POST',
               dataType: "json"
             })
      .done(function(data) {
        $('.alert-message').addClass('hide');

        if (data['redirect']) {
          window.location.href = data['redirect'];
        }
      })
      .fail(function(data) {
        if (data['status'] === 400) {
          $('.form-signin').addClass('has-error');
          $('.alert-message').removeClass('hide').text(data['responseJSON']['error']);
        }
        else {
          window.location.href = '/error';
        }
      });
    });
  });
})(jQuery);
