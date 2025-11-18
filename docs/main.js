document.addEventListener('DOMContentLoaded', () => {
  const menuScreen = document.querySelector('.menu-screen');
  const openMenuButton = document.querySelector('.menu-open');
  const closeMenuButton = document.querySelector('.menu-close');
  const menuBackdrop = document.querySelector('.menu-backdrop');

  function openMenu() {
    menuScreen.classList.add('is-open');
    menuScreen.setAttribute('aria-hidden', 'false');
  }

  function closeMenu() {
    menuScreen.classList.remove('is-open');
    menuScreen.setAttribute('aria-hidden', 'true');
  }

  openMenuButton.addEventListener('click', openMenu);
  closeMenuButton.addEventListener('click', closeMenu);

  // Клик по затемнению справа — закрыть меню
  if (menuBackdrop) {
    menuBackdrop.addEventListener('click', closeMenu);
  }

  // Закрытие по Escape
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });
});

