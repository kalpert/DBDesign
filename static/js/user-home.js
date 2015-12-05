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
  });
})(jQuery);
