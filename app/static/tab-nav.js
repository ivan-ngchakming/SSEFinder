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

  if (tabname == "new_case_btn") {
    document.getElementById('add_new_case_btn_upper').style.display = "none";
    $.ajax({
      url: 'ajax/add_newcase',
      data: {},
      dataType: 'html',
      success: function(data){
        document.getElementById('addnewcases').innerHTML = data;
      },
    });
  } else {
    document.getElementById('add_new_case_btn_upper').style.display = "block";
  }
};
