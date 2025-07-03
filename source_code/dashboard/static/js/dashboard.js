

/* FUNCTION FOR HANDLING DROPDOWN MENU */
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('profileToggle');
  const menu   = document.getElementById('profileMenu');

  toggle.addEventListener('click', e => {
    e.stopPropagation();
    const isOpen = !menu.classList.contains('hidden');
    menu.classList.toggle('hidden', isOpen);
    toggle.setAttribute('aria-expanded', String(!isOpen));
  });

  document.addEventListener('click', () => {
    if (!menu.classList.contains('hidden')) {
      menu.classList.add('hidden');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
});




