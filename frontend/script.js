// change navbar style on scroll

window.addEventListener('scroll', () =>{
    document.querySelector('nav').classList.toggle('window-scroll', window.scrollY > 0 )
})

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Slick Slider initialization
$(document).ready(function(){
    $('.features-slider').slick({
        infinite: true,
        slidesToShow: 3, // Adjust number of slides shown at once
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        arrows: true,  // Adds the arrows for navigation
        dots: true,    // Adds the pagination dots
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1 // Show 1 slide on smaller screens
                }
            }
        ]
    });
});