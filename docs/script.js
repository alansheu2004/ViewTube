var form = document.getElementById("form");
const results = document.getElementById("results");
const loading = document.getElementById("loading");

google.charts.load('current', {'packages':['corechart', 'line']});
google.charts.setOnLoadCallback(drawChart);

dataString = "[]";

function drawChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Days Passed');
    data.addColumn('number', 'Predicted View Count');

    data.addRows(JSON.parse(dataString));

    var options = {
      chart: {
        title: 'Predicted View Count'
      },
      width: 400,
      height: 300,
      legend: {position: 'none'},
      series: {
        0: { color: 'red' },
      }
    };

    var chart = new google.charts.Line(results);

    chart.draw(data, google.charts.Line.convertOptions(options));
  
}


function submit() {
    loading.style.display = "inline-block";
    results.style.display = "none";

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        loading.style.display = "none";
        results.style.display = "inline-block";
        dataString = this.responseText;
        drawChart();
    }

    // xhttp.open("POST", "http://127.0.0.1:5000/get-data");
    xhttp.open("POST", "https://viewtube-5snyncdtxa-uw.a.run.app/get-data");
    xhttp.send(new FormData(form));
    console.log("sent");
}

form.addEventListener('submit', function(e) {
    e.preventDefault();
    submit();
});