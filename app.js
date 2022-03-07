$(document).ready(function () {
    show_bar();
});

function select_btn1(title) {
    $.ajax({
        type: 'POST',
        url: '/api/select1',
        data: {title_give: title},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });
}

function select_btn2(title) {
    $.ajax({
        type: 'POST',
        url: '/api/select2',
        data: {title_give: title},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });
}

function show_bar() {
    $.ajax({
        type: 'GET',
        url: '/api/showbar',
        data: {},
        success: function (response) {
            let show_bar = response['show_bars']
            let cnt1 = show_bar[0]['sel_cnt1']
            let cnt2 = show_bar[0]['sel_cnt2']
            let percent1 = Math.round(cnt1 / (cnt1 + cnt2) * 100)
            let percent2 = Math.round(cnt2 / (cnt1 + cnt2) * 100)

            let temp_html = `
                                       <div class="progress second">
                                            <div class="progress-bar bg-danger" role="progressbar" style="width:${percent1}%" aria-valuenow="15"
                                                 aria-valuemin="0" aria-valuemax="100">${percent1}%
                                            </div>
                                            <div class="progress-bar" role="progressbar" style="width:${percent2}%" aria-valuenow="30"
                                                 aria-valuemin="0" aria-valuemax="100">${percent2}%
                                            </div>
                                        </div>`

            $('#progress_bar').append(temp_html);
        }
    });
}

function openClose() {
    if ($(".comment-box").css("display") == "block") {
        $(".comment-box").hide();
        $("#tr_btn").text("토론참여창 열기");
    } else {
        $(".comment-box").show();
        $("#tr_btn").text("토론참여창 닫기");
    }
}