window.onload = function(){
  document.getElementById("check").onchange = function() {check()};
  table = document.getElementById("history_table");
  all_tr = table.getElementsByTagName("tr");

  function check() {
      if(document.getElementById("check").checked == true){
        for (i = 0; i < all_tr.length; i++) {
          tr = all_tr[i].getElementsByTagName("td");
          for (j = 0; j < tr.length; j++) {
            td = tr[j]
            td.style.display = "";
      }
        }

        th = all_tr[0].getElementsByTagName("th");
          for (j = 0; j < th.length; j++) {
            td = th[j]
            td.style.display = "";
        }
      }
      else{
        for (i = 0; i < all_tr.length; i++) {
          tr = all_tr[i].getElementsByTagName("td");
          for (j = 0; j < tr.length; j++) {
            td = tr[j]
            if (j > 0 && j%2 == 0) {
                td.style.display = "none";
          }
        }
     }

        th = all_tr[0].getElementsByTagName("th");
          for (j = 0; j < th.length; j++) {
            td = th[j]
            if (j > 0 && j%2 == 0) {
                td.style.display = "none";
          }
        }

  }
  }

check();

}

var current_table = "history_table"

document.getElementById("search").oninput = function() {inputFunction()};
// document.getElementById("search").onblur = function() {blurFunction()};


function inputFunction() {
  var filter, table, tr, td, i;
  filter = document.getElementById("search").value.toUpperCase();
  table = document.getElementById(current_table);
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[1];
    td2 = tr[i].getElementsByTagName("td")[5];
    if (td1 || td2) {
      if (td1.innerHTML.toUpperCase().indexOf(filter) > -1 || td2.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}