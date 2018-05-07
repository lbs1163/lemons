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
        console.log(data);
    }).fail(function() {
        alert("오류: 학기를 선택할 수 없습니다!");
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

window.onload = function() {
    redrawTimetable();
};