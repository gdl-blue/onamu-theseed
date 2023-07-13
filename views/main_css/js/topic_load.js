function topic_load(name, sub, num) {
    var test = setInterval(function() {
        var url = "/api/topic/" + name + "/sub/" + sub + "?num=" + num;
        var doc_data = document.getElementById("plus");

        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.send(null);

        xhr.onreadystatechange = function() {
            if(this.readyState === 4 && this.status === 200) {
                if(this.responseText) {
                    doc_data.innerHTML += '<table id="toron" style="background: transparent;"> <tbody><tr> <td id="toron_color"> <a href="javascript:void(0);" id="51"></a> <a href="/w/사용자:시스템"><b>시스템</b></a> </td></tr><tr> <td style="padding:5px 10px 10px 15px; background:#e8e8e8;color:#4a4a4a; border-radius:0 0 6px 6px; box-sizing:inherit; display:block; box-sizing:inherit; box-sizing:inherit; font-size:1rem; font-weight:400;">새 댓글이 있습니다. <a href="?">새로고침</a>해 주세요. </td></tr></tbody></table><br>';

                    // https://programmingsummaries.tistory.com/379
                    var options = {
                        body: 'New topic'
                    }
                   
                    var notification = new Notification("openNAMU", options);
                    
                    setTimeout(function () {
                        notification.close();
                    }, 5000);

                    clearInterval(test);
                }
            }
        }
    }, 2000);
}