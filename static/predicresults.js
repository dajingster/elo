window.onload = function(){
  table = document.getElementById("history_table");
  all_tr = table.getElementsByTagName("tr");

  function check() {
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

check();
   var x = document.getElementById("stat").innerHTML;
   console.log(x)
   document.getElementById("bar").style.background = "linear-gradient(to right, #0F52BA" + x + "%,#FF9966" + x + "%)";

}