var uiMap = {
    'status': '------',
    'btnToggle1' : '1',
    'btnToggle2' : '2',
    'adventBtn' : 'advent',
    'animationBtn' : 'animation',
    'clockBtn' : 'clock',
    'xmasBtn' : 'xmas',
    'stopBtn' : 'stop',
    'serviceBtn': 'service'
};

function labelMainPageElements() {
    for (var key in uiMap){
        document.getElementById(key).innerHTML = uiMap[key].toUpperCase();
    }
}

function labelServicePageElements() {
    document.getElementById('homeBtn').innerHTML = "Home";
    document.getElementById('restartBtn').innerHTML = "Restart App";
    document.getElementById('rebootBtn').innerHTML = "Reboot Device";
}
