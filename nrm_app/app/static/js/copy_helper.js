function copyToClipboard() {
    // funciton to copy data from copy_data endpoint
    const dataToCopy = document.getElementById("copyButton").getAttribute("data-copy");

    // New copy style with clipboard
    navigator.clipboard.writeText(dataToCopy)
        .then(() => {
            // alert("Copied to clipboard: " + dataToCopy);
            document.getElementById('message').innerText = 'Dane skopiowane pomyślnie!';
        })
        .catch(err => {
            console.error("Failed to copy: ", err);
        });
}

