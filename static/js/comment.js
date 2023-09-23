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
                  <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${res.name}</h5>
                            <p class="card-text">${res.text}</p>
                             <h6 class="card-subtitle mb-2 text-muted text-end">${res.date}</h6>
                        </div>
                  </div>
            `
        }).finally(res => btn.innerHTML = 'Add this comment')

})