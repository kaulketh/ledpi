function ajaxRequest(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);

    xhr.onload = function() {

        if (xhr.status !== 200) {
            console.log('Request failed.  Returned status of: ' + xhr.status);
        } else {
            console.log('Response Text: ' + xhr.responseText);
        }
    };
    document.getElementById("status").innerHTML = url.slice(1).toUpperCase();
    xhr.send();
}

function goto(url) {
    location.href = url;
}