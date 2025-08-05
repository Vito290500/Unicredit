document.addEventListener('DOMContentLoaded', () => {
  console.log('navbar.js loaded');
  const profileToggle = document.getElementById('profileToggle');
  const profileMenu = document.getElementById('profileMenu');
  console.log('profileToggle:', profileToggle);
  console.log('profileMenu:', profileMenu);
  if (profileToggle && profileMenu) {
    profileToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      const isOpen = !profileMenu.classList.contains('hidden');
      profileMenu.classList.toggle('hidden', !isOpen); // Invertito per mostrare/nascondere correttamente
      profileToggle.setAttribute('aria-expanded', String(!isOpen));
      console.log('profileToggle clicked, menu toggled');
    });
    document.addEventListener('click', function() {
      if (!profileMenu.classList.contains('hidden')) {
        profileMenu.classList.add('hidden');
        profileToggle.setAttribute('aria-expanded', 'false');
        console.log('document clicked, menu hidden');
      }
    });
  } else {
    console.error('profileToggle or profileMenu not found in DOM');
  }
});
