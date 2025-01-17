import { socket } from "./socket_dashboard.js";


socket.on('samba_server_data_table', function (response) {
    console.log('samba_server_data_table działa');

    // Check status firstly.
    if ((response.status === 'success')  || (response.data.samba_server_data.cpu_usage.length > 0)){
        const sambaServerData = response.data.samba_server_data;

        let serverDataList = document.getElementById('server-samba-data-list');
        serverDataList.innerHTML = ''; // Wyczyść istniejące wiersze

        // Loop through data
        const numRows = sambaServerData.cpu_usage.length;
        for (let i = 0; i < numRows; i++) {
            let row = document.createElement('tr');

            // Dodanie komórki dla procesu
            let processCell = document.createElement('td');
            processCell.textContent = sambaServerData.processes[i] || '';
            row.appendChild(processCell);

            // Dodanie komórki dla CPU Usage
            let cpuCell = document.createElement('td');
            cpuCell.textContent = `${sambaServerData.cpu_usage[i]}%` || 0;
            row.appendChild(cpuCell);

            // Dodanie komórki dla Memory Usage
            let memoryCell = document.createElement('td');
            memoryCell.textContent = `${sambaServerData.memory_usage[i]}GB` || '';
            row.appendChild(memoryCell);

            // Dodanie wiersza do tabeli
            serverDataList.appendChild(row);
        }
    } else {
       let noServerSambaDataRow = document.createElement('tr');
        noServerSambaDataRow.id = 'no_server_samba_data';

        let noServerSambaDataCell = document.createElement('td');
        noServerSambaDataCell.colSpan = 3;
        noServerSambaDataCell.textContent = 'Brak dostępnych danych o serwerze Samba';
        noServerSambaDataRow.appendChild(noServerSambaDataCell);

        serverDataList.innerHTML = '';
        serverDataList.appendChild(noServerSambaDataRow);
        noServerSambaDataRow.style.display = 'table-row';
    }
    sambaRenderPagination(response.total_pages, response.page)

});

// Funkcja do renderowania paginacji
function sambaRenderPagination(totalPages, currentPage) {
    console.log('renderuje paginacje dla info o sambie:');
    let paginationControls = document.getElementById('pagination-controls-samba-server-data');
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
            socket.emit('request_page_for_samba_server_data', { page: i });
        };

        li.appendChild(link);
        paginationControls.appendChild(li);
    }
}
