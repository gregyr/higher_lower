document.addEventListener("DOMContentLoaded", (event) => {
  difficulties = document.querySelectorAll(".difficulty input");
  leaderboards = document.querySelectorAll(".leaderboard-container")

  difficulties.forEach((e, i) => {if (e.checked) leaderboards[i].classList.add("hidden")})
});