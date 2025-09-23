var arrow = document.getElementById('arrow');
var logobig = document.getElementById('logobig');
var arrow_container = document.getElementsByClassName('arrow-container')[0]
var product1 = document.getElementsByClassName('product-box')[0];
var product2 = document.getElementsByClassName('product-box')[1];

document.addEventListener("DOMContentLoaded", (event) => {
    setup();
});

async function send_guess() {
    //console.log(this.getAttribute('user_guess'))
    await fetch("/guess", {
        method: 'POST',
        redirect: 'follow',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ guess: this.getAttribute('user_guess') })
    }).then(response => {
        console.log(response.status)
        if (response.redirected) {
            window.location.href = response.url;
        }
        return response.json();
    }).then(response => {
        document.querySelectorAll('.price')[1].textContent = `Preis: ${response.productLast_price} €`
        //console.log(response)
        if (response.correct) {
            load_next_product(response);
        }
        else {
            game_over();
        }
    });
}

function load_next_product(response) {
    product1.remove();
    moveDown(arrow_container);
    product2.removeEventListener('mouseenter', enter_rotate);
    product2.removeEventListener('mouseleave', leave_rotate);
    product2.removeEventListener('click', send_guess);

    document.querySelector('.product-container').insertAdjacentHTML('beforeend', `<div class="product-box">
                    <img class="product-image" src=${response.productNext_high_q_img} alt="Produkt">
                    <div class="text-box">
                        <h2>${response.productNext_brand}</h2>
                        <h3>${response.productNext_name}</h3>
                        <p class="price">Preis: ${response.productNext_price} €</p>
                        <p>lieferbar - in 2-3 Werktagen bei dir</p>
                        <img alt="Logo" class="UpLogo" src="/static/images/otto-up-logo.png">
                    </div>
                </div>`);

    setup();
}

function moveDown(element) {
  if(element.nextElementSibling)
    element.parentNode.insertBefore(element.nextElementSibling, element);
}

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function setup() {
    arrow = document.getElementById('arrow');
    logobig = document.getElementById('logobig');
    arrow_container = document.getElementsByClassName('arrow-container')[0]
    product1 = document.getElementsByClassName('product-box')[0];
    product2 = document.getElementsByClassName('product-box')[1];

    product1.setAttribute('rotation', '-180');
    product2.setAttribute('rotation', '0');

    product1.setAttribute('user_guess', 'lower');
    product2.setAttribute('user_guess', 'higher');

    // Initialzustand
    arrow.style.display = 'none';
    logobig.style.display = 'block';

    // Maus berührt ein Feld
    product1.addEventListener('mouseenter', enter_rotate);
    product2.addEventListener('mouseenter', enter_rotate);

    // Maus verlässt ein Feld
    product1.addEventListener('mouseleave', leave_rotate);
    product2.addEventListener('mouseleave', leave_rotate);

    product1.addEventListener('click', send_guess);
    product2.addEventListener('click', send_guess);
}

function enter_rotate() {
    rotation = this.getAttribute('rotation')
    arrow.style.transform = `rotate(${rotation}deg)`;
    arrow.style.display = 'block';
    logobig.style.display = 'none';
}

function leave_rotate() {
    arrow.style.transform = 'rotate(-90deg)';
    arrow.style.display = 'block';
    logobig.style.display = 'none';
}

function game_over() {
    product1.removeEventListener('mouseenter', enter_rotate);
    product1.removeEventListener('mouseleave', leave_rotate);
    product1.removeEventListener('click', send_guess);

    product2.removeEventListener('mouseenter', enter_rotate);
    product2.removeEventListener('mouseleave', leave_rotate);
    product2.removeEventListener('click', send_guess);
}