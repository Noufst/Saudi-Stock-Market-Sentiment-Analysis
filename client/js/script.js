'use strict';
var ctx = document.getElementById("chart-offline-timeline").getContext("2d");
var myChart;
var Monthes = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
var valsP=[];
var valsN=[];
/* function */
function setToAll()
{
    myChart.data.labels=Monthes;
    myChart.data.datasets[0].data = valsN
    myChart.data.datasets[1].data = valsP
    myChart.update()
}
// set the dimensions of the canvas
function bar(jsonData) {
    d3.json("empty.json", function (error, data) {

        // data.forEach(function(d) {
        //     d.Letter = d.Letter;
        //     d.Freq = +d.Freq;
        // });
        data = jsonData
        console.log(data);

        var i;
        for (i = 0; i < data.length; i++) {
            if (i%2==0) {
                valsN.push(data[i]);
            }else {
                valsP.push(data[i]);
            }
        }


        //var ctx = document.getElementById("chart-0").getContext("2d");
        Chart.defaults.global.defaultFontSize = 16;
        myChart =new Chart(ctx, {
            type: 'line',
            data: {
                labels: Monthes,
                datasets: [{
                    label: "Negative",
                    fill: false,
                    backgroundColor: window.chartColors.red,
                    borderColor: window.chartColors.red,
                    data:valsN,
                }, {
                    label: "Positive",
                    fill: false,
                    backgroundColor: window.chartColors.green,
                    borderColor: window.chartColors.green,
                    //borderDash: [5, 5],
                    data: valsP,
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
                            labelString: 'Number of Tweets'
                        }
                    }]
                }
            }
        });
    });

}
function drawMonth(jsonData) {
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
        myChart.data.labels=Days;
        myChart.data.datasets[0].data = valsND
        myChart.data.datasets[1].data = valsPD
        myChart.update()
    });

}
