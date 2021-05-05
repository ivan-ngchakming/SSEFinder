// Create new Case
function submitCaseForm() {
  console.log($("id_case_number").val())
  $.ajax({
    type: "POST",
    url: "ajax/add_newcase",
    data: {
      'case_number': $("#id_case_number").val(),
      'person_name': $("#id_person_name").val(),
      'identity_document_number': $("#id_identity_document_number").val(),
      'date_of_birth': $("#id_date_of_birth").val(),
      'onset_date': $("#id_onset_date").val(),
      'date_confirmed': $("#id_date_confirmed").val(),
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {
      if (data.success) {
        document.getElementById("add_new_case_output").innerHTML = "Add record success! Please wait 2s for redirect...";
        setInterval(function(){
          // wait 2 seconds before reload
          location.reload();
        }, 2000);
      } else {
        console.log("Displaying error msg: " + data.error_msg)
        document.getElementById("add_new_case_output").innerHTML = data.error_msg;
      }
    },
    error: function(data){
      document.getElementById("add_new_case_output").innerHTML = "Failed to add record!";
    },
  });
}


// Create new Attendance record
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
      console.log("Processing new record js");
      if (response.date_valid) {
        document.getElementById('output_' + case_number).innerHTML = "Succesfully added record!"; /* response message */
        showCaseDetail(case_number);
        showCaseDetail(case_number);
        document.getElementById('output_' + case_number).innerHTML = "Succesfully added record!"; /* response message */
      } else {
        var error_msg = "Please input date within time period of interest (" + response.date_start + " to " + response.date_end + ")!";
        document.getElementById('output_'+case_number).innerHTML = error_msg;
      }

    },

    failure: function() {
      document.getElementById('output_' + case_number).innerHTML = "Error"; /* response message */
    }
  });
  // End of AJAX
};
