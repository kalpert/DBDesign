(function($) {

  $(function() {
    $('.header').find('.add-friends').addClass('active');


    $('.add-friend').click(function() {
      var $this = $(this);

      $.ajax({
               url: '/friends/' + $this.data('id'),
               type: 'POST',
               dataType: "json"
             })
      .done(function() {
        $this.prop('disabled', true);
        successAlert();
      })
      .fail(function() {
        failureAlert()
      });
    });
  });
})(jQuery);
