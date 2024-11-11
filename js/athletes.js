document.addEventListener("DOMContentLoaded", function () {
  const resultsRows = document.querySelectorAll("#athlete-table .result-row");
  let labels = []; // X-axis: Race names
  let times = []; // Y-axis: Race times in minutes

  // Extract data from table
  resultsRows.forEach((row) => {
    let raceName = row.querySelector("td:first-child a").textContent.trim(); // Race name

    // Truncate race name to the first 5 words
    raceName = raceName.split(" ").slice(0, 5).join(" ");

    const timeText = row.querySelector("td:nth-child(2)").textContent.trim(); // Time (e.g., "19:21.4 SR")

    // Clean the time string (remove non-numeric characters like "SR")
    const cleanTimeText = timeText.replace(/[^0-9:.]/g, ""); // Keeps only numbers and colons
    const [minutes, seconds] = cleanTimeText.split(":").map(Number); // Split into minutes and seconds
    const timeInMinutes = minutes + seconds / 60; // Convert to decimal minutes

    labels.push(raceName); // Add truncated race name
    times.push(timeInMinutes); // Add race time in minutes
  });

  // Reverse the arrays to flip the x-axis direction
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
        labels: labels, // Reversed and truncated X-axis labels
        datasets: [
          {
            label: "Race Times (Minutes)",
            data: times, // Reversed Y-axis data
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
            color: textColor, // Dynamic title color
          },
          tooltip: {
            callbacks: {
              label: function (tooltipItem) {
                return `Time: ${tooltipItem.raw.toFixed(2)} mins`;
              },
            },
          },
          legend: {
            display: false, // Legend removed
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Races (Oldest to Newest)",
              color: textColor,
            }, // Dynamic x-axis title color
            ticks: { color: textColor }, // Dynamic x-axis labels color
            grid: { color: "rgba(200, 200, 200, 0.3)" }, // Subtle grid color
          },
          y: {
            title: { display: true, text: "Time (Minutes)", color: textColor }, // Dynamic y-axis title color
            ticks: { color: textColor, callback: (value) => `${value} mins` }, // Dynamic y-axis labels color
            grid: { color: "rgba(200, 200, 200, 0.3)" }, // Subtle grid color
          },
        },
      },
    });
  }

  // Initial rendering of the chart
  let chart = renderChart();

  // Listen for changes in the user's color preference and update the chart
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => {
      chart.destroy(); // Destroy the existing chart
      chart = renderChart(); // Re-render the chart with updated colors
    });
});
