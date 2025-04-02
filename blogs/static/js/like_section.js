document.getElementById('like-btn').addEventListener('click', function() {
    const blogId = this.getAttribute('data-blog-id');
    const likeBtn = this;
    const likeCount = document.getElementById('like-count');

    // Get CSRF token from the DOM
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/post/${blogId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.liked) {
            likeBtn.textContent = 'Unlike';
        } else {
            likeBtn.textContent = 'Like';
        }
        likeCount.textContent = data.total_likes;
    })
    .catch(error => console.error('Error:', error));
});