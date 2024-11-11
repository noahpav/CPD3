document.addEventListener("DOMContentLoaded", function () {
  const resultsRows = document.querySelectorAll("#athlete-table .result-row");
  let labels = []; // X-axis: Race names
  let times = []; // Y-axis: Race times in minutes

  // Extract data from table
  resultsRows.forEach((row) => {
    let raceName = row.querySelector("td:first-child a").textContent.trim();
    raceName = raceName.split(" ").slice(0, 4).join(" ");

    const timeText = row.querySelector("td:nth-child(2)").textContent.trim();

    // Clean the time string (remove non-numeric characters like "SR")
    const cleanTimeText = timeText.replace(/[^0-9:.]/g, "");
    const [minutes, seconds] = cleanTimeText.split(":").map(Number);
    const timeInMinutes = minutes + seconds / 60;

    labels.push(raceName);
    times.push(timeInMinutes);
  });

  labels.reverse();
  times.reverse();

  // Function to render the chart with dynamic colors
  function renderChart() {
    const prefersDarkMode = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const textColor = prefersDarkMode ? "#8ccbeb" : "#2e2e2e";

    const ctx = document.getElementById("resultsChart").getContext("2d");
    return new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Race Times (Minutes)",
            data: times,
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            pointBackgroundColor: "rgba(75, 192, 192, 1)",
            pointBorderColor: "#fff",
            pointRadius: 5,
            hoverRadius: 7,
            tension: 0.4,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Athlete Race Times",
            font: { size: 18, family: "Arial", weight: "bold" },
            color: textColor,
          },
          tooltip: {
            callbacks: {
              label: function (tooltipItem) {
                return `Time: ${tooltipItem.raw.toFixed(2)} mins`;
              },
            },
          },
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Races (Oldest to Newest)",
              color: textColor, // Dynamic x-axis title color
            },
            ticks: {
              color: textColor, // Dynamic x-axis labels color
            },
            grid: {
              color: "rgba(200, 200, 200, 0.3)", // Subtle grid color
            },
          },
          y: {
            title: { display: true, text: "Time (MM:SS)", color: textColor }, // Update axis title
            ticks: {
              color: textColor,
              stepSize: 0.25, // 15 seconds = 0.25 minutes
              callback: (value) => {
                const totalSeconds = Math.round(value * 60); // Convert minutes to total seconds
                const minutes = Math.floor(totalSeconds / 60); // Get whole minutes
                const seconds = totalSeconds % 60; // Get remaining seconds
                return `${minutes}:${seconds.toString().padStart(2, "0")}`; // Format as MM:SS
              },
            },
            grid: { color: "rgba(200, 200, 200, 0.3)" },
          },
        },
      },
    });
  }

  let chart = renderChart();

  // Listen for changes in the user's color preference
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => {
      chart.destroy();
      chart = renderChart();
    });
});
