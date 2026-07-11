// =====================================================
// VWAP SUPERTREND BOT
// BYBIT CANDLE CHART
// =====================================================


let candleChart = null;



async function loadChart(){


    try{


        const res =
        await fetch("/api/candles");


        const json =
        await res.json();



        let list =
        json.result.list;



        list.reverse();



        let data = [];



        list.forEach(c=>{


            data.push({


                x:Number(c[0]),


                o:Number(c[1]),


                h:Number(c[2]),


                l:Number(c[3]),


                c:Number(c[4])


            });


        });




        drawChart(data);



    }


    catch(e){


        console.log(
            "CANDLE ERROR",
            e
        );


    }


}







function drawChart(data){



    const ctx =
    document.getElementById(
        "chart"
    );



    if(!ctx)

    return;






    if(candleChart){


        candleChart.data.datasets[0].data=data;


        candleChart.update();


        return;


    }







    candleChart = new Chart(

        ctx,


        {


        type:"candlestick",



        data:{


            datasets:[{


                label:"BTCUSDT",


                data:data


            }]


        },



        options:{


            responsive:true,


            maintainAspectRatio:false,



            scales:{


                x:{


                    type:"time"



                },


                y:{


                    position:"right"



                }



            },



            plugins:{


                legend:{


                    display:true


                }


            }


        }



        }



    );



}






setInterval(

loadChart,

5000

);



loadChart();
