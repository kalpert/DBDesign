(function($) {

  $(function() {
    var $newPostForm = $('.new-post-form');

    $('select').tagsinput({
                            cancelConfirmKeysOnEmpty: false
                          });

    $newPostForm.find('textarea, input').focus(function() {
      $('.submit, .tags, .wrapper').removeClass('hide');
    });

    $newPostForm.submit(function(e) {
      e.preventDefault();

      $.ajax({
               url: '/post',
               data: $('.new-post-form').serialize(),
               type: 'POST',
               dataType: "json"
             })
      .done(function() {
        $('select').tagsinput('removeAll');
        $newPostForm.find('textarea').val('');
      })
      .fail(function() {
        window.location.href = '/error';
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
