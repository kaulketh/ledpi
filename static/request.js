function ajaxRequest(url) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);

    xhr.onload = function () {

        if (xhr.status !== 200) {
            console.log('Request failed.  Returned status of: ' + xhr.status);
        } else {
            console.log('Response Text: ' + xhr.responseText);
        }
    };
    try {
        xhr.send();
        console.log('function status: ' + url.slice(1).toUpperCase());
        document.getElementById("status").innerHTML = url.slice(1).toUpperCase();
    } catch (e) {
        //console.log(e)
    }
}

function goto(url) {
    location.href = url;
}