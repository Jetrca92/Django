$(document).on('click', '.edit-button', function() {
    // Get the post content and id
    let postContent = $(this).closest('.list-group-item').find('.mb-1').text().trim();
    let postId = $(this).data('id');
  
    // Show the textarea and hide the post content
    $(this).closest('.list-group-item').find('.mb-1').hide();
    $(this).closest('.list-group-item').append(`
      <textarea class="form-control mb-1">${postContent}</textarea>
      <button class="btn btn-primary save-button" data-id="${postId}">Save</button>
    `);
  });
  
  $(document).on('click', '.save-button', function() {
    // Get the updated post content and id
    let postContent = $(this).closest('.list-group-item').find('textarea').val().trim();
    let postId = $(this).data('id');
  
    // Send a PUT request to the backend API
    $.ajax({
      url: '/api/posts/' + postId,
      method: 'PUT',
      data: {
        content: postContent
      },
      success: function() {
        // Update the post content in the HTML
        $(this).closest('.list-group-item').find('.mb-1').text(postContent).show();
        $(this).closest('.list-group-item').find('textarea, .save-button').remove();
      }
    });
  });
