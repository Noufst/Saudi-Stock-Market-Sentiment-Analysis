'use strict';
var ctxAramco = document.getElementById("chart-offline-aramco-timeline").getContext("2d");
var myChartAramco;
var Monthes = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
var valsPAramco=[];
var valsNAramco=[];
/* function */
function setToAllAramco()
{
  myChartAramco.data.labels=Monthes;
  myChartAramco.data.datasets[0].data = valsNAramco
  myChartAramco.data.datasets[1].data = valsPAramco
  myChartAramco.update()
}
// set the dimensions of the canvas
function aramcoMonthes(jsonData) {
  d3.json("empty.json", function (error, data) {

      // data.forEach(function(d) {
      //     d.Letter = d.Letter;
      //     d.Freq = +d.Freq;
      // });
      data = jsonData
      console.log(data);
data.splice(3, 0, 0);
data.splice(8, 0, 0);
data.splice(10, 0, 0);

    var i;
for (i = 0; i < data.length; i++) {
  if (i%2==0) {
    valsNAramco.push(data[i]);
  }else {
    valsPAramco.push(data[i]);
  }
}


//var ctx = document.getElementById("chart-0").getContext("2d");
myChartAramco =new Chart(ctxAramco, {
type: 'line',
data: {
labels: Monthes,
datasets: [{
label: "Negative",
fill: false,
backgroundColor: window.chartColors.red,
borderColor: window.chartColors.red,
data:valsNAramco,
}, {
label: "Positive",
fill: false,
backgroundColor: window.chartColors.green,
borderColor: window.chartColors.green,
//borderDash: [5, 5],
data: valsPAramco,
}]
},
options: {
responsive: true,
title:{
display:false
},
tooltips: {
mode: 'index',
intersect: false,
},
hover: {
mode: 'nearest',
intersect: true
},
scales: {
xAxes: [{
display: true,
scaleLabel: {
  display: true,
  labelString: 'Month'
}
}],
yAxes: [{
display: true,
scaleLabel: {
  display: true,
  labelString: 'Value'
}
}]
}
}
});
});

}
function drawMonthAramco(jsonData) {
  d3.json("empty.json", function (error, data) {

      // data.forEach(function(d) {
      //     d.Letter = d.Letter;
      //     d.Freq = +d.Freq;
      // });
      data = jsonData
      console.log(data);
      var entries = d3.nest()
   .key(function(d) { return d.dateDay; })
   .key(function(d) { return d.sentiment; })
   .entries(data);
console.log(entries);
var Days = entries.map(a => a.key);
var values = entries.map(a => a.values);
console.log(Monthes);
console.log("sentiment"+values);

var valsPD=[];
var valsND=[];
for(var item of values){
  console.log("item"+item.length);
 for(var i of item)
 {
   console.log(i);
   if (i.key=="0") {
     valsND.push(i.values.length);
     console.log(i.values.length);
     if (item.length==1) {
         valsPD.push(0);
       }
   }else  if (i.key=="1") {
     valsPD.push(i.values.length);
     if (item.length==1) {
         valsND.push(0);
       }
   }
 }
}
myChartAramco.data.labels=Days;
myChartAramco.data.datasets[0].data = valsND
myChartAramco.data.datasets[1].data = valsPD
myChartAramco.update()
});

}
