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

function drawTimetables(data) {
    var timetable_box = $("#timetable");
    timetable_box.empty();

    var tabs_outer_div = $('<div class="col s12 m10 offset-m1 l8 offset-l2"></div>');

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
        var timetable_div = $('<div id="timetable' + data[i].pk
            + '" class="col s12 m10 offset-m1 l8 offset-l2 timetable"></div>');
        timetable_box.append(timetable_div);

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

        var days = ['mon', 'tue', 'wed', 'thu', 'fri'];

        for (var j = 0; j < days.length; j++) {
            var day_div = $('<div class="day" day="' + days[j] + '"></div>');
            daybox_div.append(day_div);

            for (var k = 0; k < data[i].subjects.length; k++) {
                var subjects = data[i].subjects;

                for (var l = 0; l < subjects.length; l++) {
                    var periods = subjects[l].period;

                    for (var m = 0; m < periods.length; m++) {
                        if (periods[m].mon && days[j] == 'mon'
                            || periods[m].tue && days[j] == 'tue'
                            || periods[m].wed && days[j] == 'wed'
                            || periods[m].thu && days[j] == 'thu'
                            || periods[m].fri && days[j] == 'fri') {
                            var period_div = $('<div class="period" '
                                + 'subject="' + subjects[l].pk
                                + '" start="' + periods[m].start
                                + '" end="' + periods[m].end + '"></div>');
                            day_div.append(period_div);

                            period_div.append('<p class="delete"><i class="tiny material-icons">clear</i></p>');
                            period_div.append('<p class="name">' + subjects[l].name + '</p>');
                            period_div.append('<p class="professor">' + subjects[l].professor + '</p>');
                            period_div.append('<p class="place">' + periods[m].place + '</p>');
                        }
                    }
                }
            }

            var hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];

            for (var k = 0; k < hours.length; k++) {
                var hour_div = $('<div class="hour" hour="' + hours[k] + '"></div>');
                day_div.append(hour_div);

                var thirty_minute_div_1 = $('<div class="thirty-minute" start="0"></div>');
                var thirty_minute_div_2 = $('<div class="thirty-minute" start="30"></div>');

                hour_div.append(thirty_minute_div_1);
                hour_div.append(thirty_minute_div_2);
            }
        }
    }

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
          console.log(data);
        }).fail(function() {
              alert("오류: 시간표를 추가할 수 없습니다!");
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
        console.log(data);
      }).fail(function() {
            alert("오류: 시간표를 삭제할 수 없습니다!");
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
        console.log(data);
      }).fail(function() {
            alert("오류: 시간표를 복사할 수 없습니다!");
      });
}

function searchSubject(q, one_hundred, two_hundred, three_hundred, four_hundred, higher_hundred, department, category, start_time, end_time, one_credit, two_credit, three_credit, four_credit) {
    $.ajax({
        method: "GET",
        url: "/searchSubject/",
        data: {
            q: q,
            one_hundred: one_hundred, two_hundred: two_hundred, three_hundred: three_hundred, four_hundred: four_hundred, higher_hundred: higher_hundred,
            department: department,
            category: category,
            start_time: start_time, end_time: end_time,
            one_credit: one_credit, two_credit: two_credit, three_credit: three_credit, four_credit: four_credit
        },
    }).done(function(data) {
        console.log(data);
    }).fail(function() {
        alert("오류: 검색할 수 없습니다!");
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
        console.log(data);
    }).fail(function() {
        alert("오류: addSubjectTotimetable!");
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
        console.log(data);
    }).fail(function() {
        alert("오류: deleteSubjectFromTimetable");
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

    var height = (delta * 2.5 / 30) + "vh";
    var top = (((start_hour - 8) * 60 + start_minute) * 2.5 / 30) + "vh";

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

function searchSubjectButtonEventHandler(e) {
    alert("search subject");
}

function addTimetableButtonEventHandler(e) {
    alert("add timetable");
}

function copyTimetableButtonEventHandler(e) {
    alert("copy timetable");
}

function deleteTimetableButtonEventHandler(e) {
    alert("delete timetable");
}

function shareOnFacebookButtonEventHandler(e) {
    alert("share on facebook");
}

$(document).ready(function() {
    $('.fixed-action-btn').floatingActionButton();
    
    $("#semester-before").bind("click", beforeSemesterButtonEventHandler);
    $("#semester-after").bind("click", afterSemesterButtonEventHandler);

    $("#search-subject").bind("click", searchSubjectButtonEventHandler);
    $("#add-timetable").bind("click", addTimetableButtonEventHandler);
    $("#copy-timetable").bind("click", copyTimetableButtonEventHandler);
    $("#delete-timetable").bind("click", deleteTimetableButtonEventHandler);
    $("#share-on-facebook").bind("click", shareOnFacebookButtonEventHandler);

    var semester = parseInt($('h4.semester.active').attr('semester'));
    selectSemester(semester);
});