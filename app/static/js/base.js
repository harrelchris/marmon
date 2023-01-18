// Display the current UTC time and update it every second
function writeFormattedEveTime() {
    const d = new Date();
    document.getElementById('eve-time').innerText = `${d.getUTCHours()}:${d.getMinutes().toString().padStart(2, '0')}`;
}


// Display the current logged-in player count as a comma separated integer
function writeFormattedPlayerCount(count) {
    while (/(\d+)(\d{3})/.test(count.toString())){
        count = count.toString().replace(/(\d+)(\d{3})/, '$1'+','+'$2');
    }
    document.getElementById('player-count').innerText = count;
}


// Add classes to color text green or red according to server status
function addServerStatusColorClass(inService) {
    const klass = inService ? 'text-success' : 'text-danger';
    document.getElementById('eve-time-wrapper').classList.add(klass);
    document.getElementById('player-count-wrapper').classList.add(klass);
}


// Fetch the current server status and display colored time & player count
function writeServerStatus() {
    fetch('https://esi.evetech.net/latest/status/?datasource=tranquility')
        .then(response => response.json())
        .then(data => {
            addServerStatusColorClass(true);
            writeFormattedEveTime();
            setInterval(() => {writeFormattedEveTime()},1000);
            writeFormattedPlayerCount(data['players']);
        })
        .catch(error => {
            console.error(error);
            addServerStatusColorClass(false);
            writeFormattedEveTime();
            writeFormattedPlayerCount(0);
        })
}


writeServerStatus();
