function topic_top_load(name, sub) {
    var o_data = document.getElementById('top_topic');
    var url = "/api/topic/" + encodeURI(name) + "/sub/" + encodeURI(sub) + "?top=1&render=1";
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
            topic_main_load(name, sub, null);
        }
    }
    
}