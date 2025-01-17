export const socket = io('localhost:5002');
let currentUsers;
let previousUsers = [];

socket.on('connect', function () {
    // server connected
    console.log("connected now");
    socket.emit('what_about_server');
});

// Obsługa błędów połączenia
socket.on('connect_error', (err) => {
    console.error('Błąd połączenia z WebSocket:', err);
});

socket.on('update_users', function (data) {
    console.log('update_users działa')
    currentUsers = data;

    let otherUsers = JSON.stringify(previousUsers) !== JSON.stringify(data.users);

    if (!otherUsers) {
        // if users didn't change... left function'
        return;
    }

    previousUsers = data.users;
    let userList = document.getElementById('user-list');

    userList.innerHTML = '';

    if (data.users.length > 0) {
        // add all active users to list
        data.users.forEach(function (user) {
            let row = document.createElement('tr');

            // Dodaj kolumny dla każdego użytkownika
            let usernameCell = document.createElement('td');
            console.log(user);
            usernameCell.textContent = user[0]; // Username
            row.appendChild(usernameCell);

            let groupCell = document.createElement('td');
            groupCell.textContent = user[1]; // Group
            row.appendChild(groupCell);

            let machineCell = document.createElement('td');
            machineCell.textContent = user[2]; // Machine
            row.appendChild(machineCell);

            // Dodaj wiersz do tabeli
            userList.appendChild(row);

        });
    } else {
        let noUserRow = document.createElement('tr');
        noUserRow.id = 'no_user';

        let noUserCell = document.createElement('td');
        noUserCell.colSpan = 3;
        noUserCell.textContent = 'Brak aktywnych użytkowników';

// Dodaj komórkę `td` do wiersza `tr`
noUserRow.appendChild(noUserCell);

// Wyczyść listę użytkowników i dodaj nowy wiersz `no_user`
userList.innerHTML = '';
userList.appendChild(noUserRow);

// Opcjonalnie, ustaw styl, jeśli jest to potrzebne
noUserRow.style.display = 'table-row';
    }
    // pagintaion handle
    renderPagination(data.total_pages, data.page)
});


// Pagination function for users
function renderPagination(totalPages, currentPage) {
    console.log('renderuje paginacje:');
    let paginationControls = document.getElementById('pagination-controls');
    paginationControls.innerHTML = ''; // Wyczyść istniejące elementy paginacji

    for (let i = 1; i <= totalPages; i++) {
        let li = document.createElement('li');

        // Wyróżnij wybraną stronę
        li.className = 'page-item ' + (i === currentPage ? 'active' : '');

        // Utwórz klikalny link
        const link = document.createElement('a');
        link.className = 'page-link';
        link.href = '#';
        link.textContent = i;

        // Przygotuj event socket do żądania wybranej strony
        link.onclick = function () {
            console.log("Wysłano żądanie strony:", i); // Debugging
            socket.emit('request_page', { page: i });
        };

        li.appendChild(link);
        paginationControls.appendChild(li);
    }
}

