const arrow = document.getElementById('arrow');
const questionMark = document.getElementById('questionMark');
const product1 = document.getElementById('product1');
const product2 = document.getElementById('product2');


// Maus berührt ein Feld
product1.addEventListener('mouseenter', () => {
    arrow.style.transform = 'rotate(0deg)';
    arrow.style.display = 'block';
    questionMark.style.display = 'none';
});

product2.addEventListener('mouseenter', () => {
    arrow.style.transform = 'rotate(180deg)';
    arrow.style.display = 'block';
    questionMark.style.display = 'none';
});

// Maus berührt kein Feld:
document.addEventListener('mousemove', (event) => {
    const rect1 = product1.getBoundingClientRect();
    const rect2 = product2.getBoundingClientRect();
});

// Initialzustand
arrow.style.display = 'none';
questionMark.style.display = 'block';
