(function($) {

  $(function() {

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
