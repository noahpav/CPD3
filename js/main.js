document.addEventListener("DOMContentLoaded", function () {
  // Create Favorites Section
  const favoriteSection = document.createElement("section");
  favoriteSection.id = "favorites-section";
  favoriteSection.innerHTML = `
        <h2>Favorites</h2>
        <ul id="favorites-list"></ul>
        <button id="clear-favorites" style="margin-top: 10px; display: none;">Clear Favorites</button>
    `;
  document.querySelector("main").prepend(favoriteSection);

  const favoriteList = document.getElementById("favorites-list");
  const clearButton = document.getElementById("clear-favorites");
  let savedFavorites = JSON.parse(localStorage.getItem("favorites")) || [];

  // Load saved favorites
  function loadFavorites() {
    favoriteList.innerHTML = ""; // Clear existing list
    savedFavorites.forEach((athlete) => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="${athlete.link}">${athlete.name}</a>`;
      favoriteList.appendChild(li);
    });

    // Toggle clear button visibilitya
    clearButton.style.display = savedFavorites.length > 0 ? "block" : "none";
  }

  loadFavorites();

  // Add favorite button to each athlete
  document.querySelectorAll("table a").forEach((link) => {
    const favoriteButton = document.createElement("button");
    favoriteButton.textContent = "⭐";
    favoriteButton.style.marginLeft = "10px";
    link.parentNode.appendChild(favoriteButton);

    favoriteButton.addEventListener("click", function () {
      const athlete = { name: link.textContent, link: link.href };

      // Check if already favorited
      const exists = savedFavorites.some((fav) => fav.link === athlete.link);
      if (!exists) {
        savedFavorites.push(athlete);
        localStorage.setItem("favorites", JSON.stringify(savedFavorites));

        const li = document.createElement("li");
        li.innerHTML = `<a href="${athlete.link}">${athlete.name}</a>`;
        favoriteList.appendChild(li);
      }

      // Ensure clear button is visible
      clearButton.style.display = "block";
    });
  });

  // Clear favorites functionality
  clearButton.addEventListener("click", function () {
    savedFavorites = [];
    localStorage.removeItem("favorites");
    loadFavorites();
  });
});
