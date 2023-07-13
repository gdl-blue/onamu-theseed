var n = 0;

function topic_plus_load(tnum, num) {
    n = Number(document.getElementById('enu').value);

    var test = setInterval(function() {
        var url = "/api/thread/" + encodeURI(tnum) + "?num=" + num + "&render=1";
        var p_data = document.getElementById("plus_topic");
        var n_data = '';
        var n_num = 1;

        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.send(null);

        xhr.onreadystatechange = function() {
            if(this.readyState === 4 && this.status === 200 && this.responseText !== '{}\n' && Number(num) > Number($('input#numLLR').val())) {
                var element =  document.getElementById('toronac' + String(num));
                var el2 =  document.getElementById('toron' + String(num));

                if(!(typeof(element) != 'undefined' && element != null) && !(typeof(el2) != 'undefined' && el2 != null)) {
                    p_data.innerHTML += '<div id="toron' + String(num) + '" class="res-wrapper res-loading"><div class="res res-type-normal"><div class="r-head"> <a class=num id="' + String(num) + '">#' + String(num) + '</a></div><div class="r-body"></div></div></div>';
                    $('input#numLLR').val(String(Number($('input#numLLR').val()) + 1));
                }

                // console.log('1');
                t_data = JSON.parse(this.responseText);
                for(key in t_data) {
                    n_data += t_data[key]['data'];
                    n_num = key;
                }

                if(!(typeof(element) != 'undefined' && element != null) && !(typeof(el2) != 'undefined' && el2 != null)) {
                    setTimeout(function () {
                        $('#toron' + String(num)).remove();
                        p_data.innerHTML += n_data;
                         jQuery(function() { $("time").each(function () { var format = $(this).attr("data-format"); var time = $(this).attr("datetime"); if (!format || !time) { return; } $(this).text(formatDate(new Date(time), format)); }); });
                    }, 400);
                }

                // https://programmingsummaries.tistory.com/379
                var options = {
                    body: '토론에 새 댓글이 있읍니다. 확인해주십시오.'
                };

                var notification = new Notification("토론", options);

                setTimeout(function () {
                    notification.close();
                }, 3000);
                document.getElementById('enu').value = String(Number(document.getElementById('enu').value) + 1);
                topic_plus_load(tnum, String(Number(num) + 1));
                clearInterval(test);
            }
        }
    }, 1);
}