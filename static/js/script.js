const toggler = document.getElementById('navbar-toggler');const navbarNav = document.getElementById('navbarNav');
toggler.addEventListener('click', () => {
navbarNav.classList.toggle('show');
toggler.innerHTML = navbarNav.classList.contains('show') ? '<span class="lni lni-close"></span>' : '<span class="navbar-toggler-icon"></span>';});
    
document.querySelectorAll('.dropdown-submenu > a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.stopPropagation(); // Prevent the click from closing the entire dropdown
        e.preventDefault();
        const submenu = this.nextElementSibling;
        submenu.classList.toggle('show');
    });
});
 
document.addEventListener('click', function(e) {
if (!e.target.closest('.dropdown-submenu')) {
    document.querySelectorAll('.dropdown-submenu .dropdown-menu.show').forEach(submenu => submenu.classList.remove('show'));
}});


// CUSTOM INDICATOR FOR CAROUSEL
const carousel = document.getElementById('churchCarousel');
      const indicators = document.querySelectorAll('.custom-indicator');
      
      carousel.addEventListener('slid.bs.carousel', function() {
        const activeIndex = Array.from(document.querySelectorAll('.carousel-item')).findIndex(item => 
          item.classList.contains('active')
        );
        
        indicators.forEach((indicator, index) => {
          if (index === activeIndex) {
            indicator.classList.add('active');
          } else {
            indicator.classList.remove('active');
          }
        });
      });
      
      // Add click handlers for custom indicators
indicators.forEach(indicator => {
indicator.addEventListener('click', function() {
    const targetSlide = this.getAttribute('data-bs-slide-to');
    const carousel = new bootstrap.Carousel(document.getElementById('churchCarousel'));
    carousel.to(targetSlide);
});
});


// SCROLL REVEAL ANIMATION
const sermonCarousel = document.getElementById('sermonCarousel');
        const paginationText = document.getElementById('paginationText');
        const totalItems = 3;

        function updatePagination() {
            const activeIndex = Array.from(carousel.querySelectorAll('.carousel-item')).findIndex(item => item.classList.contains('active')) + 1;
            paginationText.innerHTML = `◄ ${activeIndex} ${activeIndex + 1 > totalItems ? '' : activeIndex + 1} ... 14 15 ►`;
        }

        sermonCarousel.addEventListener('slid.bs.carousel', updatePagination);
        updatePagination(); // Initial update



// GALLERY VIEW 
const images = document.querySelectorAll('.gallery-img');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const downloadBtn = document.getElementById('downloadBtn');

  let currentIndex = 0;

  images.forEach((img, index) => {
    img.addEventListener('click', () => {
      currentIndex = index;
      showImage(img.dataset.full);
    });
  });

  function showImage(src) {
    lightboxImg.src = src;
    downloadBtn.href = src;
    lightbox.style.display = 'flex';
  }

  function closeLightbox() {
    lightbox.style.display = 'none';
    lightboxImg.src = '';
  }

  function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    showImage(images[currentIndex].dataset.full);
  }

  function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(images[currentIndex].dataset.full);
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') nextImage();
    if (e.key === 'ArrowLeft') prevImage();
  });