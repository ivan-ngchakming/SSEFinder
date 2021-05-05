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
        },
        error: function(data){
          alert("Failed to add record!");
        },
      });
    });
  });

  if (tabname == "new_case_btn") {
    case_id = document.querySelectorAll('[id^="case_detail_"]').length + 1
    $.ajax({
      url: 'ajax/add_newcase',
      data: {
        'case_id': case_id,
      },
      dataType: 'html',
      success: function(data){
        document.getElementById('addnewcases').innerHTML = data;
        document.getElementById('id_case_number').defaultValue = case_id;
        document.getElementById('id_case_number').disabled = true;
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

