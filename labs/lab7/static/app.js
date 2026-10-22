document.addEventListener('DOMContentLoaded', () => {
  const filterInput = document.querySelector('#filter-input');
  const projectCards = document.querySelectorAll('.card');
  const projectCount = document.querySelector('#project-count');
  const projectsButton = document.querySelector('.button--primary');

  if (projectsButton) {
    projectsButton.addEventListener('click', () => {
      window.location.hash = 'projects';
    });
  }

  if (!filterInput || !projectCount) return;

  const totalProjects = projectCards.length;

  const updateFilter = () => {
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

  projectCards.forEach((card) => {
    const upvoteButton = card.querySelector('.upvote-btn');
    const likeCount = card.querySelector('.like-count');

    if (!upvoteButton || !likeCount) return;

    upvoteButton.addEventListener('click', async () => {
      const projectId = card.dataset.projectId;

      try {
        const response = await fetch(`/api/projects/${projectId}/upvote`, {
          method: 'POST',
        });
        if (!response.ok) {
          throw new Error(`Upvote request failed with status ${response.status}`);
        }

        const result = await response.json();
        likeCount.textContent = result.likes;
      } catch (error) {
        console.error('Unable to upvote project:', error);
      }
    });
  });
});
