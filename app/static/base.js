function openTab(tabname) {
  var i;
  var x = document.getElementsByClassName("tab");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(tabname).style.display = "block";

  if (tabname == "SSE_Loc") {
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
  }
};


function showCaseDetail(case_number) {
  var td = document.getElementById("case_detail_"+case_number);
  if (td.style.display == "none") {
    var all_case_detail = document.querySelectorAll('[id^="case_detail_"]')
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
         document.getElementById("x_coord_field").innerHTML = result[0]['x'];
         document.getElementById("y_coord_field").innerHTML = result[0]['y'];
         document.getElementById("address_field").innerHTML = result[0]['addressEN'];
      }
   })
};

// Check range for date
function check_form() {
    var input_date = $('#date_of_event').val()
    var onset_date = document.getElementById("onset_date").innerHTML
    var confirmed_date = document.getElementById("date_confirmed").innerHTML

    var date = new Date(onset_date);
    var startperiod = new Date(date);

    startperiod.setDate(startperiod.getDate() - 14);

    var dd = startperiod.getDate();
    var mm = startperiod.getMonth() + 1;
    var y = startperiod.getFullYear();

    var startrange = y + '-' + mm + '-' + dd;

    D_1 = input_date.split("-");
    D_2 = startrange.split("-");
    D_3 = confirmed_date.split("-");

    var d1 = new Date(D_1[2], parseInt(D_1[1]) - 1, D_1[0]);
    var d2 = new Date(D_2[2], parseInt(D_2[1]) - 1, D_2[0]);
    var d3 = new Date(D_3[2], parseInt(D_3[1]) - 1, D_3[0]);

    return(d1 < d2 || d1 > d3); // true if date lies outside range
}

function submitrecord(case_number) {
  if (check_form() == false) {
  // start of AJAX
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

       success: function(){
         document.getElementById('output').innerHTML = "Succesfully added record!"; /* response message */
         showCaseDetail(case_number);
         showCaseDetail(case_number);
       },

       failure: function() {
         document.getElementById('output').innerHTML = "Please fill in all fields!"; /* response message */
       }
   });
  }// End of AJAX
  else {
    document.getElementById('output').innerHTML = "Please input date within range!";
    document.getElementById('date_of_event').innerHTML = " ";
  }
};
