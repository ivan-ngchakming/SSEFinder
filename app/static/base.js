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
          addrecord();
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

function addrecord() {
  $.ajax({
      url: 'ajax/showrecordform',
      data: {

      },
      dataType: 'html',
      success: function (data) {
        document.getElementById('RecordBox').innerHTML = data;
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        document.getElementById('RecordBox').innerHTML = "Error";
      },
    });
};

function searchcoord() {
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

function submitrecord(case_classification) {
  console.log(case_classification);
  $.ajax({
       type : "POST",
       url: 'ajax/showrecordform',
       data: {
        venue_name : $('#venue_name').val(),
        venue_location : $('#venue_location').val(),
        address : document.getElementById("address_field").innerHTML,
        x_coord : document.getElementById("x_coord_field").innerHTML,
        y_coord : document.getElementById("y_coord_field").innerHTML,
        date_of_event : $('#date_of_event').val(),
        description : $('#description').val(),
        event: $('#venue_name').val(),
        // case: case_classification,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        action: 'post',

       },

       success: function(){
         document.getElementById('output').innerHTML = "Succesfully added record!"; /* response message */
       },

       failure: function() {
         document.getElementById('output').innerHTML = "Please fill in all fields!"; /* response message */
       }
   });
};
