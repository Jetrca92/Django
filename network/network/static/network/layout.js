var allEditBtns = document.querySelectorAll('.edit-button');
var allEditBtnsArray = [...allEditBtns];
var allSaveBtns = document.querySelectorAll('.edit-post-btn');
var allSaveBtnsArray = [...allSaveBtns];

// Add event listener to edit btns, display edit area, hide post <p>
allEditBtnsArray.forEach((editBtn) => {
  editBtn.addEventListener('click', () => {
    const postId = editBtn.parentNode.id.match(/\d+/)[0]; // Get post id
    const p = editBtn.parentNode.querySelector('p');
    const editArea = editBtn.parentNode.querySelector('textarea');
    const saveEditedPostBtn = editBtn.parentNode.querySelector('.edit-post-btn');
    editBtn.style.display = 'none';
    p.style.display = 'none';
    editArea.style.display = 'block';
    saveEditedPostBtn.style.display = 'block';
  });
});

// Save edited post, display new <p>, hide edit area
allSaveBtnsArray.forEach((saveBtn) => {
  saveBtn.addEventListener('click', () => {
    const textArea = saveBtn.parentNode.parentNode.querySelector('textarea');
    const textAreaValue = textArea.value
    const p = saveBtn.parentNode.parentNode.querySelector('p');
    const editBtn = saveBtn.parentNode.parentNode.querySelector('.edit-post-btn');
    const editPostBtn = saveBtn.parentNode.parentNode.querySelector('.edit-button');
    p.innerHTML = textAreaValue;
    textArea.style.display = 'none';
    p.style.display = 'block';
    editBtn.style.display = 'none';
    editPostBtn.style.display = 'block';
  })
})


