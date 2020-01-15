const indexLabels = {
    // 'status': '------',
    'candleBtn': 'candles',
    'clockBtn': 'clock 1',
    'adventBtn': 'advent',
    'theaterBtn': 'theater',
    'clockBtn2': 'clock 2',
    'circusBtn': 'circus',
    'stopBtn': 'all off',
    'serviceBtn': 'service'
};
const serviceLabels = {
    'homeBtn': 'home',
    'restartBtn': 'restart app',
    'rebootBtn': 'reboot device'
};

const requestIndexFunctions = {
    'candleBtn': '/candles',
    'clockBtn': '/clock 1',
    'adventBtn': '/advent',
    'theaterBtn': '/theater',
    'clockBtn2': '/clock 2',
    'circusBtn': '/circus',
    'stopBtn': '/all off'
};


function setupIndexPage() {
    try {
        for (const id in requestIndexFunctions) {
            try {
                document.getElementById(id).setAttribute('onclick', "ajaxRequest(requestIndexFunctions[id], this)");
            } catch (e) {
                // console.log(e)
            }
        }
        try {
            document.getElementById('serviceBtn').setAttribute('onclick', "goto('/service')");
        } catch (e) {
            // console.log(e)
        }

        for (const id in indexLabels) {
            try {
                document.getElementById(id).innerHTML = indexLabels[id].toUpperCase();
            } catch (e) {
                // console.log(e)
            }
        }
    } catch (e) {
        // console.log(e)
    }
}

function setupServicePage() {
    document.getElementById('homeBtn').setAttribute('onclick', "goto('/')");
    document.getElementById('restartBtn').setAttribute('onclick', "goto('/');ajaxRequest('/restart')");
    document.getElementById('rebootBtn').setAttribute('onclick', "ajaxRequest('/reboot')");

    for (const id in serviceLabels) {
        document.getElementById(id).innerHTML = serviceLabels[id].toUpperCase();
    }
}

