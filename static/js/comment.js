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
        commentContainer.innerHTML += `
        <div data="${res.name}" class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">${res.name}</h5>
                <p class="card-text">${res.text}</p>
                <h6 class="card-subtitle mb-2 text-muted text-end">${res.date}</h6>
                <button formaction="{% url 'workspace_delete_comment_ajax' id=comment.id%}" align='end' class="btn btn-danger">Delete</button>
            </div>
        </div>
    `
    })
    .finally(res => btn.innerHTML = 'Add this comment')
})


const commentContainer = document.querySelector('#commentContainer')
function getChildren(list) {
    for (item of list){
        item.getAttribute('data')
        item.children[0].children[3].addEventListener('click', e => {
            e.preventDefault()
            if (e.target.closest('.card')){
                e.target.closest('.card').remove()
            } 
            // fetch(
            //     '/workspace/ajax/delete_comment/',
            //     {
            //         method: 'GET',
            //         headers:{
            //             'Accept': 'application/json'
            //         },
            //         // body
            //     }
            // ).then(response => response.json())
            // .then(response => {
            //     console.log(response);
            // })
        })
    } 
}

getChildren(commentContainer.children)
    
