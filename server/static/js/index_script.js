document.addEventListener("DOMContentLoaded", (event) => {
    difficulties = document.querySelectorAll(".difficulty input");
    show_selected_board();
});

function show_selected_board() {
    difficulties = document.querySelectorAll(".difficulty input");
    leaderboards = document.querySelectorAll(".leaderboard-container")

    leaderboards.forEach((e) => e.classList.add("hidden"))
    difficulties.forEach((e, i) => {if (e.checked) leaderboards[i].classList.remove("hidden")})
}