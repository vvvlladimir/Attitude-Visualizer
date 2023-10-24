document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        const ulElement = document.querySelector('.subHeader');
        ulElement.style.animation = 'scrollUp 1.5s .16s forwards';
    }, 2000);
});

function deleteFile(fileName) {
    fetch(`/delete/${fileName}`, {
        method: 'DELETE'
    }).then(response => response.json()).then(data => {
        if (data.status === "success") {
            location.reload();
        } else {
            alert("Error deleting file");
        }
    });
}

fetch('/list_files/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('jsonDate').textContent = data.date;
        document.getElementById('jsonTime').textContent = data.time;
    })
    .catch(error => {
        console.error('There was an error fetching the data:', error);
    });
