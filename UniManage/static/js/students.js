/* ================================================================
   UniManage – Students List Interactive Logic
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

  const searchInput = document.getElementById('searchInput');
  const filterForm  = document.getElementById('filterForm');

  /* ── 1. Debounced Live Search ──────────────────────────────── */
  if (searchInput && filterForm) {
    let debounceTimeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimeout);
      debounceTimeout = setTimeout(() => {
        filterForm.submit();
      }, 500);
    });

    // Highlight search match in table
    const query = searchInput.value.trim().toLowerCase();
    if (query) {
      document.querySelectorAll('.student-cell-name, .student-cell-email, .student-id-tag').forEach((el) => {
        const text = el.textContent;
        const idx = text.toLowerCase().indexOf(query);
        if (idx !== -1) {
          const highlighted = 
            text.substring(0, idx) +
            `<mark style="background:#fef08a;color:#854d0e;padding:1px 3px;border-radius:3px;">${text.substring(idx, idx + query.length)}</mark>` +
            text.substring(idx + query.length);
          el.innerHTML = highlighted;
        }
      });
    }
  }

  /* ── 2. Click Table Row to Navigate to Edit ────────────────── */
  document.querySelectorAll('.student-row').forEach((row) => {
    row.style.cursor = 'pointer';
    row.addEventListener('click', (e) => {
      // Don't trigger if clicking buttons, links, or checkboxes
      if (
        e.target.closest('a') ||
        e.target.closest('button') ||
        e.target.closest('input[type="checkbox"]')
      ) {
        return;
      }
      const studentId = row.dataset.id;
      if (studentId) {
        window.location.href = `/students/${studentId}/edit`;
      }
    });
  });

  /* ── 3. Quick Department Filtering on Tag Click ────────────── */
  document.querySelectorAll('.dept-tag').forEach((tag) => {
    tag.style.cursor = 'pointer';
    tag.title = 'Click to filter by this department';
    tag.addEventListener('click', (e) => {
      e.stopPropagation();
      const deptName = tag.textContent.trim();
      const select = document.querySelector('select[name="department"]');
      if (select && filterForm) {
        select.value = deptName;
        filterForm.submit();
      }
    });
  });

});

