// Select the cart button and add an event listener to it
const cartButton = document.getElementById('cart-button');
// Add an event listener to the "Add to Cart" button
const addToCartButton = document.querySelector('.add-to-cart');
addToCartButton.addEventListener('click', (event) => {
  event.preventDefault();

  // Send an AJAX request to the server to add the product to the cart
  const productId = event.target.dataset.productId;
  fetch(`/cart/add/${productId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: JSON.stringify({}),
  })
    .then(response => response.json())
    .then(data => {
      // Update the cart count on the page
      cartButton.textContent = `Cart (${data.cart_count})`;
    });
});
