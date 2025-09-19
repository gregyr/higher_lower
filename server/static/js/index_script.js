const leaderboardData = [
  { place: 1, name: "Robert", score: 15 },
  { place: 2, name: "Julia", score: 12 },
  { place: 3, name: "Timo", score: 10 },
  { place: 4, name: "Hans", score: 8 },
  { place: 5, name: "Maria", score: 5 }
];

const playerData = {place: 105, name:"gorg (Du)", score: 3}

const leaderboardContainer = document.querySelector(".leaderboard-container");

leaderboardData.forEach(item => {
  const leaderboardElement = document.createElement("div");
  leaderboardElement.classList.add("leaderboard-element");

  leaderboardElement.innerHTML = `
    <span class="leaderboard-place">${item.place}.</span>
    <span class="leaderboard-name">${item.name}</span>
    <span class="leaderboard-score">${item.score}</span>
  `;

  leaderboardContainer.appendChild(leaderboardElement);
  console.log(leaderboardElement)
});

const leaderboardElement = document.createElement("div");
  leaderboardElement.classList.add("leaderboard-element-player");

  leaderboardElement.innerHTML = `
    <span class="leaderboard-place">${playerData.place}.</span>
    <span class="leaderboard-name">${playerData.name}</span>
    <span class="leaderboard-score">${playerData.score}</span>
  `;

  leaderboardContainer.appendChild(leaderboardElement);
  console.log(leaderboardElement)

