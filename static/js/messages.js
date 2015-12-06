(function($) {

  $(function() {
    $('.header').find('.messages').addClass('active');

    $.ajax({url: '/friends', type: 'GET', dataType: 'json'})
    .done(function(data) {
      $('#friend-input').typeahead({
                                     source: data,
                                     autoSelect: true,
                                     afterSelect: function(item) {
                                       $.ajax({
                                                url: '/messages/' + item.id,
                                                data: 'html',
                                                type: 'GET'
                                              })
                                       .done(function(data) {
                                         $('.content').html(data);
                                       });
                                     }
                                   });
    });

    $('.container').on('submit', '#send-message', function(e) {
      console.log('send-message');
      e.preventDefault();

      var $this = $(this);

      $.ajax({
               url: '/messages/' + $this.data('user-id'),
               data: $this.serialize(),
               dataType: 'html',
               type: 'POST'
             })
      .done(function(data) {
        $('div.messages').append(data);
        $this.find('input').val('');
      })
      .fail(function() {
        failureAlert();
      });
    });
  });
})(jQuery);
