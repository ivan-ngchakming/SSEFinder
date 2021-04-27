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
      }
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
        url: 'ajax',
        data: {
          'case_number': case_number,
        },
        dataType: 'html',
        success: function (data) {
          td.getElementsByTagName('Table')[0].innerHTML = data;
        }
      });

  } else {
    td.style.display = "none";
  }

};