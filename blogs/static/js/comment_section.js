ocument.getElementById("btn-post").addEventListener("click", function () {
    const newCommentText = document.getElementById("new-comment").value.trim();

    if (newCommentText === "") {
        alert("Comment cannot be empty!");
        return;
    }

    const commentContainer = document.getElementById("comment-container");
    const commentElement = document.createElement("div");
    commentElement.classList.add("comment");

    const commentText = document.createElement("p");
    commentText.innerText = newCommentText;
    
    const editButton = document.createElement("button");
    editButton.innerText = "Edit";
    editButton.addEventListener("click", function () {
        if (editButton.innerText === "Edit") {
            // Switch to edit mode
            const editInput = document.createElement("textarea");
            editInput.cols = 50;
            editInput.rows = 3;
            editInput.value = commentText.innerText;

            commentElement.replaceChild(editInput, commentText);
            editButton.innerText = "Save";
        } else {
            // Save edited comment
            const editedText = commentElement.querySelector("textarea").value.trim();
            if (editedText !== "") {
                commentText.innerText = editedText;
                commentElement.replaceChild(commentText, commentElement.querySelector("textarea"));
                editButton.innerText = "Edit";
            } else {
                alert("Comment cannot be empty!");
            }
        }
    });

    const deleteButton = document.createElement("button");
    deleteButton.innerText = "Delete";
    deleteButton.addEventListener("click", function () {
        commentContainer.removeChild(commentElement);
    });

    commentElement.appendChild(commentText);
    commentElement.appendChild(editButton);
    commentElement.appendChild(deleteButton);
    commentContainer.appendChild(commentElement);

    document.getElementById("new-comment").value = "";
});