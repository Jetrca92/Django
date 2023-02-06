document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.edit-button').forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault();
  
      let postId = this.closest('li').id;
      let postContent = document.querySelector(`#p${postId} .post-content`).innerHTML;
      let textarea = document.createElement('textarea');
  
      textarea.value = postContent;
      textarea.className = 'form-control';
      textarea.rows = '3';
  
      postContent.innerHTML = '';
      postContent.appendChild(textarea);
    });
  });
});