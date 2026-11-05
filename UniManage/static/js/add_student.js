/* ================================================================
   UniManage – Add / Edit Student Interactive Logic
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

  const avatarInput   = document.getElementById('avatarInput');
  const avatarPreview = document.getElementById('avatarPreview');

  const fullNameInput  = document.getElementById('fullNameInput');
  const studentIdInput = document.getElementById('studentIdInput');
  const deptSelect     = document.getElementById('deptSelect');

  const previewName = document.getElementById('previewName');
  const previewId   = document.getElementById('previewId');
  const previewDept = document.getElementById('previewDept');

  /* ── 1. Avatar Upload & Live Preview ───────────────────────── */
  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;

      // 5MB limit check
      if (file.size > 5 * 1024 * 1024) {
        alert('File size exceeds 5MB limit. Please choose a smaller image.');
        avatarInput.value = '';
        return;
      }

      const reader = new FileReader();
      reader.onload = (event) => {
        avatarPreview.src = event.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  /* ── 2. Live Student ID Card Sync ──────────────────────────── */
  function updateCardPreview() {
    if (previewName && fullNameInput) {
      previewName.textContent = fullNameInput.value.trim() || 'Full Name';
    }
    if (previewId && studentIdInput) {
      previewId.textContent = studentIdInput.value.trim() || 'Student ID';
    }
    if (previewDept && deptSelect) {
      const selectedText = deptSelect.options[deptSelect.selectedIndex]?.text;
      previewDept.textContent = (deptSelect.value ? selectedText : '') || 'Department';
    }
  }

  fullNameInput?.addEventListener('input', updateCardPreview);
  studentIdInput?.addEventListener('input', updateCardPreview);
  deptSelect?.addEventListener('change', updateCardPreview);

  // Initial call
  updateCardPreview();

  /* ── 3. Client-side Form Validation ────────────────────────── */
  const form = document.getElementById('addStudentForm') || document.getElementById('editStudentForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      let hasError = false;

      // Clear existing errors
      form.querySelectorAll('.field-error-client').forEach((el) => el.remove());
      form.querySelectorAll('.has-error-client').forEach((el) => el.classList.remove('has-error-client'));

      const requiredFields = form.querySelectorAll('[required]');
      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          hasError = true;
          field.closest('.form-group-custom')?.classList.add('has-error-client');
          const errorMsg = document.createElement('span');
          errorMsg.className = 'field-error field-error-client';
          errorMsg.textContent = 'This field is required.';
          field.closest('.form-group-custom')?.appendChild(errorMsg);
        }
      });

      // Email validation
      const emailField = form.querySelector('input[type="email"]');
      if (emailField && emailField.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value.trim())) {
          hasError = true;
          emailField.closest('.form-group-custom')?.classList.add('has-error-client');
          const errorMsg = document.createElement('span');
          errorMsg.className = 'field-error field-error-client';
          errorMsg.textContent = 'Please enter a valid email address.';
          emailField.closest('.form-group-custom')?.appendChild(errorMsg);
        }
      }

      if (hasError) {
        e.preventDefault();
        const firstError = form.querySelector('.has-error-client');
        firstError?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

  /* ── 4. Form Reset Handler ─────────────────────────────────── */
  window.resetForm = function() {
    if (!form) return;
    form.reset();
    if (avatarPreview) {
      avatarPreview.src = 'https://ui-avatars.com/api/?name=New+Student&background=1e3a5f&color=fff&size=200';
    }
    updateCardPreview();
    form.querySelectorAll('.field-error-client').forEach((el) => el.remove());
    form.querySelectorAll('.has-error-client').forEach((el) => el.classList.remove('has-error-client'));
  };

});

