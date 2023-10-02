document.forms.createComment.addEventListener('submit', e => {
    e.preventDefault();
    const form = e.target
    // const name = form.name.value
    // const text = form.text.value
    const newsId = +document.getElementById('news_id').textContent
    const body = new FormData(form)
    body.append('news', newsId)
    const btn = document.querySelector('#addCommentBtn')
    btn.innerHTML = '<img src="https://i.gifer.com/ZKZg.gif" width="15px">'
    fetch(
        '/ajax/create_comment/',
        {
            method: 'POST',
            headers:{
                'Accept': 'application/json'
            },
            body
        }
    ).then(res => res.json())
    .then(res => {
        return new Promise((resolve, reject) => {
            setTimeout(() => resolve(res), 1300)
        })
    })
    .then(res => {
        const commentContainer = document.querySelector('#commentContainer')
        commentContainer.innerHTML = `
            <div class="card mb-3" id="comment_block_${res.id}">
                <div class="card-body">
                    <h5 class="card-title">${res.name}</h5>
                    <p class="card-text">${res.text}</p>
                    <h6 class="card-subtitle mb-2 text-muted text-end">${res.date}</h6>
                    <button class="btn btn-danger" onclick="deleteComment(${res.id})">Delete</button>
                </div>
            </div>
        ` + commentContainer.innerHTML
    })
    .finally(res => btn.innerHTML = 'Add this comment')
})


const deleteComment = async (commentId) => {

    const res = await fetch(`/workspace/ajax/comments/${commentId}/delete/`)
    if (res.status === 200) {
        const data = await res.json()
        if (data.isDeleted) {
            const commentBlock = document.querySelector(`#comment_block_${commentId}`)
            commentBlock.remove()
        }
    } else {
        alert('Network error or unauthorized')
    }


}  
