/* ================================================================
   UniManage – Main Global JavaScript
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. Responsive Sidebar Toggle & Collapse ──────────────── */
  const sidebar       = document.getElementById('sidebar');
  const toggleBtn     = document.getElementById('sidebarToggle');
  const overlay       = document.getElementById('sidebarOverlay');
  const isMobile      = () => window.innerWidth <= 768;

  function toggleSidebar() {
    if (isMobile()) {
      const isOpen = sidebar.classList.contains('mobile-open');
      if (isOpen) {
        sidebar.classList.remove('mobile-open');
        overlay?.classList.remove('active');
        document.body.style.overflow = '';
      } else {
        sidebar.classList.add('mobile-open');
        overlay?.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    } else {
      sidebar.classList.toggle('collapsed');
      localStorage.setItem('unimanage_collapsed', sidebar.classList.contains('collapsed') ? '1' : '0');
    }
  }

  toggleBtn?.addEventListener('click', toggleSidebar);
  overlay?.addEventListener('click', () => {
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  });

  // Restore desktop collapsed state
  if (!isMobile() && localStorage.getItem('unimanage_collapsed') === '1') {
    sidebar.classList.add('collapsed');
  }

  window.addEventListener('resize', () => {
    if (!isMobile()) {
      sidebar.classList.remove('mobile-open');
      overlay?.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  /* ── 2. Toast Notifications Auto-Dismiss ───────────────────── */
  const toasts = document.querySelectorAll('.toast-notification');
  toasts.forEach((toast, idx) => {
    setTimeout(() => {
      toast.style.transition = 'all 0.3s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 4500 + idx * 500);
  });

  /* ── 3. Topbar Quick Search ────────────────────────────────── */
  const globalSearch = document.getElementById('globalSearch');
  if (globalSearch) {
    globalSearch.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const query = globalSearch.value.trim();
        if (query) {
          window.location.href = `/students?q=${encodeURIComponent(query)}`;
        }
      }
    });
  }

  // Ctrl+K Shortcut to focus search
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const targetInput = globalSearch || document.getElementById('searchInput');
      targetInput?.focus();
    }
  });

  /* ── 4. Animated Counters for Stat Cards ───────────────────── */
  function animateCounter(el, target, duration = 1200) {
    const startVal = 0;
    const startTime = performance.now();

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // easeOutCubic
      const ease = 1 - Math.pow(1 - progress, 3);
      const currentVal = Math.round(startVal + (target - startVal) * ease);
      el.textContent = currentVal.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = target.toLocaleString();
      }
    }
    requestAnimationFrame(update);
  }

  document.querySelectorAll('[data-count]').forEach((el) => {
    const val = parseInt(el.getAttribute('data-count'), 10);
    if (!isNaN(val)) {
      animateCounter(el, val);
    }
  });

  /* ── 5. Select All Checkbox ────────────────────────────────── */
  const selectAll = document.getElementById('selectAll');
  if (selectAll) {
    selectAll.addEventListener('change', () => {
      const checkboxes = document.querySelectorAll('.row-check');
      checkboxes.forEach((cb) => {
        cb.checked = selectAll.checked;
      });
    });
  }

  /* ── 6. Client Table Sorting ───────────────────────────────── */
  const table = document.getElementById('studentsTable');
  if (table) {
    const headers = table.querySelectorAll('th.sortable');
    headers.forEach((th, colIdx) => {
      th.addEventListener('click', () => {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAsc = th.dataset.sortDir !== 'asc';

        // Reset indicator on other headers
        headers.forEach((h) => {
          delete h.dataset.sortDir;
          const arrow = h.querySelector('.sort-arrow');
          if (arrow) arrow.remove();
        });

        th.dataset.sortDir = isAsc ? 'asc' : 'desc';
        const arrow = document.createElement('span');
        arrow.className = 'sort-arrow ms-1';
        arrow.innerHTML = isAsc ? '▲' : '▼';
        arrow.style.fontSize = '10px';
        th.appendChild(arrow);

        rows.sort((a, b) => {
          const aText = a.children[colIdx]?.innerText.trim() || '';
          const bText = b.children[colIdx]?.innerText.trim() || '';
          return isAsc ? aText.localeCompare(bText) : bText.localeCompare(aText);
        });

        rows.forEach((row) => tbody.appendChild(row));
      });
    });
  }

  /* ── 7. Submit Button Loading Indicator ────────────────────── */
  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn && !form.classList.contains('has-error')) {
        setTimeout(() => {
          btn.disabled = true;
          const original = btn.innerHTML;
          btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Saving...`;
          setTimeout(() => {
            btn.disabled = false;
            btn.innerHTML = original;
          }, 8000);
        }, 20);
      }
    });
  });

});

