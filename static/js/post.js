(function($) {

  $(function() {
    var $newPostForm = $('.new-post-form');


    $newPostForm.submit(function(e) {
      e.preventDefault();

      var $this = $(this);

      $.ajax({
               url: '/posts/' + $this.data('post-id') + '/comments',
               data: $('.new-post-form').serialize(),
               type: 'POST',
               dataType: 'html'
             })
      .done(function(data) {
        $(data).hide().prependTo('.comments').fadeIn('slow');
        successAlert();
      })
      .fail(function() {
        failureAlert();
      });
    });

    $('.add-favorite').click(function() {
      var $this = $(this);
      var $favorites = $this.closest('.panel').find('.favorites');

      $favorites.text(parseInt($favorites.text())+1);

      $.ajax({
               url: '/favorite/' + $(this).data('post-id'),
               type: 'POST',
               dataType: "json"
             })
      .done(function() {
        $this.prop('disabled', true);
      })
      .fail(function() {
        $this.prop('disabled', true);
        $favorites.text(parseInt($favorites.text())-1);
        failureAlert();
      });
    });
  });
})(jQuery);
