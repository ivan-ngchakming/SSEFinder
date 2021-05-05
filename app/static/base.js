function openTab(tabname) {
  var i;
  var x = document.getElementsByClassName("tab");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(tabname).style.display = "block";

  if (tabname == "SSE_Loc") {
    document.getElementById("nav-bar").style.width = "500px";
    document.getElementById("event_query").style.display = "block";
    $.ajax({
      url: 'ajax/SSE_Loc',
      data: {},
      dataType: 'html',
      success: function (data) {
        document.getElementById(tabname).innerHTML = data;
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        document.getElementById(tabname).innerHTML = "Error";
      },
    });
  } else {
    document.getElementById("nav-bar").style.width = "auto";
    document.getElementById("event_query").style.display = "none";
  }

  $(document).ready(function(){
    $("#case_form").submit(function() {
      setTimeout(function(){},10000);
      $.ajax({
        type: "POST",
        url: "ajax/success-page",
        async: false,
        data: $(this).serialize(),
        success: function () {
          alert("Add record success!");
          location.reload();
        },
        error: function(data){
          alert("Failed to add record!");
        },
      });
    });
  });

  if (tabname == "new_case_btn") {
    $.ajax({
      url: 'ajax/add_newcase',
      data: {},
      dataType: 'html',
      success: function(data){
        document.getElementById('addnewcases').innerHTML = data;
//        document.getElementById('id_case_number').defaultValue = case_id;
//        document.getElementById('id_case_number').disabled = true;
      },
    });
  }

};


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
  var all_case_detail = document.querySelectorAll('[id^="case_detail_"]')

  if (td.style.display == "none") {
    for (i = 0; i < all_case_detail.length; i++) {
      if (all_case_detail[i].id != td.id) {
        all_case_detail[i].style.display = "none";
        all_case_detail[i].getElementsByTagName('Table')[0].innerHTML = "";
      } else {
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


function showEventDetail(event_name) {
  var td = document.getElementById("event_detail_"+event_name);
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


function submissionroutine(request) {
  $.ajax({
    url: 'ajax/success-page',
    data: {
      'request': request,
    },
    dataType: 'html',
    success: function (data) {
      document.getElementById('addnewcases').innerHTML = "added!!!!";
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      document.getElementById('addnewcases').innerHTML = "Error";
    },
  });
};


function showRecordForm(case_number) {
  var tr = document.getElementById("case_detail_"+case_number);
  $.ajax({
    url: 'ajax/showrecordform',
    data: {},
    dataType: 'html',
    success: function (data) {
      tr.getElementsByClassName('RecordBox')[0].innerHTML = data;
      document.getElementById('show-add-event-form-'+case_number).style.display = "none";
      document.getElementById('submit-add-event-form-'+case_number).style.display = "block";
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      tr.getElementsByClassName('RecordBox')[0].innerHTML = "Error";
    },
  });
};

var typingTimer;                //timer identifier
var doneTypingInterval = 1000;  //time in ms, 1 second in this case

function searchcoord() {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(request_coordinate, doneTypingInterval);
}

function request_coordinate() {
  var venue_location = document.getElementById("venue_location").value;
  // GET and show coordinates
  let endpoint = 'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=';
  $.ajax({
      url: endpoint + venue_location,
      type: "GET",
      dataType: 'json',
      success: function(result){
        console.log(result);
        console.log(typeof(result));
        document.getElementById("x_coord_field").innerHTML = result[0]['x'];
        document.getElementById("y_coord_field").innerHTML = result[0]['y'];
        document.getElementById("address_field").innerHTML = result[0]['addressEN'];
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        console.log("Request Coordinate failed!");
      },
   })
};


function submitrecord(case_number) {
  $.ajax({
    type : "POST",
    url: 'ajax/showrecordform',
    data: {
      'venue_name' : $('#venue_name').val(),
      'venue_location' : $('#venue_location').val(),
      'address' : document.getElementById("address_field").innerHTML,
      'x_coord' : document.getElementById("x_coord_field").innerHTML,
      'y_coord' : document.getElementById("y_coord_field").innerHTML,
      'date_of_event' : $('#date_of_event').val(),
      'description' : $('#description').val(),
      'event': $('#venue_name').val(),
      'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
      'case_number': case_number,
    },
    dataType: 'json',
    success: function(response){
      if (response.date_valid) {
        document.getElementById('output_' + case_number).innerHTML = "Succesfully added record!"; /* response message */
        showCaseDetail(case_number);
        showCaseDetail(case_number);
      } else {
        var error_msg = "Please input date within time period of interest (" + response.date_start + " to " + response.date_end + ")!<br>";
        if (response.event_exist) {
          error_msg = error_msg + "Event already exist, with event date of " + response.date_of_event;
        }

        document.getElementById('output_'+case_number).innerHTML = error_msg;
      }

    },

    failure: function() {
      document.getElementById('output_' + case_number).innerHTML = "Error"; /* response message */
    }
  });
  // End of AJAX
};
