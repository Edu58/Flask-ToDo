function deleteTodo(id) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({todoId: id})
    }).then((_res) => {
        window.location.href = '/';
    })
}