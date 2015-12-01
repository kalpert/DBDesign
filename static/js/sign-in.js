(function($) {
  $(function() {
    $('.header').find('.sign-in').addClass('active');

    $('.form-signin').submit(function(e) {
      e.preventDefault();

      $.ajax({
               url: '/signIn',
               data: $('form').serialize(),
               type: 'POST',
               dataType: "json"})
      .done(function(data) {
        if (data['redirect']) {
          window.location.href = data['redirect'];
        }
      })
      .fail(function(data) {
        if (data['status'] === 401) {
          $('.form-signin').addClass('has-error');
        }
        else {
          window.location.href = '/error';
        }
      });
    });
  });
})(jQuery);
