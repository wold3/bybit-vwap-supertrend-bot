//////////////////////////////////////////////////////
// VWAP SUPERTREND BOT
// BYBIT V5 CANDLE CHART
//////////////////////////////////////////////////////


let candleChart = null;



// ==================================================
// LOAD DATA
// ==================================================

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



        let candles = [];



        list.reverse();



        list.forEach(c=>{


            candles.push({


                x:
                Number(c[0]),



                o:
                Number(c[1]),



                h:
                Number(c[2]),



                l:
                Number(c[3]),



                c:
                Number(c[4])


            });



        });




        drawCandleChart(
            candles
        );



    }


    catch(e){


        console.log(

            "CHART ERROR",

            e

        );


    }


}









// ==================================================
// DRAW CANDLE
// ==================================================

function drawCandleChart(data){



    const canvas =

        document.getElementById(
            "chart"
        );



    if(!canvas)

        return;







    if(candleChart === null){



        candleChart = new Chart(

            canvas,

            {


            type:

            "candlestick",




            data:{


                datasets:[{


                    label:

                    "BTCUSDT",



                    data:

                    data



                }]


            },






            options:{


                responsive:true,


                maintainAspectRatio:false,



                animation:false,



                plugins:{


                    legend:{


                        display:true


                    }



                },





                scales:{



                    x:{


                        type:

                        "time",



                        time:{


                            unit:

                            "minute"



                        }



                    },



                    y:{


                        beginAtZero:false



                    }



                }





            }



        });



    }



    else{



        candleChart
        .data
        .datasets[0]
        .data = data;



        candleChart.update();



    }



}










// ==================================================
// AUTO REFRESH
// ==================================================


setInterval(

    loadChart,

    5000

);



loadChart();
