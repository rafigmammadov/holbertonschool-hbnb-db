// Пример данных для мест
const places = [
    {
        name: "Beautiful Beach House",
        price: 150,
        location: "Los Angeles, United States",
    },
    {
        name: "Cozy Cabin",
        price: 100,
        location: "Toronto, Canada",
    },
    {
        name: "Modern Apartment",
        price: 200,
        location: "New York, United States",
    }
];

// Пример заполнения фильтра стран (это можно сделать динамически из API)
const countries = ["All", "United States", "Canada"];
const countryFilter = document.getElementById('country-filter');
countries.forEach(country => {
    const option = document.createElement('option');
    option.value = country.toLowerCase();
    option.textContent = country;
    countryFilter.appendChild(option);
});

// Примерный скрипт для управления отображением формы или кнопки
document.addEventListener('DOMContentLoaded', function() {
    const isAuthenticated = checkIfAuthenticated(); // Ваша функция проверки аутентификации
    const addReviewSection = document.querySelector('.reviews');

    if (isAuthenticated) {
        const reviewForm = `
            <form action="submit_review" method="post" class="add-review form">
                <label for="review">Review:</label>
                <textarea id="review" name="review" required></textarea>
                <label for="rating">Rating:</label>
                <input type="number" id="rating" name="rating" min="1" max="5" required>
                <button type="submit">Submit Review</button>
            </form>`;
        addReviewSection.insertAdjacentHTML('beforeend', reviewForm);
    } else {
        const addButton = `<a href="add_review.html" class="add-review">Add Review</a>`;
        addReviewSection.insertAdjacentHTML('beforeend', addButton);
    }
});

function checkIfAuthenticated() {
    // Здесь ваша логика для проверки аутентификации
    // Например, проверка наличия токена в cookies
    return document.cookie.includes('jwt='); // Пример
}


document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const token = getCookie('token');

    if (!token) {
        window.location.href = '/index';
    }

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;
        const placeId = getPlaceIdFromURL();

        const response = await submitReview(token, placeId, reviewText, rating);
        handleResponse(response);
    });
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

async function submitReview(token, placeId, reviewText, rating) {
    const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            user_id: getUserIdFromToken(token),
            rating: parseInt(rating),
            comment: reviewText
        })
    });
    return response;
}

function getUserIdFromToken(token) {
    // Assuming the token is a JWT and has the user ID in the payload
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id;
}

function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        document.getElementById('review-form').reset();
    } else {
        alert('Failed to submit review');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const response = await login(email, password);
        handleResponse(response);
    });
});

async function login(email, password) {
    const response = await fetch('/api/v1/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });
    return response;
}

function handleResponse(response) {
    if (response.ok) {
        response.json().then(data => {
            document.cookie = `token=${data.access_token}; path=/`;
            alert('Login successful!');
            window.location.href = '/index';
        });
    } else {
        alert('Failed to login');
    }
}
