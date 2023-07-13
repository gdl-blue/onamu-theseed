function topic_plus_load(name, sub, num) {
    var test = setInterval(function() {
        var url = "/api/topic/" + encodeURI(name) + "/sub/" + encodeURI(sub) + "?num=" + num + "&render=1";
        var p_data = document.getElementById("plus_topic");
		var adm = document.getElementById("isa").value;
        var n_data = '';
        var n_num = 1;

        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.send(null);

        xhr.onreadystatechange = function() {
            if(this.readyState === 4 && this.status === 200 && this.responseText !== '{}\n') {                
                t_data = JSON.parse(this.responseText);
                for(key in t_data) {
                    n_data += '<div style="overflow-x: scroll;"><table id="toron" style="background: transparent;"> <tbody><tr> <td id="toron_color_blue"> <a href="javascript:void(0);" id="' + num + '">#' + num + '</a> <a href="/w/%EC%82%AC%EC%9A%A9%EC%9E%90%3A' + encodeURI(t_data[key]['id']) + '">' + t_data[key]['id'] + '</a><span style="float:right">' + t_data[key]['date'] + '</span></td></tr><td style="padding:5px 10px 10px 15px; background:#e8e8e8;color:#4a4a4a; border:none;border-radius:0; box-sizing:inherit; display:block; box-sizing:inherit; box-sizing:inherit; font-size:1rem; font-weight:400;">' + t_data[key]['data'] + '</td></tr></tbody></table></div>';
					if(String(adm) == '1'){ n_data += '<span style="color:#fff; background-color:#d9534f; border-color:#d9534f; display:inline-block; font-weight:400; text-align:center; border:1px solid transparent; padding:.25rem .5rem; font-size:.875rem; border-radius:.2rem;"><span class="wiki-color" style="color:#FFFFFF"><a href="/topic/' + encodeURI('name') + '/sub/' + encodeURI('sub') + '/b/' + num + '" style="color:#fff">[ADMIN] 숨기기</a></span></span><br><br>';}
                    n_num = key;
                }
                
                p_data.innerHTML += n_data;

                // https://programmingsummaries.tistory.com/379
                var options = {
                    body: 'New ' + n_num + ' topic'
                }
               
                var notification = new Notification("openNAMU", options);
                
                setTimeout(function () {
                    notification.close();
                }, 5000);

                topic_plus_load(name, sub, String(Number(num) + 1));
                clearInterval(test);
            }
        }
    }, 2000);
}