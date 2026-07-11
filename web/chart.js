// =====================================================
// VWAP SUPERTREND BOT
// BYBIT V5 CANDLE CHART
// =====================================================


let candleChart = null;



async function loadChart(){


    try{


        const res = await fetch(
            "/api/candles"
        );


        const json = await res.json();



        if(
            !json.result ||
            !json.result.list
        ){

            console.log(
                "NO CANDLE DATA"
            );

            return;

        }



        let list =
            json.result.list;



        list = list.reverse();



        let candles = [];



        list.forEach(c=>{


            candles.push({

                x: Number(c[0]),

                o: Number(c[1]),

                h: Number(c[2]),

                l: Number(c[3]),

                c: Number(c[4])

            });


        });




        console.log(
            "CANDLES",
            candles
        );



        drawChart(candles);



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


        candleChart.data.datasets[0].data = data;


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



            animation:false,



            parsing:false,



            scales:{


                x:{


                    type:"timeseries",



                    ticks:{


                        maxTicksLimit:10


                    }



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
