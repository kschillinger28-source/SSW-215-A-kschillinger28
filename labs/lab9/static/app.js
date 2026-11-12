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

  if (filterInput && projectCount) {
    const totalProjects = projectCards.length;

    const updateFilter = () => {
      const query = filterInput.value;
      let visibleCount = 0;
      const visibleTitles = [];

      projectCards.forEach((card) => {
        const titleElement = card.querySelector('h2');
        const titleText = titleElement ? titleElement.textContent : card.textContent;

        const matches = titleText.toLowerCase().includes(query.toLowerCase());
        card.classList.toggle('is-hidden', !matches);

        if (matches) {
          visibleCount++;
          if (titleElement) {
            visibleTitles.push(titleElement.textContent.trim());
          }
        }
      });

      projectCount.textContent = `Showing ${visibleCount} of ${totalProjects} projects`;
      console.log(`(${visibleTitles.length})`, visibleTitles);
    };

    filterInput.addEventListener('input', updateFilter);
    updateFilter();
  }

  // Handle Upvotes
  document.querySelectorAll('.card').forEach((card) => {
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

  // Handle Adding a New Project over the Network (Part 5 Stretch)
  const newTitleInput = document.querySelector('#new-title');
  const addProjectBtn = newTitleInput ? newTitleInput.nextElementSibling : null;

  if (newTitleInput && addProjectBtn) {
    addProjectBtn.addEventListener('click', async () => {
      const title = newTitleInput.value.trim();

      try {
        const response = await fetch('/api/projects', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ title }),
        });

        if (response.status === 201) {
          window.location.reload();
        } else {
          console.error('Server rejected project creation with status:', response.status);
        }
      } catch (error) {
        console.error('Network error while creating project:', error);
      }
    });
  }
});