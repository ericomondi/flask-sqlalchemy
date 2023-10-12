
// Bar chart
function createChart() {
    new Chart(document.getElementById("bar-chart"), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: "Sales",
            backgroundColor:  ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
            data: remainingStock
          }
        ]
      },
      options: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Top Five Sales'
        }
      }
    });
  }
  
var labels = [];
var remainingStock = [];

// Function to fetch data from Flask route
function fetchData() {
  $.ajax({
    url: '/dashboard', 
    method: 'GET',
    success: function(listof_data) {
      // Flask route returns JSON data like this:
      // {
      //   "labels": ["Product A", "Product B", ...],
      //   "remaining_stock": [100, 200, ...]
      // }
      labels = listof_datadata.labels;
      remainingStock = listof_data.remaining_stock;

      // Create and update the chart
      createChart();
    },
    error: function() {
      console.error('Error fetching data.');
    }
  });
}

// Call fetchData() to initiate data retrieval and chart creation
fetchData();




// new Chart(document.getElementById("pie-chart"), {
// type: 'pie',
// data: {
// labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
// datasets: [{
// label: "Population (millions)",
// backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
// data: [2478,5267,734,784,433]
// }]
// },
// options: {
// title: {
// display: true,
// text: 'Predicted world population (millions) in 2050'
// }
// }
// });

// new Chart(document.getElementById("line-chart"), {
// type: 'line',
// data: {
// labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
// datasets: [{ 
// data: [86,114,106,106,107,111,133,221,783,2478],
// label: "Africa",
// borderColor: "#3e95cd",
// fill: false
// }, { 
// data: [282,350,411,502,635,809,947,1402,3700,5267],
// label: "Asia",
// borderColor: "#8e5ea2",
// fill: false
// }, { 
// data: [168,170,178,190,203,276,408,547,675,734],
// label: "Europe",
// borderColor: "#3cba9f",
// fill: false
// }, { 
// data: [40,20,10,16,24,38,74,167,508,784],
// label: "Latin America",
// borderColor: "#e8c3b9",
// fill: false
// }, { 
// data: [6,3,2,2,7,26,82,172,312,433],
// label: "North America",
// borderColor: "#c45850",
// fill: false
// }
// ]
// },
// options: {
// title: {
// display: true,
// text: 'World population per region (in millions)'
// }
// }
// });

// new Chart(document.getElementById("bar-chart"), {
//     type: 'bar',
//     data: {
//     labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
//     datasets: [
//     {
//       label: "Population (millions)",
//       backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
//       data: [2478,5267,734,784,433]
//     }
//     ]
//     },
//     options: {
//     legend: { display: false },
//     title: {
//     display: true,
//     text: 'Predicted world population (millions) in 2050'
//     }
//     }
//     });


