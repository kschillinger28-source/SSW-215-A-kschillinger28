document.addEventListener('DOMContentLoaded', () => {
  const primaryButton = document.querySelector('.button--primary');
  const projects = document.querySelector('.projects');

  if (!primaryButton || !projects) {
    return;
  }

  const setExpanded = (isExpanded) => {
    projects.classList.toggle('is-expanded', isExpanded);
    primaryButton.classList.toggle('is-expanded', isExpanded);
    primaryButton.setAttribute('aria-expanded', String(isExpanded));
  };

  setExpanded(false);

  primaryButton.addEventListener('click', (event) => {
    event.preventDefault();
    const nextExpanded = !projects.classList.contains('is-expanded');
    setExpanded(nextExpanded);

    if (nextExpanded) {
      projects.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
