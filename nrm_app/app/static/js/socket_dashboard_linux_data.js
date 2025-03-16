    import { socket } from "./socket_dashboard.js";

socket.on('linux_server_data_table', function (response) {
    console.log('linux_server_data_table działa');
    console.log(`I got response of: ${response.data} with type: ${typeof(response.data)}`);
    console.log(response.data);

    // Check data status
    if (response.status === 'success'){
        const linuxServerData = response.data;

        let linuxServerDataList = document.getElementById('server-data-list');
        linuxServerDataList.innerHTML = '';

        let row = document.createElement('tr');

        // Cell with disc data
        let diskDataCell = document.createElement('td');
        diskDataCell.textContent = `${linuxServerData.disk_usage.percent}%` || '';
        row.appendChild(diskDataCell);

        // Dodanie komórki dla CPU Usage
        let cpuCell = document.createElement('td');
        cpuCell.textContent = `${linuxServerData.cpu_usage}%` || 0;
        row.appendChild(cpuCell);

        // Dodanie komórki dla Memory Usage
        let memoryCell = document.createElement('td');
        memoryCell.textContent = `${linuxServerData.memory_usage.percent}%` || '';
        row.appendChild(memoryCell);

        // Dodanie wiersza do tabeli
        linuxServerDataList.appendChild(row);

    } else {
       let noServerLinuxDataRow = document.createElement('tr');
        noServerLinuxDataRow.id = 'no_server_linux_data';

        let noServerLinuxDataCell = document.createElement('td');
        noServerLinuxDataCell.colSpan = 3;
        noServerLinuxDataCell.textContent = 'Brak dostępnych danych o serwerze Samba';
        noServerLinuxDataRow.appendChild(noServerLinuxDataCell);

        linuxServerDataList.innerHTML = '';
        linuxServerDataList.appendChild(noServerLinuxDataRow);
        noServerLinuxDataRow.style.display = 'table-row';
    }

});

socket.on('resource_linux_server_data_table', function (response) {
    console.log('resource_linux_server nie działa');
    console.log(`I got response of: ${response.data} with type: ${typeof(response.data)}`);
    console.log("working?")
    console.log(response.data);
    console.log(response.data.name, 'not working');

    // Check data status
    if (response.status === 'success'){
        const resourceServerData = response.data;

        let resourceServerDataList = document.getElementById('server-resource-data-list');
        resourceServerDataList.innerHTML = '';

        let resource_row = document.createElement('tr');

        // Cell with disc data
        let nameDataCell = document.createElement('td');
        nameDataCell.textContent = `${resourceServerData.name}` || '';
        resource_row.appendChild(nameDataCell);

        // Dodanie komórki dla CPU Usage
        let cpuCell = document.createElement('td');
        cpuCell.textContent = `${resourceServerData.cpu_percent}%` || 0;
        resource_row.appendChild(cpuCell);

        // Dodanie komórki dla Memory Usage
        let memoryCell = document.createElement('td');
        memoryCell.textContent = `${resourceServerData.memory_usage_gb}GB` || '';
        resource_row.appendChild(memoryCell);

        // Dodanie wiersza do tabeli
        resourceServerDataList.appendChild(resource_row);

    } else {
       let noResourceServerDataRow = document.createElement('tr');
        noResourceServerDataRow.id = 'no_resource_linux_data';

        let noResourceServerDataCell = document.createElement('td');
        noResourceServerDataCell.colSpan = 3;
        noResourceServerDataCell.textContent = 'Brak dostępnych danych o serwerze Samba';
        noResourceServerDataRow.appendChild(noResourceServerDataCell);

        resourceServerDataList.innerHTML = '';
        resourceServerDataList.appendChild(noResourceServerDataRow);
        noResourceServerDataRow.style.display = 'table-row';
    }

});


function renderServerPagination(totalPages, currentPage) {
    console.log("should handle pagination");
    let paginationControls = document.getElementById('pagination-controls-server-data');
    paginationControls.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        let li = document.createElement('li');

        // Wyróżnij wybraną stronę
        li.className = 'page-item-data ' + (i === currentPage ? 'active' : '');

        // Prepare clickable link for card swap
        const link = document.createElement('a');
        link.className = 'page-link-data';
        link.href = '#';
        link.textContent = i;

        link.onclick = function () {
            console.log("Wysłano żądanie strony:", i); // Debugging
            socket.emit('request_page_for_server_data', { page: i });
        };

        li.appendChild(link);
        paginationControls.appendChild(li);
    }
}
