// Exam tabs functionality
document.addEventListener('DOMContentLoaded', function () {
  const tabs = document.querySelectorAll('[role="tab"]');
  const tabContents = document.querySelectorAll('[role="tabpanel"]');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Deactivate all tabs
      tabs.forEach(t => {
        t.classList.remove('text-[#4584b6]', 'dark:text-[#4584b6]', 'border-[#4584b6]');
        t.classList.add('text-gray-500', 'dark:text-gray-400', 'hover:text-gray-600', 'dark:hover:text-gray-300', 'border-transparent');
        t.setAttribute('aria-selected', 'false');
      });

      // Activate clicked tab
      tab.classList.remove('text-gray-500', 'dark:text-gray-400', 'hover:text-gray-600', 'dark:hover:text-gray-300', 'border-transparent');
      tab.classList.add('text-[#4584b6]', 'dark:text-[#4584b6]', 'border-[#4584b6]');
      tab.setAttribute('aria-selected', 'true');

      // Hide all tab panels
      tabContents.forEach(content => {
        content.classList.add('hidden');
        content.classList.remove('active');
      });

      // Show selected tab panel
      const panelId = tab.getAttribute('data-tabs-target').substring(1);
      const panel = document.getElementById(panelId);
      panel.classList.remove('hidden');
      panel.classList.add('active');
    });
  });
});