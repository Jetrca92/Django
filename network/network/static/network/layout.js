var allEditBtns = document.querySelectorAll('.edit-button');
var allEditBtnsArray = [...allEditBtns];
allEditBtnsArray.forEach((editBtn) => {
  editBtn.addEventListener('click', () => {
    const postId = editBtn.parentNode.id.match(/\d+/)[0]; // Get post id
    const p = editBtn.parentNode.querySelector('p');
    const editArea = editBtn.parentNode.querySelector('textarea');
    p.style.display = 'none';
    editArea.style.display = 'block';

  });
});

function addEditText() {
  const textArea = document.createEelement('input');
  textArea.setAtribute('type', 'text');

}