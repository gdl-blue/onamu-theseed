function discussFetch(topic) {
    $("div.res-wrapper.res-loading[data-visible=true]").each(function () {
        tid = this.getAttribute('data-id');
        $.get(topic + "/" + String(tid), function(response) {
            document.querySelector(".res-wrapper.res-loading[data-id=\"" + String(tid) + "\"]").innerHTML = response;
            document.querySelector(".res-wrapper.res-loading[data-id=\"" + String(tid) + "\"]").className = 'res-wrapper';
        });
	});
	$(window).scroll(function() {
	    $("div.res-wrapper.res-loading[data-visible=true]").each(function () {
            tid = this.getAttribute('data-id');
            $.get(topic + "/" + String(tid), function(response) {
                document.querySelector(".res-wrapper.res-loading[data-id=\"" + String(tid) + "\"]").innerHTML = response;
                document.querySelector(".res-wrapper.res-loading[data-id=\"" + String(tid) + "\"]").className = 'res-wrapper';
            });
    	});
    });
}

function topic_main_load(tnum, s_num) {
    var o_data = document.getElementById('main_topic');
    if(s_num) {
        var url = "/api/thread/" + tnum + "?render=1&num=" + s_num;
    } else {
        var url = "/api/thread/" + tnum + "?render=1";
    }
    var url_2 = "/api/markup";
    var n_data = "";
    var num = 1;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send(null);

    var xhr_2 = new XMLHttpRequest();
    xhr_2.open("GET", url_2, true);
    xhr_2.send(null);

    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4 && xhr.status === 200) {
            t_data = JSON.parse(xhr.responseText);
            var rescount = document.querySelectorAll('.res-wrapper').length;
            var cnt = 1;
            for(key in t_data) {
                n_data += t_data[key]['data'];
                num = key;
                document.getElementById('discussLoadProgress').value = cnt / rescount;
                cnt++;
            }

            document.querySelector(".res-wrapper.res-loading").remove();
            $('#discussLoadProgress').remove();
            o_data.innerHTML = n_data;
            if(document.getElementById('noDisplayHideAuthor').checked)
                toggle('r-hidden-body', 'none');
            else
                toggle('r-hidden-body', 'block');

            jQuery(function() { $("time").each(function () { var format = $(this).attr("data-format"); var time = $(this).attr("datetime"); if (!format || !time) { return; } $(this).text(formatDate(new Date(time), format)); }); });

            if(!s_num) {
                topic_plus_load(tnum, String(Number(num) + 1));
            }

            xhr_2.onreadystatechange = function() {
                if(xhr_2.readyState === 4 && xhr_2.status === 200) {
                    markup = JSON.parse(xhr_2.responseText)['markup'];

                    if(markup === 'markdown') {
                        render_markdown();
                    }
                }
            }
        }
    }

}