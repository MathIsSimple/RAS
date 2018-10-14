window.onload = function(event) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let info = JSON.parse(this.responseText).info;
            let html = "";
            for (let client of info) {
                html += "<tr>";
                for (let pinfo of client) {
                    pinfo = pinfo.substr(pinfo.indexOf(":") + 1);
                    html += "<td>"+pinfo+"</td>";
                }
                html += "</tr>";
            }
            document.getElementById("info_tbody").innerHTML = html;
        }
    };
    xhttp.open("GET", "socket_info", true);
    xhttp.send();
}