document.addEventListener('DOMContentLoaded', () => {
  // Select
  const filterInput = document.querySelector('#filter-input');
  const projectCards = document.querySelectorAll('.card');
  const projectCount = document.querySelector('#project-count');

  if (!filterInput || !projectCount) return;

  const totalProjects = projectCards.length;

  const updateFilter = () => {
    // Read
    const query = filterInput.value;
    let visibleCount = 0;
    const visibleTitles = [];

    projectCards.forEach((card) => {
      const titleElement = card.querySelector('h2');
      const titleText = titleElement ? titleElement.textContent : card.textContent;

      // hand-edited by KS
      const matches = titleText.toLowerCase().includes(query.toLowerCase());

      // Update - hand-edited by KS
      card.classList.toggle('is-hidden', !matches);

      if (matches) {
        visibleCount++;
        if (titleElement) {
          visibleTitles.push(titleElement.textContent.trim());
        }
      }
    });

    // Update count display
    projectCount.textContent = `Showing ${visibleCount} of ${totalProjects} projects`;

    // Stretch goal log output
    console.log(`(${visibleTitles.length})`, visibleTitles);
  };

  // Listen
  filterInput.addEventListener('input', updateFilter);

  // Initial run on page load
  updateFilter();
});