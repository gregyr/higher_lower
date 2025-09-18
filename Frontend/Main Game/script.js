const arrow = document.getElementById('arrow');
const questionMark = document.getElementById('questionMark');
const product1 = document.getElementById('product1');
const product2 = document.getElementById('product2');


// Maus berührt ein Feld
product1.addEventListener('mouseenter', () => {
    arrow.style.transform = 'rotate(180deg)';
    arrow.style.display = 'block';
    questionMark.style.display = 'none';
});

product2.addEventListener('mouseenter', () => {
    arrow.style.transform = 'rotate(0deg)';
    arrow.style.display = 'block';
    questionMark.style.display = 'none';
});

product1.addEventListener('mouseleave', () => {
    arrow.style.display = 'none';
    questionMark.style.display = 'block';
});

product2.addEventListener('mouseleave', () => {
    arrow.style.display = 'none';
    questionMark.style.display = 'block';
});

// Maus berührt kein Feld:
document.addEventListener('mousemove', (event) => {
    const rect1 = product1.getBoundingClientRect();
    const rect2 = product2.getBoundingClientRect();

    if (!(event.clientX >= rect1.left && event.clientX <= rect1.right && event.clientY >= rect1.top && event.clientY <= rect1.bottom) &&
        !(event.clientX >= rect2.left && event.clientX <= rect2.right && event.clientY >= rect2.top && event.clientY <= rect2.bottom)) {
        arrow.style.display = 'none';
        questionMark.style.display = 'block';
    }
});

// Initialzustand
arrow.style.display = 'none';
questionMark.style.display = 'block';