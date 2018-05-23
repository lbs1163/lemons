
var csrftoken = getCookie('csrftoken');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function drawSearchedSubjects(subjects) {
    var searched_subjects_div = $("#searched-subjects");
    searched_subjects_div.empty();

    if (subjects.length == 0) {
        searched_subjects_div.append('<h5>검색 결과가 없습니다!</h5>');
        return;
    }

    var collection_div = $('<ul class="collection"></ul>');
    searched_subjects_div.append(collection_div);

    for (var i = 0; i < subjects.length; i++) {
        var item_div = $('<li class="collection-item avatar" subject="' + subjects[i].pk + '"></li>');
        collection_div.append(item_div);
        item_div.append('<span class="title">' + subjects[i].name + '</span>');

        var str = "";
        for (var j = 0; j < subjects[i].period.length; j++) {
            var day = "";
            if (subjects[i].period[j].mon) {
                day += "월, ";
            } if (subjects[i].period[j].tue) {
                day += "화, ";
            } if (subjects[i].period[j].wed) {
                day += "수, ";
            } if (subjects[i].period[j].thu) {
                day += "목, ";
            } if (subjects[i].period[j].fri) {
                day += "금, ";
            }
            str += '<br>' + day.substring(0, day.length-2) + " " + subjects[i].period[j].start.slice(0, 5) + " ~ " + subjects[i].period[j].end.slice(0, 5);
        }

        item_div.append('<p>' + subjects[i].professor
            + ' / ' + subjects[i].code
            + ' / ' + subjects[i].class_number + '분반'
            + '<br>' + subjects[i].credit
            + str + '</p>');
        item_div.append('<a href="#" class="subject-add secondary-content"><i class="material-icons">add</i></a>');
        item_div.append('<a href="/subject/' + subjects[i].pk + '/" target="_blank" class="subject-detail secondary-content"><i class="material-icons">search</i></a>');
    }

    $(".subject-add").bind("click", function(e) {
        var subject = $(this).parent().attr("subject");
        var timetable = $(".tabs .tab .active").attr("timetable");

        if (timetable) {
            addSubjectToTimetable(timetable, subject);
        } else {
            alert("오류: 과목을 추가할 시간표가 없습니다!");
        }
    });
}

function drawTimetables(data) {
    var timetable_box = $("#timetable");
    timetable_box.empty();

    var tabs_outer_div = $('<div class="col s12 xl10 offset-xl1"></div>');

    timetable_box.append(tabs_outer_div);

    if (data.length > 0) {
        var ul = $('<ul class="tabs"></ul>');
        tabs_outer_div.append(ul);

        for (var i = 0; i < data.length; i++) {
            var li = $('<li class="tab"></li>');
            var a;

            if (i == 0) {
                a = $('<a class="active" href="#timetable' + data[i].pk
                    + '" timetable="' + data[i].pk + '">시간표 ' + (i+1) + '</a>');
            } else {
                a = $('<a href="#timetable' + data[i].pk
                    + '" timetable="' + data[i].pk + '">시간표 ' + (i+1) + '</a>');
            }

            ul.append(li);
            li.append(a);
        }
    } else {
        var h3 = $('<h3 class="center-align">시간표가 없어요 ;(</h3>');
        var p = $('<p class="center-align">오른쪽 하단의 메뉴에서 새 시간표를 만들어보세요!</p>');
        tabs_outer_div.append(h3);
        tabs_outer_div.append(p);
    }

    for (var i = 0; i < data.length; i++) {
        var colors = ["red", "yellow", "orange", "teal", "purple", "indigo", "light-blue", "lime", "brown", "blue-grey"];
        var color_num = 0;
        var color_dict = {};

        for (var j = 0; j < data[i].subjects.length; j++) {
            if (color_dict[data[i].subjects[j].pk] == undefined) {
                color_dict[data[i].subjects[j].pk] = colors[color_num];
                color_num = color_num + 1;
                if (color_num >= colors.length) {
                    color_num = 0;
                }
            }
        }

        var timetable_div = $('<div id="timetable' + data[i].pk
            + '" class="col s12 xl10 offset-xl1 timetable"></div>');
        timetable_box.append(timetable_div);

        var credits_div = $('<div class="credit center-align"></div>');
        credits_div.append('<h5>학점 통계</h5>');

        var sum = 0;
        var sums = Array.apply(null, Array(10)).map(Number.prototype.valueOf,0);

        for (var j = 0; j < data[i].subjects.length; j++) {
            var subject = data[i].subjects[j];
            var credit = parseInt(subject.credit.split('-')[2]);
            sum = sum + credit;

            for (var k = 0; k < categories.length; k++) {
                if (categories[k] == subject.category.category) {
                    sums[k] = sums[k] + credit;
                }
            }
        }

        credits_div.append('<h6 class="credit-all">총 이수학점: ' + sum + '</h6>');
        credits_div.append('<div class="divider"></div>')
        for (var j = 0; j < categories.length; j++) {
            credits_div.append('<p>' + categories[j] + ': ' + sums[j] + '</p>');
        }

        credits_div.append('<p class="warning">※주의: lms상의 이수구분으로 각 과별로 다를 수 있습니다.</p>');

        credits_div.append('<div class="divider"></div>')

        timetable_div.append(credits_div);

        var days_div = $('<div class="days">'
            + '<p>월요일</p><p>화요일</p><p>수요일</p><p>목요일</p><p>금요일</p>'
            + '</div>');
        timetable_div.append(days_div);

        var time_div = $('<div class="time">'
            + '<p>8</p><p>9</p><p>10</p><p>11</p><p>12</p>'
            + '<p>1</p><p>2</p><p>3</p><p>4</p><p>5</p>'
            + '<p>6</p><p>7</p><p>8</p><p>9</p><p>10</p><p>11</p><p>12</p>'
            + '</div>');
        timetable_div.append(time_div);

        var daybox_div = $('<div class="daybox"></div>');
        timetable_div.append(daybox_div);
        var row_div;

        var days = ['mon', 'tue', 'wed', 'thu', 'fri'];

        for (var j = 0; j < days.length; j++) {
            var day_div = $('<div class="day" day="' + days[j] + '"></div>');
            daybox_div.append(day_div);

            var range_div = $('<div class="red lighten-2 valign-wrapper time-range-selector disabled"><p>클릭해서 선택</p></div>');
            day_div.append(range_div);

            var subjects = data[i].subjects;

            for (var l = 0; l < subjects.length; l++) {
                var periods = subjects[l].period;

                for (var m = 0; m < periods.length; m++) {
                    if (periods[m].mon && days[j] == 'mon'
                        || periods[m].tue && days[j] == 'tue'
                        || periods[m].wed && days[j] == 'wed'
                        || periods[m].thu && days[j] == 'thu'
                        || periods[m].fri && days[j] == 'fri') {
                        var period_div = $('<div class="period '
                            + color_dict[subjects[l].pk] + ' lighten-4" '
                            + 'subject="' + subjects[l].pk
                            + '" start="' + periods[m].start
                            + '" end="' + periods[m].end + '"></div>');
                        day_div.append(period_div);

                        //period_div.append('<p class="delete"><i class="tiny material-icons">clear</i></p>');
                        period_div.append('<p class="name">' + subjects[l].name + '</p>');
                        period_div.append('<p class="professor">' + subjects[l].professor + '</p>');
                        period_div.append('<p class="place">' + periods[m].place + '</p>');
                        period_div.append('<a class="subject-delete" href="javascript:void(0)"><i class="material-icons">close</i></a>');
                        period_div.append('<a class="subject-detail" target="_blank" href="/subject/' + subjects[l].pk + '/"><i class="material-icons">search</i></a>');
                    }
                }

                if ((j==0)&&(periods.length == 0)){

                    if (row_div == undefined) {
                        row_div = $('<div class="row" id="noperiod"></div>');
                        timetable_div.append(row_div);
                        row_div.append('<p class="center-align">시간표에 없는 과목</p>');
                    }

                    var col_div = $('<div class = "col s3"></div>');
                    row_div.append(col_div);

                    var card_div = $('<div class = "card '
                            + color_dict[subjects[l].pk] + ' lighten-4" '
                            + 'subject="' + subjects[l].pk
                            + '"></div>');
                    col_div.append(card_div);

                    var noperiod_div = $('<div class = "card-content"></div>');
                    card_div.append(noperiod_div);

                    noperiod_div.append('<p class="name">' + subjects[l].name + '</p>');
                    noperiod_div.append('<p class="professor">' + subjects[l].professor + '</p>');
                    noperiod_div.append('<a class="subject-delete" href="javascript:void(0)"><i class="material-icons">close</i></a>');
                    noperiod_div.append('<a class="subject-detail" target="_blank" href="/subject/' + subjects[l].pk + '/"><i class="material-icons">search</i></a>');
                }
            }

            var hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];

            for (var k = 0; k < hours.length; k++) {
                var hour_div = $('<div class="hour" hour="' + hours[k] + '"></div>');
                day_div.append(hour_div);

                var thirty_minute_div_1 = $('<div draggable="true" class="thirty-minute" start="0"></div>');
                var thirty_minute_div_2 = $('<div draggable="true" class="thirty-minute" start="30"></div>');

                hour_div.append(thirty_minute_div_1);
                hour_div.append(thirty_minute_div_2);
            }
        }
    }

    $(".period .subject-delete").bind("click", function(e) {
        var subject = $(this).parent().attr('subject');
        var timetable = $("#timetable ul.tabs .tab a.active").attr("timetable");

        deleteSubjectFromTimetable(timetable, subject);
    });

    $(".card .subject-delete").bind("click", function(e) {
        var subject = $(this).parent().parent().attr('subject');
        var timetable = $("#timetable ul.tabs .tab a.active").attr("timetable");

        deleteSubjectFromTimetable(timetable, subject);
    })

    $(".time-range-selector").bind("click touchstart", timeRangeSelectorEventHandler);

    redrawTimetable();
    $('.tabs').tabs();
}

// semester를 pk로 받아 요청을 보내는 함수
// 이런 식으로 짜는데 done부분은 일단 결과 출력만 해놓고 내가 나중에 채우겠음
function selectSemester(semester) {
    $.ajax({
        method: "GET",
        url: "/select_semester/",
        data: {
            semester: semester
        },
    }).done(function(data) {
        drawTimetables(data);
    }).fail(function() {
        alert("오류: 학기를 선택할 수 없습니다!");
        window.location.reload();
    });
}

function addTimetable(semester) {
    $.ajax({
        method: "POST",
        url: "/add_timetable/",
        data: {
            semester: semester
        },
    }).done(function(data) {
          drawTimetables(data);
          $('#timetable .tabs .tab a').removeClass('active');
          $('#timetable .tabs .tab a').last().addClass('active');
          $('.tabs').tabs();
    }).fail(function() {
          alert("오류: 시간표를 추가할 수 없습니다!");
          window.location.reload();
    });
}

function deleteTimetable(timetable) {
  $.ajax({
      method: "POST",
      url: "/delete_timetable/",
      data: {
          timetable: timetable
      },
  }).done(function(data) {
        drawTimetables(data);
      }).fail(function() {
            alert("오류: 시간표를 삭제할 수 없습니다!");
            window.location.reload();
      });
}

function copyTimetable(timetable) {
  $.ajax({
      method: "POST",
      url: "/copy_timetable/",
      data: {
          timetable: timetable
      },
  }).done(function(data) {
        drawTimetables(data);
        $('#timetable .tabs .tab a').removeClass('active');
        $('#timetable .tabs .tab a').last().addClass('active');
        $('.tabs').tabs();
      }).fail(function() {
            alert("오류: 시간표를 복사할 수 없습니다!");
            window.location.reload();
      });
}

function searchSubject(data) {
    $.ajax({
        method: "GET",
        url: "/search_subject/",
        data: data,
    }).done(function(data) {
        drawSearchedSubjects(data);
    }).fail(function() {
        alert("오류: 검색할 수 없습니다!");
        window.location.reload();
    });
}

function addSubjectToTimetable(timetable, subject) {
    $.ajax({
        method: "POST",
        url: "/add_subject_to_timetable/",
        data: {
            timetable: timetable,
            subject: subject
        },
    }).done(function(data) {
        if (data['error']) {
            alert("오류: " + data['error']);
        } else {
            drawTimetables(data);
            $('#timetable .tabs .tab a').removeClass('active');
            $('#timetable .tabs .tab a[href="#timetable' + timetable + '"]').addClass('active');
            $('.tabs').tabs();
        }
    }).fail(function() {
        alert("오류: 시간표에 과목을 추가할 수 없습니다!");
        window.location.reload();
    });
}

function deleteSubjectFromTimetable(timetable, subject) {
    $.ajax({
        method: "POST",
        url: "/delete_subject_from_timetable/",
        data: {
            timetable: timetable,
            subject: subject
        },
    }).done(function(data) {
        if (data['error']) {
            alert("오류: " + data['error']);
        } else {
            drawTimetables(data);
            $('#timetable .tabs .tab a').removeClass('active');
            $('#timetable .tabs .tab a[href="#timetable' + timetable + '"]').addClass('active');
            $('.tabs').tabs();
        }
    }).fail(function() {
        alert("오류: 시간표에서 과목을 삭제할 수 없습니다!");
        window.location.reload();
    });
}

function redrawPeriod(period) {
    var start = period.attr('start');
    var end = period.attr('end');

    var starts = start.split(":");
    var start_hour = parseInt(starts[0]);
    var start_minute = parseInt(starts[1]);

    var ends = end.split(":");
    var end_hour = parseInt(ends[0]);
    var end_minute = parseInt(ends[1]);

    var delta = (end_hour * 60 + end_minute) - (start_hour * 60 + start_minute);

    var height = (delta * 3 / 30) + "vh";
    var top = (((start_hour - 8) * 60 + start_minute) * 3 / 30) + "vh";

    period.css("height", height);
    period.css("top", top);
}

function redrawTimetable() {
    $(".period").each(function() {
        redrawPeriod($(this));
    });
}

function beforeSemesterButtonEventHandler(e) {
    $("#semester-after").removeClass('disabled');

    var current = $('h4.semester.active').first();
    var before = current.next('h4.semester');

    if (before.length == 0) {
        alert("이전 학기가 없습니다");
    } else {
        var semester = parseInt(before.attr('semester'));
        current.removeClass("active");
        before.addClass("active");
        selectSemester(semester);

        var beforebefore = before.next('h4.semester');
        if (beforebefore.length == 0) {
            $("#semester-before").addClass('disabled');
        }
    }
}

function afterSemesterButtonEventHandler(e) {
    $("#semester-before").removeClass('disabled');

    var current = $('h4.semester.active').first();
    var after = current.prev('h4.semester');

    if (after.length == 0) {
        alert("다음 학기가 없습니다");
    } else {
        var semester = parseInt(after.attr('semester'));
        current.removeClass("active");
        after.addClass("active");
        selectSemester(semester);

        var afterafter = after.prev('h4.semester');
        if (afterafter.length == 0) {
            $("#semester-after").addClass('disabled');
        }
    }
}

function addTimetableButtonEventHandler(e) {
    var semester_name = $("h4.semester.active").html();
    var semester = $("h4.semester.active").attr("semester");

    var r = confirm(semester_name + "에 시간표를 추가하시겠습니까?");

    if (r) {
        addTimetable(semester);
    }
}

function copyTimetableButtonEventHandler(e) {
    var timetable_name = $("#timetable ul.tabs .tab a.active").html();
    var timetable = $(".tabs .tab .active").attr("timetable");

    if (timetable == undefined) {
        alert("오류: 복사할 시간표가 없습니다!")
        return;
    }

    var r = confirm("현재 선택된 " + timetable_name + "(을)를 복사하시겠습니까?");

    if (r) {
        copyTimetable(timetable);
    }
}
// 지금 사용자가 보고있는 시간표를 지우는 기능??
function deleteTimetableButtonEventHandler(e) {
    var timetable_name = $("#timetable ul.tabs .tab a.active").html();
    var timetable = $("#timetable ul.tabs .tab a.active").attr("timetable");

    if (timetable == undefined) {
        alert("오류: 삭제할 시간표가 없습니다!")
        return;
    }

    var r = confirm("현재 선택된 " + timetable_name + "(을)를 정말로 삭제하시겠습니까?");

    if (r) {
      deleteTimetable(timetable);
    }
}

function SaveToImageButtonEventHandler(e) {

    $(".subject-delete .material-icons, .subject-detail .material-icons, .credit").addClass("invisible");
    $(".time").css("top", "3.5vh");
    $(".timetable").addClass("no-margin");
    
    domtoimage.toJpeg($(".timetable.active").get(0), { bgcolor: "white" })
    .then(function (dataUrl) {
        var link = document.createElement('a');
        link.download = 'timetable.jpeg';
        link.href = dataUrl;
        link.click();
        $(".subject-delete .material-icons, .subject-detail .material-icons, .credit").removeClass("invisible");
        $(".time").removeAttr("style");
        $(".timetable").removeClass("no-margin");
    });
}

function hundredcheckboxchangeHandler(e){
    if($(this).attr("name")=="all_hundred"){ //'전체'를 클릭했을 때
        //전체를 체크한 경우 나머지 체크해제
        if ($('#hundreds input[name="all_hundred"]').is(":checked")){
            $('#hundreds input[name="one_hundred"]').prop("checked", false);
            $('#hundreds input[name="two_hundred"]').prop("checked", false);
            $('#hundreds input[name="three_hundred"]').prop("checked", false);
            $('#hundreds input[name="four_hundred"]').prop("checked", false);
            $('#hundreds input[name="higher_hundred"]').prop("checked", false);
        }
        //나머지가 체크되어있지 않을 때 전체를 체크해제 한 경우 해제되지 않음
        else{
            if ((!$('#hundreds input[name="one_hundred"]').is(":checked"))
                && (!$('#hundreds input[name="two_hundred"]').is(":checked"))
                && (!$('#hundreds input[name="three_hundred"]').is(":checked"))
                && (!$('#hundreds input[name="four_hundred"]').is(":checked"))
                && (!$('#hundreds input[name="higher_hundred"]').is(":checked"))){

                $('#hundreds input[name="all_hundred"]').prop("checked", "checked");
            }
        }
    }
    else{ //나머지를 클릭했을때
        // 모두 체크하면 '전체' 체크로 바꿈
        if ($('#hundreds input[name="one_hundred"]').is(":checked")
            && $('#hundreds input[name="two_hundred"]').is(":checked")
            && $('#hundreds input[name="three_hundred"]').is(":checked")
            && $('#hundreds input[name="four_hundred"]').is(":checked")
            && $('#hundreds input[name="higher_hundred"]').is(":checked")) {

            $('#hundreds input[name="all_hundred"]').prop("checked", "checked");
            $('#hundreds input[name="one_hundred"]').prop("checked", false);
            $('#hundreds input[name="two_hundred"]').prop("checked", false);
            $('#hundreds input[name="three_hundred"]').prop("checked", false);
            $('#hundreds input[name="four_hundred"]').prop("checked", false);
            $('#hundreds input[name="higher_hundred"]').prop("checked", false);
            return;
        }

        //하나라도 체크하면 '전체' 체크해제
        if ($('#hundreds input[name="one_hundred"]').is(":checked")
            || $('#hundreds input[name="two_hundred"]').is(":checked")
            || $('#hundreds input[name="three_hundred"]').is(":checked")
            || $('#hundreds input[name="four_hundred"]').is(":checked")
            || $('#hundreds input[name="higher_hundred"]').is(":checked")){
            $('#hundreds input[name="all_hundred"]').prop("checked", false);
            return;
        }

        //모두 체크해제할 시
        $('#hundreds input[name="all_hundred"]').prop("checked", "checked");
    }    
}

function creditcheckboxchangeHandler(e){
    if($(this).attr("name")=="all_credit"){ //'전체'를 클릭했을 때
        //전체를 체크한 경우 나머지 체크해제
        if ($('#credits input[name="all_credit"]').is(":checked")){
            $('#credits input[name="one_credit"]').prop("checked", false);
            $('#credits input[name="two_credit"]').prop("checked", false);
            $('#credits input[name="three_credit"]').prop("checked", false);
            $('#credits input[name="four_credit"]').prop("checked", false);
            $('#credits input[name="higher_credit"]').prop("checked", false);
        }
        //나머지가 체크되어있지 않을 때 전체를 체크해제 한 경우 해제되지 않음
        else{
            if ((!$('#credits input[name="one_credit"]').is(":checked"))
                && (!$('#credits input[name="two_credit"]').is(":checked"))
                && (!$('#credits input[name="three_credit"]').is(":checked"))
                && (!$('#credits input[name="four_credit"]').is(":checked"))
                && (!$('#credits input[name="higher_credit"]').is(":checked"))){

                $('#credits input[name="all_credit"]').prop("checked", "checked");
            }
        }
    }
    else{ //나머지를 클릭했을때
        // 모두 체크하면 '전체' 체크로 바꿈
        if ($('#credits input[name="one_credit"]').is(":checked")
            && $('#credits input[name="two_credit"]').is(":checked")
            && $('#credits input[name="three_credit"]').is(":checked")
            && $('#credits input[name="four_credit"]').is(":checked")
            && $('#credits input[name="higher_credit"]').is(":checked")) {

            $('#credits input[name="all_credit"]').prop("checked", "checked");
            $('#credits input[name="one_credit"]').prop("checked", false);
            $('#credits input[name="two_credit"]').prop("checked", false);
            $('#credits input[name="three_credit"]').prop("checked", false);
            $('#credits input[name="four_credit"]').prop("checked", false);
            $('#credits input[name="higher_credit"]').prop("checked", false);
            return;
        }

        //하나라도 체크하면 '전체' 체크해제
        if($('#credits input[name="one_credit"]').is(":checked")
            || $('#credits input[name="two_credit"]').is(":checked")
            || $('#credits input[name="three_credit"]').is(":checked")
            || $('#credits input[name="four_credit"]').is(":checked")
            || $('#credits input[name="higher_credit"]').is(":checked")){

            $('#credits input[name="all_credit"]').prop("checked", false);
        }
        //모두 체크해제할 시
        else{
            $('#credits input[name="all_credit"]').prop("checked", "checked");
        }
        
    }    
}

function searchButtonEventHandler(e) {
    e.preventDefault();

    var semester = $("h4.semester.active").attr("semester");
    var data = {};

    data["semester"] = semester;

    if ($("#search select#category").val()) {
        data["category"] = $("#search select#category").val();
    }

    if ($("#search select#department").val()) {
        data["department"] = $("#search select#department").val();
    }

    if ($('#search input[name="one_hundred"]:checked').val()) {
        data["one_hundred"] = $('#search input[name="one_hundred"]:checked').val();
    }
    if ($('#search input[name="two_hundred"]:checked').val()) {
        data["two_hundred"] = $('#search input[name="two_hundred"]:checked').val();
    }
    if ($('#search input[name="three_hundred"]:checked').val()) {
        data["three_hundred"] = $('#search input[name="three_hundred"]:checked').val();
    }
    if ($('#search input[name="four_hundred"]:checked').val()) {
        data["four_hundred"] = $('#search input[name="four_hundred"]:checked').val();
    }
    if ($('#search input[name="higher_hundred"]:checked').val()) {
        data["higher_hundred"] = $('#search input[name="higher_hundred"]:checked').val();
    }

    if ($('#search input[name="one_credit"]:checked').val()) {
        data["one_credit"] = $('#search input[name="one_credit"]:checked').val();
    }
    if ($('#search input[name="two_credit"]:checked').val()) {
        data["two_credit"] = $('#search input[name="two_credit"]:checked').val();
    }
    if ($('#search input[name="three_credit"]:checked').val()) {
        data["three_credit"] = $('#search input[name="three_credit"]:checked').val();
    }
    if ($('#search input[name="four_credit"]:checked').val()) {
        data["four_credit"] = $('#search input[name="four_credit"]:checked').val();
    }
    if ($('#search input[name="higher_credit"]:checked').val()) {
        data["higher_credit"] = $('#search input[name="higher_credit"]:checked').val();
    }

    if ($('#search input#q').val()) {
        data["q"] = $('#search input#q').val();
    }

    if ($('#search input#time').val() != "아래 버튼으로 시간대를 입력하세요") {
        data["start_time"] = day + " " + start_hour + ":" + start_minute;
        data["end_time"] = day + " " + end_hour + ":" + end_minute;
    }

    $('#searched-subjects').empty();
    $("#searched-subjects").append('<h5>로딩중...</h5>');
    searchSubject(data);
}

function timerangeButtonEventHandler(e) {
    e.preventDefault();
    $("#search").modal('close');

    $("header").addClass("invisible");
    $("#semesters").addClass("invisible");
    $("#timetable > div:first-child").addClass("invisible");
    $(".credit").addClass("invisible");
    $(".fixed-action-btn").addClass("invisible");
    $("footer").addClass("invisible");
    $("body").addClass("body-selecting");

    var ypos = $(".timetable.active .days").offset().top;
    window.scrollTo(0, ypos);

    document.body.addEventListener("dragstart", dragStartEventHandler);
    document.body.addEventListener("drag", dragEventHandler);
    document.body.addEventListener("dragend", dragEndEventHandler);

    $(".timetable").addClass("no-scroll");
    $(".timetable").attr("touch-action", "none");

    document.body.addEventListener("touchstart", touchStartEventHandler);
    document.body.addEventListener("touchmove", touchEventHandler);
    document.body.addEventListener("touchend", touchEndEventHandler);
}

function timerangeDeleteButtonEventHandler(e) {
    e.preventDefault();
    $('#search input#time').val("아래 버튼으로 시간대를 입력하세요");
}

function timeRangeSelectorEventHandler(e) {
    e.preventDefault();
    e.stopPropagation();

    $("#search").modal('open');
    if (start_minute == 0) {
        start_minute = "00";
    }
    if (end_minute == 0) {
        end_minute = "00";
    }
    if (reversed) {
        var temp;
        temp = start_hour;
        start_hour = end_hour;
        end_hour = temp;
        temp = start_minute;
        start_minute = end_minute;
        end_minute = temp;
    }
    $('#search input#time').val(day + " " + start_hour + ":" + start_minute + " ~ " + end_hour + ":" + end_minute);

    $('.time-range-selector').addClass("disabled");

    $("header").removeClass("invisible");
    $("#semesters").removeClass("invisible");
    $("#timetable > div:first-child").removeClass("invisible");
    $(".credit").removeClass("invisible");
    $(".fixed-action-btn").removeClass("invisible");
    $("footer").removeClass("invisible");
    $("body").removeClass("body-selecting");

    document.body.removeEventListener("dragstart", dragStartEventHandler);
    document.body.removeEventListener("drag", dragEventHandler);
    document.body.removeEventListener("dragend", dragEndEventHandler);

    $(".timetable").removeClass("no-scroll");
    $(".timetable").removeAttr("touch-action");

    document.body.removeEventListener("touchstart", touchStartEventHandler);
    document.body.removeEventListener("touchmove", touchEventHandler);
    document.body.removeEventListener("touchend", touchEndEventHandler);
}

var day;
var start_hour;
var start_minute;
var end_hour;
var end_minute;
var reversed = false;
var range_div;
var x;
var y;

function touchStartEventHandler(e) {
    e.pageX = e.touches[0].pageX;
    e.pageY = e.touches[0].pageY;
    dragStartEventHandler(e);
}

function touchEventHandler(e) {
    e.pageX = e.touches[0].pageX;
    e.pageY = e.touches[0].pageY;
    x = e.touches[0].pageX;
    y = e.touches[0].pageY;
    dragEventHandler(e);
}

function touchEndEventHandler(e) {
    e.pageX = x;
    e.pageY = y;
    dragEndEventHandler(e);
}

function dragStartEventHandler(e) {
    var img = new Image();
    img.style.display = "none";
    if (e.dataTransfer && e.dataTransfer.setDragImage) {
        e.dataTransfer.setDragImage(img, 0, 0);
    }

    if ($('.timetable.active .day[day="fri"]').offset().left <= e.pageX) {
        day = "fri";
    } else if ($('.timetable.active .day[day="thu"]').offset().left <= e.pageX) {
        day = "thu";
    } else if ($('.timetable.active .day[day="wed"]').offset().left <= e.pageX) {
        day = "wed";
    } else if ($('.timetable.active .day[day="tue"]').offset().left <= e.pageX) {
        day = "tue";
    } else if ($('.timetable.active .day[day="mon"]').offset().left <= e.pageX) {
        day = "mon";
    } else {
        day = undefined;
    }

    var top = $(".timetable.active .thirty-minute").first().offset().top;
    var bottom = $(".timetable.active .thirty-minute").last();
    bottom = bottom.offset().top + bottom.height();

    var height = bottom - top;
    var time = (e.pageY - top) * 32 / height;
    start_hour = ((time / 2)|0) + 8;
    start_minute = ((time | 0) % 2) * 30;

    $(".time-range-selector").addClass("disabled");

    range_div = $('.timetable.active .day[day="' + day + '"] .time-range-selector').first();

    var top = (((start_hour - 8) * 60 + start_minute) * 3 / 30) + "vh";
    range_div.css("top", top);

    range_div.css("height", "3vh");
}

function dragEventHandler(e) {
    var top = $(".timetable.active .thirty-minute").first().offset().top;
    var bottom = $(".timetable.active .thirty-minute").last();
    bottom = bottom.offset().top + bottom.height();

    var height = bottom - top;
    var time = (e.pageY - top) * 32 / height;
    if ((time|0) > 31) {
        time = 31;
    }
    end_hour = ((time / 2)|0) + 8;
    end_minute = ((time | 0) % 2) * 30;

    if (end_hour < start_hour || end_hour == start_hour && end_minute < start_minute) {
        reversed = true;
    } else {
        reversed = false;
    }

    if (!reversed) {
        if (end_minute == 30) {
            end_hour = end_hour + 1;
            end_minute = 0;
        } else if (end_minute == 0) {
            end_minute = end_minute + 30;
        }
    }

    var delta = (end_hour * 60 + end_minute) - (start_hour * 60 + start_minute);
    if (delta < 0) {
        delta = -delta;
    }

    var height = (delta * 3 / 30) + "vh";
    var top;
    if (reversed) {
        top = (((end_hour - 8) * 60 + end_minute) * 3 / 30) + "vh";
    } else {
        top = (((start_hour - 8) * 60 + start_minute) * 3 / 30) + "vh";
    }

    range_div.removeClass("disabled");
    range_div.css("height", height);
    range_div.css("top", top);
}

function dragEndEventHandler(e) {
    var top = $(".timetable.active .thirty-minute").first().offset().top;
    var bottom = $(".timetable.active .thirty-minute").last();
    bottom = bottom.offset().top + bottom.height();

    var height = bottom - top;
    var time = (e.pageY - top) * 32 / height;
    if ((time|0) > 31) {
        time = 31;
    }
    end_hour = ((time / 2)|0) + 8;
    end_minute = ((time | 0) % 2) * 30;

    if (end_hour < start_hour || end_hour == start_hour && end_minute < start_minute) {
        reversed = true;
    } else {
        reversed = false;
    }

    if (!reversed) {
        if (end_minute == 30) {
            end_hour = end_hour + 1;
            end_minute = 0;
        } else if (end_minute == 0) {
            end_minute = end_minute + 30;
        }
    }

    var delta = (end_hour * 60 + end_minute) - (start_hour * 60 + start_minute);
    if (delta < 0) {
        delta = -delta;
    }

    var height = (delta * 3 / 30) + "vh";
    var top;
    if (reversed) {
        top = (((end_hour - 8) * 60 + end_minute) * 3 / 30) + "vh";
    } else {
        top = (((start_hour - 8) * 60 + start_minute) * 3 / 30) + "vh";
    }

    range_div.css("height", height);
    range_div.css("top", top);
}

$(document).ready(function() {
    $('.fixed-action-btn').floatingActionButton();
    $('.modal').modal();
    $('select').formSelect();

    $("#semester-before").bind("click", beforeSemesterButtonEventHandler);
    $("#semester-after").bind("click", afterSemesterButtonEventHandler);

    $("#add-timetable").bind("click", addTimetableButtonEventHandler);
    $("#copy-timetable").bind("click", copyTimetableButtonEventHandler);
    $("#delete-timetable").bind("click", deleteTimetableButtonEventHandler);
    $("#share-on-facebook").bind("click", SaveToImageButtonEventHandler);

    $("#search-button").bind("click", searchButtonEventHandler);

    $("#timerange-select").bind("click", timerangeButtonEventHandler);
    $("#timerange-delete").bind("click", timerangeDeleteButtonEventHandler);
    $('#hundreds input[type="checkbox"]').bind("click", hundredcheckboxchangeHandler);
    $('#credits input[type="checkbox"]').bind("click", creditcheckboxchangeHandler);

    var semester = parseInt($('h4.semester.active').attr('semester'));
    selectSemester(semester);
});
