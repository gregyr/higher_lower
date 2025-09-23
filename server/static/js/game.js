document.addEventListener("DOMContentLoaded", (event) => {

const arrow = document.getElementById('arrow');
const questionMark = document.getElementById('logobig');
const product1 = document.getElementById('product1');
const product2 = document.getElementById('product2');


// Maus berührt ein Feld
product1.addEventListener('mouseenter', () => {
    arrow.style.transform = 'rotate(-180deg)';
    arrow.style.display = 'block';
    logobig.style.display = 'none';
});

product2.addEventListener('mouseenter', () => {
    arrow.style.transform = 'rotate(0deg)';
    arrow.style.display = 'block';
    logobig.style.display = 'none';
});

// Maus verlässt ein Feld
product1.addEventListener('mouseleave', () => {
    if (!product2.matches(':hover')) { // Wenn Maus NICHT über product2 ist
        arrow.style.transform = 'rotate(-90deg)';
        arrow.style.display = 'block';
        logobig.style.display = 'none';
    }
});

product2.addEventListener('mouseleave', () => {
    if (!product1.matches(':hover')) { // Wenn Maus NICHT über product1 ist
        arrow.style.transform = 'rotate(-90deg)';
        arrow.style.display = 'block';
        logobig.style.display = 'none';
    }
});



// Initialzustand
arrow.style.display = 'none';
logobig.style.display = 'block';

});