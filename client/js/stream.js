
function draw_online_timeline(){
    // Declare an EventSource
    const eventSource = new EventSource('http://127.0.0.1:5000/liveChart2');
    const date = moment();

    //var d = Date(Date.now());
    // Converting the number of millisecond in date string 
    a = date.format('MMMM Do YYYY, h:mm:ss a'); 
    // Printing the current date  
    document.getElementById("timeline_date").innerHTML = "<b>Streamaing since:</b> " + a;

    var ctx = document.getElementById("chart-online-timeline").getContext("2d");
    var myChart;
    var Time = []
    var valsP=[];
    var valsN=[];
    var pervValue="no";
    var nextValue=900;
    var moreThan60=0;
    var pCounter=0;
    var today = new Date();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    Time.push("start")
    valsP.push(0)
    valsN.push(0)
    myChart =new Chart(ctx, {
        type: 'line',
        data: {
            labels: Time,
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
                        labelString: 'Time'
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



    // Handler for events
    eventSource.onmessage = (e) => {
        var data = JSON.parse(e.data);
        seconds=data.date.split(":");
        realSecond=parseInt(seconds[2])
        if (nextValue==900) {
            nextValue=parseInt(seconds[2])
            nextValue=nextValue+10
            if (nextValue>60) {
                moreThan60=nextValue
                nextValue=nextValue-60
            }else if (nextValue==60)
            {
                nextValue=1
            }
            Time.push(data.date)
            if (data.sentiment == "1") {
                valsP.push(1)
                valsN.push(0)
            } else  {
                valsN.push(1)
                valsP.push(0)
            }
        }else if (nextValue<=realSecond) {
            if (moreThan60!=0 && realSecond>=51 ) {
                if (data.sentiment == "1") {
                    valsP.push(valsP.pop()+1)
                } else  {
                    valsN.push(valsN.pop()+1)
                }
            }else {
                Time.push(data.date)
                nextValue=parseInt(seconds[2])
                nextValue=nextValue+10
                if (nextValue>60) {
                    moreThan60=nextValue
                    nextValue=nextValue-60
                }else if (nextValue==60)
                {
                    nextValue=1
                    moreThan60=0
                }else {
                    moreThan60=0
                }
                if (data.sentiment == "1") {
                    valsP.push(1)
                    valsN.push(0)
                } else  {
                    valsN.push(1)
                    valsP.push(0)
                }
            }
        }else {
            if (data.sentiment == "1") {
                valsP.push(valsP.pop()+1)
            } else  {
                valsN.push(valsN.pop()+1)
            }
        }

        myChart.data.labels=Time;
        myChart.data.datasets[0].data = valsN
        myChart.data.datasets[1].data = valsP
        myChart.update()

    };
}