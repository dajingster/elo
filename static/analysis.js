var mode = 0;

function rating() {
	document.getElementById("consistency").style.backgroundColor = "white";
	document.getElementById("rating").style.border = "0.1em solid #ffa500";
	document.getElementById("rating").style.backgroundColor = "#FFC760";
	document.getElementById("consistency").style.border = "";
	document.getElementById("profile").style.backgroundColor = "white";
	document.getElementById("profile").style.border = "";

	document.getElementById("profile_tab").style.display = "none";
	document.getElementById("con_tab").style.display = "none";
	document.getElementById("y-axis").innerHTML = "";
	document.getElementById("lines").innerHTML = "";
	document.getElementById("connectors").innerHTML = "";
	document.getElementById("data").innerHTML = "";


	mode = 0;

	progress = document.getElementById('progress').innerHTML;
	progress = progress.split('[').join('');
	progress = progress.split(']').join('');
	progress = progress.split(',')
	console.log(progress)

	lowest = Math.floor(document.getElementById('low').innerHTML/100)*100;

	highest = Math.ceil(document.getElementById('high').innerHTML/100)*100;

	var lines = highest/100 - lowest/100
	document.getElementById("y-axis").innerHTML += '<text x="8%" y=\"' + 5 + '%">' + highest + '</text>';

	for (i = 0; i < lines; i++) {
		var x = 100 - (i+1)*100/lines;
		var rating = highest - 100*(i+1)
		var numbers = 5 + 92*(i+1)/lines

		document.getElementById("lines").innerHTML += '<line x1="0%" x2="100%" y1=\"' + x + '%" y2=\"' + x +'%"></line>';
		document.getElementById("y-axis").innerHTML += '<text x="8%" y=\"' + numbers + '%">' + rating + '</text>';
	}

	var points = [];

	for (i = 0; i < progress.length/3; i++) {
		point = parseInt(progress[i*3 + 2])
		x = 100 - point*22/7
		y = 97 - 92*(progress[i*3]/100 - lowest/100)/lines
		points.push([x, y]);
		document.getElementById("data").innerHTML += '<g class="data" data-setname=""> <circle cx=\"' + x + '%" cy=\"' + y + '%" r="4"></circle>';
	}

	for (i = 1; i < points.length; i++) {
		var x1 = points[i][0]
		var y1 = points[i][1]
		var x2 = points[i-1][0]
		var y2 = points[i-1][1]
		document.getElementById("connectors").innerHTML += '<line x1=\"' + x1 + '%" x2=\"' + x2 + '%" y1=\"' + y1 + '%" y2=\"' + y2 +'%"></line>';
	}
	document.getElementById("chart").style.display = "";
	document.getElementById("piechart").style.display = "none";
	document.getElementById("x-axis-labels").style.display = "";
	document.getElementById("rating_tab").style.display = "";

}



function consistency() {
	document.getElementById("rating").style.backgroundColor = "white";
	document.getElementById("consistency").style.backgroundColor = "#FFC760";
	document.getElementById("consistency").style.border = "0.1em solid #ffa500";
	document.getElementById("profile").style.backgroundColor = "white";
	document.getElementById("profile").style.border = "";
	document.getElementById("rating").style.border = "";

	document.getElementById("rating_tab").style.display = "none";
	document.getElementById("profile_tab").style.display = "none";
	document.getElementById("y-axis").innerHTML = "";
	document.getElementById("lines").innerHTML = "";
	document.getElementById("connectors").innerHTML = "";
	document.getElementById("data").innerHTML = "";


	mode = 1;
	lowest = 0;

	highest = 1;

	var lines = 10;
	document.getElementById("y-axis").innerHTML += '<text x="8%" y=\"' + 5 + '%">' + highest + '</text>';

	for (i = 0; i < lines; i++) {
		var x = 100 - (i+1)*100/lines;
		var rating = (highest - 0.1*(i+1)).toFixed(1)
		var numbers = 5 + 92*(i+1)/lines

		document.getElementById("lines").innerHTML += '<line x1="0%" x2="100%" y1=\"' + x + '%" y2=\"' + x +'%"></line>';
		document.getElementById("y-axis").innerHTML += '<text x="8%" y=\"' + numbers + '%">' + rating + '</text>';
	}

	var points = [];

	for (i = 0; i < progress.length/3; i++) {
		point = parseInt(progress[i*3 + 2])
		x = 100 - point*22/7
		y = 5 + 92*(progress[i*3 + 1]/100 - lowest/100)/lines
		points.push([x, y]);
		document.getElementById("data").innerHTML += '<g class="data" data-setname=""> <circle cx=\"' + x + '%" cy=\"' + y + '%" r="4"></circle>';
	}

	for (i = 1; i < points.length; i++) {
		var x1 = points[i][0]
		var y1 = points[i][1]
		var x2 = points[i-1][0]
		var y2 = points[i-1][1]
		document.getElementById("connectors").innerHTML += '<line x1=\"' + x1 + '%" x2=\"' + x2 + '%" y1=\"' + y1 + '%" y2=\"' + y2 +'%"></line>';
	}

	document.getElementById("chart").style.display = "";
	document.getElementById("piechart").style.display = "none";
	document.getElementById("x-axis-labels").style.display = "";
	document.getElementById("con_tab").style.display = "";
}

function profile() {
	document.getElementById("rating").style.backgroundColor = "white";
	document.getElementById("consistency").style.backgroundColor = "white";
	document.getElementById("profile").style.backgroundColor = "#FFC760";
	document.getElementById("profile").style.border = "0.1em solid #ffa500";
	document.getElementById("consistency").style.border = "";
	document.getElementById("rating").style.border = "";

	document.getElementById("chart").style.display = "none";
	document.getElementById("x-axis-labels").style.display = "none";
	document.getElementById("con_tab").style.display = "none";
	document.getElementById("rating_tab").style.display = "none";
	document.getElementById("y-axis").innerHTML = "";
	document.getElementById("lines").innerHTML = "";
	document.getElementById("connectors").innerHTML = "";
	document.getElementById("data").innerHTML = "";


	mode = 2;


	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawChart);

	results = document.getElementById('game_info').innerHTML;
	results = results.split(',')
	console.log(parseInt(results[0]))
	// Draw the chart and set the chart values
	function drawChart() {
	  var data = google.visualization.arrayToDataTable([
	  ['Result', 'Games'],
	  ['Win', parseInt(results[0])],
	  ['Lose', parseInt(results[1])],
	  ['Draw', parseInt(results[2])],
	]);

	  // Optional; add a title and set the width and height of the chart
	  var options = {'title':'Result Breakdown', 'backgroundColor': { fill:'transparent' }, 'width':$(window).width()*0.7, 'height':$(window).height()*0.75, 'colors': ['#769656', '#b33430', '#a7a6a2']};

	  // Display the chart inside the <div> element with id="piechart"
	  var chart = new google.visualization.PieChart(document.getElementById('piechart'));
	  chart.draw(data, options);
	}
	document.getElementById("piechart").style.display = "";
	document.getElementById("profile_tab").style.display = "";
}


document.getElementById('rating').addEventListener('mouseover',
    rating);
document.getElementById('consistency').addEventListener('mouseover',
    consistency);
document.getElementById('profile').addEventListener('mouseover',
    profile);

window.onload = function(){
	document.getElementById("chart").style.display = "none";
	document.getElementById("x-axis-labels").style.display = "none";
}