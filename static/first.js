// JavaScript to show/hide the desktop navigation bar based on scrolling
window.addEventListener('scroll', function () {
    const desktopNavbar = document.getElementById('desktop-navbar');
    const mNavbar = document.getElementById('mobile');
    const scrollY = window.scrollY;
    const maxScroll = window.innerHeight * 0.3;
    const sscroll = window.innerHeight * 0.2; // Adjusted to 60% of the page

    if (scrollY >= maxScroll) {
      desktopNavbar.classList.add('show');
    } else {
      desktopNavbar.classList.remove('show');
    }

    if (scrollY >= sscroll) {
      mNavbar.classList.add('show'); // Add the 'show' class to display the desktop navigation bar
    } else {
      mNavbar.classList.remove('show'); // Remove the 'show' class to hide the desktop navigation bar
    }
  });

  // Call the resize event listener on page load to handle initial display
  window.addEventListener('DOMContentLoaded', function () {
    window.dispatchEvent(new Event('resize'));
  });

  document.addEventListener('DOMContentLoaded', function () {
    const menuIcon = document.querySelector('.menu-icon');
    const hiddenMenu = document.querySelector('.hidden-menu');

    menuIcon.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent the default behavior of the anchor tag
        // Toggle the 'show' class on the hidden menu
        hiddenMenu.classList.toggle('show');
    });
  });