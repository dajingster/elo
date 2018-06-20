window.onload = function(){
    var complete_table = document.getElementById("complete_table").innerHTML;
    table = document.getElementById("complete_table");
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
    	td = tr[i].getElementsByTagName("td")[0];
	    if (td) {
	      if (td.innerHTML == 1) {
	        td.style.background = "#FFD700";
	      }
	      if (td.innerHTML == 2) {
	        td.style.background = "#C0C0C0";
	      }
	      if (td.innerHTML == 3) {
	        td.style.background = "#cd7f32";
	      }
	    }
	}
	 table = document.getElementById("consistency_table");
    tr = table.getElementsByTagName("tr");
	   for (i = 1; i < tr.length; i++) {
    	td = tr[i].getElementsByTagName("td")[0];
	    if (td) {
	      if (td.innerHTML == 1) {
	        td.style.background = "#FFD700";
	      }
	      if (td.innerHTML == 2) {
	        td.style.background = "#C0C0C0";
	      }
	      if (td.innerHTML == 3) {
	        td.style.background = "#cd7f32";
	      }
	    }
	}
		table = document.getElementById("gp_table");
    tr = table.getElementsByTagName("tr");
	   for (i = 1; i < tr.length; i++) {
    	td = tr[i].getElementsByTagName("td")[0];
	    if (td) {
	      if (td.innerHTML == 1) {
	        td.style.background = "#FFD700";
	      }
	      if (td.innerHTML == 2) {
	        td.style.background = "#C0C0C0";
	      }
	      if (td.innerHTML == 3) {
	        td.style.background = "#cd7f32";
	      }
	    }
	}

};

var current_table = "complete_table"

document.getElementById("search").oninput = function() {inputFunction()};
// document.getElementById("search").onblur = function() {blurFunction()};


function inputFunction() {
  var filter, table, tr, td, i;
  filter = document.getElementById("search").value.toUpperCase();
  table = document.getElementById(current_table);
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function blurFunction() {
	// alert("blur")
    // No focus = Changes the background color of input to red
    // document.getElementById("complete_table").innerHTML = complete_table;
}




document.getElementById("consistency1").onclick = function() {c_table()};
document.getElementById("consistency2").onclick = function() {c_table()};
document.getElementById("consistency3").onclick = function() {c_table()};

document.getElementById("gp1").onclick = function() {g_table()};
document.getElementById("gp2").onclick = function() {g_table()};
document.getElementById("gp3").onclick = function() {g_table()};

document.getElementById("rating1").onclick = function() {r_table()};
document.getElementById("rating2").onclick = function() {r_table()};
document.getElementById("rating3").onclick = function() {r_table()};

function c_table() {
		document.getElementById("consistency_table").style.display = "table";
		document.getElementById("complete_table").style.display = "none";
		document.getElementById("gp_table").style.display = "none";
		current_table = "consistency_table"
}

function g_table() {
		document.getElementById("consistency_table").style.display = "none";
		document.getElementById("gp_table").style.display = "table";
		document.getElementById("complete_table").style.display = "none";
		current_table = "gp_table"
}

function r_table() {
		document.getElementById("consistency_table").style.display = "none";
		document.getElementById("gp_table").style.display = "none";
		document.getElementById("complete_table").style.display = "table";
		current_table = "complete_table"
}