function topic_list_load(name, sub, s_num, where) {
    var o_data = document.getElementById(where);
    var url = "/api/topic/" + encodeURI(name) + "/sub/" + encodeURI(sub) + "?render=1&num=" + s_num;
    var n_data = "";
    var num = 1;
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send(null);

    xhr.onreadystatechange = function() {
        if(this.readyState === 4 && this.status === 200) {
            t_data = JSON.parse(this.responseText);
            for(key in t_data) {
                n_data += t_data[key]['data'];
                num = key;
            }
            
            o_data.innerHTML = n_data;
        }
    }
    
}