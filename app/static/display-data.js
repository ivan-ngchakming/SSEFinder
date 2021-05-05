function query_events() {
  console.log("Submitting form");
  $.ajax({
    type: "POST",
    url: "ajax/SSE_Loc",
    data: {
      'start_date': $('input[id=start_date]').val(),
      'end_date': $('input[id=end_date]').val(),
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    },
    dataType: 'html',
    success: function (data) {
      console.log("Query success");
      document.getElementById('SSE_Loc').innerHTML = data;
    },
    error: function(XMLHttpRequest, textStatus, errorThrown){
      console.log("Query events by date failed: " + textStatus + " - " + errorThrown);
    },
  });
};


function showCaseDetail(case_number) {
  var td = document.getElementById("case_detail_"+case_number);
  var all_case_detail = document.querySelectorAll('[id^="case_detail_"]');
  var all_output = document.querySelectorAll('[id^="output_"]');

  if (td.style.display == "none") {
    for (i = 0; i < all_case_detail.length; i++) {
      if (all_case_detail[i].id != td.id) {
        all_case_detail[i].style.display = "none";
        all_case_detail[i].getElementsByTagName('Table')[0].innerHTML = "";
      } else {
        document.getElementById('output_'+case_number).innerHTML = "";
        // Turn case deatil for selected case visible
        td.style.display = "table-row";
        document.getElementById('show-add-event-form-' + case_number).style.display = "block";
        document.getElementById('submit-add-event-form-' + case_number).style.display = "none";
        td.getElementsByTagName('Table')[0].innerHTML = "Loading..."
      }
    }

    $.ajax({
        url: 'ajax/case_detail',
        data: {
          'case_number': case_number,
        },
        dataType: 'html',
        success: function (data) {
          td.getElementsByTagName('Table')[0].innerHTML = data;
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          document.getElementById(tabname).innerHTML = "Error";
        },
      });

  } else {
    td.style.display = "none";
  }
};


function showEventDetail(event_name, event_location, date_of_event) {
  var td = document.getElementById("event_detail_"+event_name+"_"+event_location+"_"+date_of_event);
  if (td.style.display == "none") {
    var all_case_detail = document.querySelectorAll('[id^="event_detail_"]')
    for (i = 0; i < all_case_detail.length; i++) {
      if (all_case_detail[i].id != td.id) {
        all_case_detail[i].style.display = "none";
      } else {
        // Turn case deatil for selected case visible
        td.style.display = "table-row";
        td.getElementsByTagName('Table')[0].innerHTML = "Loading..."
      }
    }

    $.ajax({
        url: 'ajax/event_detail',
        data: {
          'event_name': event_name,
          'event_location': event_location,
          'date_of_event': date_of_event,
        },
        dataType: 'html',
        success: function (data) {
          td.getElementsByTagName('Table')[0].innerHTML = data;
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          td.getElementsByTagName('Table')[0].innerHTML = "Error: " + textStatus + " - " + errorThrown;
        },
      });
  } else {
    td.style.display = "none";
  }
};
