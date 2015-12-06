(function($) {

  $(function() {
    var $editPost = $('.edit-post');
    var $editPostForm = $('.edit-post-form');
    var $deletePost = $('.delete-post');

    $('.header').find('.my-posts').addClass('active');

    $editPost.click(function() {
      $('.post').addClass('hide');
      $editPostForm.removeClass('hide');
    });


    $editPostForm.submit(function(e) {
      e.preventDefault();

      $.ajax({
               url: '/posts/' + $editPostForm.data('post-id'),
               data: $editPostForm.serialize(),
               type: 'PUT',
               dataType: "json"
             })
      .done(function() {
        $('.post-body').text($editPostForm.find('textarea').val());
        $editPostForm.find('textarea').val('');
        $('.post').removeClass('hide');
        $editPostForm.addClass('hide');
        successAlert();
      })
      .fail(function() {
        failureAlert();
      });
    });

    $deletePost.click(function() {
      var $this = $(this);

      $.ajax({
               url: '/posts/' + $deletePost.data('post-id'),
               type: 'DELETE',
               dataType: "json"
             })
      .done(function() {
        $this.closest('.panel').fadeOut("normal", function() {
          $(this).remove();
        });
        successAlert();
      })
      .fail(function() {
        failureAlert();
      });
    });
  });
})(jQuery);
