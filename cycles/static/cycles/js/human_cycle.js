document.addEventListener('DOMContentLoaded', function() {
  const canvas = document.getElementById('humanCycleChart');
  const ringContainer = document.getElementById('cycleRing');
  // require at least one of the display containers
  if (!canvas && !ringContainer) return;

  const cycleButtons = document.querySelectorAll('[data-cycle]');
  const modal = document.getElementById('fullTemplateModal');
  const modalBody = document.getElementById('modalBody');
  const closeModalBtn = document.getElementById('closeModal');
  const healthPeriodsContainer = document.getElementById('healthPeriods');
  const reincarnationPeriodsContainer = document.getElementById('reincarnationPeriods');

  let activeChart = null;

  // track the last selected cycle so we can robustly know which tab is active
  let lastSelectedCycle = 'human';

  function setLastSelected(cycleType) {
    lastSelectedCycle = cycleType;
    // update button active styles for compatibility with server-side rendering
    cycleButtons.forEach(b => {
      if (b.getAttribute('data-cycle') === cycleType) {
        b.classList.add('active');
        // sync visual classes (purple bg + white text)
        b.classList.remove('bg-gray-800','text-purple-300');
        b.classList.add('bg-indigo-600','text-white');
      } else {
        b.classList.remove('active');
        b.classList.remove('bg-indigo-600','text-white');
        b.classList.add('bg-gray-800','text-purple-300');
      }
    });
  }

  // Show only the selected cycle's detailed content area and hide others.
  function showCycleContent(cycleType) {
    // hide all cycle-content blocks
    document.querySelectorAll('.cycle-content').forEach(el => el.classList.add('hidden'));
    // show the selected content block if present
    const block = document.getElementById(`${cycleType}Content`);
    if (block) block.classList.remove('hidden');

    // For the human cycle we display the compact SVG ring and the template panel.
    const ring = document.getElementById('cycleRing');
    if (cycleType === 'human') {
      if (ring) ring.classList.remove('hidden');
    } else {
      if (ring) ring.classList.add('hidden');
    }
  }

  function fetchAndRender(cycleType) {
    // show loading state
    const currentDateTimeEl = document.getElementById('currentDateTime');
    const currentCycleInfoEl = document.getElementById('currentCycleInfo');
    if (currentDateTimeEl) currentDateTimeEl.textContent = 'Loading...';
    if (currentCycleInfoEl) currentCycleInfoEl.innerHTML = '';

  // if cycleType is business and a select exists, include the selected business_id
  let url = `/api/user_cycle/${cycleType}/`;
  try {
    const sel = document.getElementById('businessSelect');
    if (cycleType === 'business' && sel && sel.value) {
      url += `?business_id=${encodeURIComponent(sel.value)}`;
    }
  } catch (e) { console.warn('business select check failed', e); }

  fetch(url)
    .then(res => {
      if (!res.ok) {
        console.warn('API returned non-OK', res.status);
        return res.json().then(j => { throw j; });
      }
      return res.json();
    })
    .then(data => {
      // normalize for business responses which return { business_cycles: [...] }
      let progress = Math.round((data.progress || 0) * 10) / 10;
      let periodName = '';
      let templateData = data.template || null;

      if (data.business_cycles && Array.isArray(data.business_cycles)) {
        // prefer the first business for the dashboard notice
        const first = data.business_cycles[0];
        if (first) {
          progress = Math.round((first.progress || 0) * 10) / 10;
          periodName = (first.current_period && first.current_period.name) ? first.current_period.name : '';
          // template might already be an effects object from the API
          templateData = first.template || null;
          // map current_period fields into a small object for modal fallback
          data.periods = first.periods || [];
          data.current_period_number = (first.periods && first.periods.indexOf(first.current_period) >= 0) ? (first.periods.indexOf(first.current_period) + 1) : 1;
          data.current_period = first.current_period || {};
        }
      } else {
        // not business: keep existing behavior
        periodName = (data.periods && data.current_period_number && data.periods[data.current_period_number - 1]) ? data.periods[data.current_period_number - 1].name : '';
      }

      // ensure templateData is available in a common place
      data._template_for_ui = templateData;

      // Helper to render a business's periods into the businessPeriods container
      // Render each business period as its own period card (matches other cycles)
      function renderBusinessCard(container, item) {
        try {
          const bizName = (item.business && item.business.name) ? item.business.name : (item.business || 'Business');
          const periods = item.periods || [];
          const current = item.current_period || {};
          const currentName = (current && current.name) ? current.name : null;

          periods.forEach((period) => {
            const active = (period.name && currentName && period.name === currentName) || (item.current_period && item.current_period.name && item.current_period.name === period.name);
            const card = document.createElement('div');
            // use the same card classes as daily/yearly for visual parity
            card.className = 'cycle-card bg-white rounded-xl shadow-md overflow-hidden fade-in';
            if (active) card.classList.add('period-active');
            // accessibility: make each card focusable and role=article
            card.setAttribute('role', 'article');
            card.setAttribute('tabindex', '0');
            card.setAttribute('aria-label', `${period.name} - ${bizName}`);
            card.setAttribute('data-period-details', JSON.stringify(period));
            const inner = document.createElement('div');
            inner.className = 'p-6';
            inner.innerHTML = `
              <h3 class="text-xl font-semibold text-gray-800">${period.name}</h3>
              <p class="text-gray-600">${period.start || ''}${period.start && period.end ? ' - ' : ''}${period.end || ''}</p>
              <p class="text-gray-600 mt-2">${period.principle || ''}</p>
              <p class="text-gray-500 mt-2"><em>Suggestion: ${period.suggestion || ''}</em></p>
              <p class="text-sm text-indigo-700 mt-3 font-medium">${bizName}</p>
            `;
            card.appendChild(inner);
            container.appendChild(card);
          });
        } catch (e) { console.warn('renderBusinessCard failed', e); }
      }

      // compute progress text-friendly
      progress = Math.round((progress || 0) * 10) / 10;
      // Render SVG progress ring if container exists
      if (ringContainer) {
        const size = 144; // px
        const stroke = 10;
        const radius = (size - stroke) / 2;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference * (1 - Math.min(Math.max(progress / 100, 0), 1));
  // prefer periodName resolved above for business; otherwise compute from periods
  if (!periodName) periodName = (data.periods && data.current_period_number && data.periods[data.current_period_number - 1]) ? data.periods[data.current_period_number - 1].name : '';
        ringContainer.innerHTML = `
          <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(${size/2}, ${size/2})">
              <circle r="${radius}" fill="transparent" stroke="#e5e7eb" stroke-width="${stroke}" />
              <circle r="${radius}" fill="transparent" stroke="#7c3aed" stroke-width="${stroke}" stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" stroke-linecap="round" transform="rotate(-90)" />
              <text x="0" y="0" text-anchor="middle" dy="0.35em" font-size="18" fill="#7c3aed">${progress}%</text>
            </g>
          </svg>
        `;
        // small label below
        const label = document.createElement('div');
  // increase contrast and size for better visibility
  label.className = 'text-center text-base text-purple-700 mt-2 font-medium';
        label.textContent = periodName;
        // replace existing label if present
        const existingLabel = ringContainer.querySelector('.cycle-label');
        if (existingLabel) existingLabel.remove();
        label.classList.add('cycle-label');
        ringContainer.appendChild(label);
      }
      // Render business periods when business cycle is active
      if (cycleType === 'business') {
        const bp = document.getElementById('businessPeriods');
        if (bp) {
          bp.innerHTML = '';
          // API may return { business_cycles: [...] } or { business: { ... } }
          if (data.business_cycles && Array.isArray(data.business_cycles) && data.business_cycles.length > 0) {
            data.business_cycles.forEach(item => renderBusinessCard(bp, item));
          } else if (data.business) {
            // single-business preview
            renderBusinessCard(bp, data.business);
          } else if (data.periods) {
            // fallback: use generic periods list
            renderBusinessCard(bp, { business: 'Preview', periods: data.periods, current_period: data.current_period || {} });
          } else {
            bp.innerHTML = '<p class="text-gray-500">No business data available.</p>';
          }
        }
      }
      // Render soul periods when soul cycle is active so they display like other cycles
      if (cycleType === 'soul') {
        const sp = document.getElementById('soulPeriods');
        if (sp) {
          sp.innerHTML = '';
          const periods = data.periods || [];
          const current = data.current_period || {};
          const currentName = (current && current.name) ? current.name : null;
          periods.forEach(period => {
            try {
              const active = (period.name && currentName && period.name === currentName);
              const card = document.createElement('div');
              card.className = 'p-4 rounded-lg';
              if (active) card.classList.add('period-active'); else card.classList.add('bg-gray-50');
              // accessibility
              card.setAttribute('role', 'article');
              card.setAttribute('tabindex', '0');
              card.setAttribute('aria-label', `${period.name} - Soul period`);
              card.setAttribute('data-period-details', JSON.stringify(period));
              const inner = document.createElement('div');
              inner.innerHTML = `
                <h4 class="font-semibold text-lg text-indigo-800">${period.name}</h4>
                <p>${period.principle || ''}</p>
                <p class="text-gray-500 mt-1"><em>Suggestion: ${period.suggestion || ''}</em></p>
              `;
              card.appendChild(inner);
              sp.appendChild(card);
            } catch (e) { console.warn('render soul period failed', e); }
          });
        }
      }

      // Render health periods when health cycle is active
      if (cycleType === 'health') {
        const hp = document.getElementById('healthPeriods');
        if (hp) {
          hp.innerHTML = '';
          const periods = data.periods || [];
          const current = data.current_period || {};
          const currentName = (current && current.name) ? current.name : null;
          periods.forEach(period => {
            try {
              const active = (period.name && currentName && period.name === currentName);
              const card = document.createElement('div');
              card.className = 'p-4 rounded-lg';
              if (active) card.classList.add('period-active'); else card.classList.add('bg-gray-50');
              // accessibility
              card.setAttribute('role', 'article');
              card.setAttribute('tabindex', '0');
              card.setAttribute('aria-label', `${period.name} - Health period`);
              card.setAttribute('data-period-details', JSON.stringify(period));
              const inner = document.createElement('div');
              inner.innerHTML = `
                <h4 class="font-semibold text-lg text-indigo-800">${period.name}</h4>
                <p>${period.principle || ''}</p>
              `;
              card.appendChild(inner);
              hp.appendChild(card);
            } catch (e) { console.warn('render health period failed', e); }
          });
        }
      }

      // Render reincarnation periods when reincarnation cycle is active
      if (cycleType === 'reincarnation') {
        const rp = document.getElementById('reincarnationPeriods');
        if (rp) {
          rp.innerHTML = '';
          const periods = data.periods || [];
          const current = data.current_period || {};
          const currentName = (current && current.name) ? current.name : null;
          periods.forEach(period => {
            try {
              const active = (period.name && currentName && period.name === currentName);
              const card = document.createElement('div');
              card.className = 'p-4 rounded-lg';
              if (active) card.classList.add('period-active'); else card.classList.add('bg-gray-50');
              // accessibility
              card.setAttribute('role', 'article');
              card.setAttribute('tabindex', '0');
              card.setAttribute('aria-label', `${period.name} - Reincarnation period`);
              card.setAttribute('data-period-details', JSON.stringify(period));
              const inner = document.createElement('div');
              inner.innerHTML = `
                <h4 class="font-semibold text-lg text-indigo-800">${period.name}</h4>
                <p>${period.principle || ''}</p>
                <p class="text-gray-500 mt-1"><em>Suggestion: ${period.suggestion || ''}</em></p>
              `;
              card.appendChild(inner);
              rp.appendChild(card);
            } catch (e) { console.warn('render reincarnation period failed', e); }
          });
        }
      }

      if (closeModalBtn && modal) {
        closeModalBtn.onclick = function() { modal.classList.add('hidden'); modal.classList.remove('flex'); }
      }
      // Escape key to close
      document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) { modal.classList.add('hidden'); modal.classList.remove('flex'); } });

  if (closeModalBtn && modal) {
    closeModalBtn.onclick = function() { modal.classList.add('hidden'); modal.classList.remove('flex'); }
  }
  // overlay click to close
  if (modal) {
    modal.onclick = function(e) { if (e.target === modal) { modal.classList.add('hidden'); modal.classList.remove('flex'); } }
  }
  // populate top summary/currentCycleInfo with friendly info
      if (currentDateTimeEl) {
        // show a simple timestamp and summary
        const now = new Date();
        currentDateTimeEl.textContent = now.toLocaleString();
      }
      if (currentCycleInfoEl) {
        // Prefer the pre-computed periodName (set earlier for business and other cycle types)
        const periodLabel = periodName || (data.current_period && data.current_period.name) || ((data.periods && data.current_period_number && data.periods[data.current_period_number - 1]) ? data.periods[data.current_period_number - 1].name : '');
        // Try to find an age range from template or period
        const ageRange = (data.template && (data.template.start_age || data.template.end_age)) ? ((data.template.start_age || '?') + ' - ' + (data.template.end_age || '?')) : (data.periods && data.current_period_number && (data.periods[data.current_period_number - 1] && (data.periods[data.current_period_number - 1].start_age || data.periods[data.current_period_number - 1].end_age)) ? ((data.periods[data.current_period_number - 1].start_age || '?') + ' - ' + (data.periods[data.current_period_number - 1].end_age || '?')) : '');
        // If a business name is available (single preview or normalized shape), include it as a small subtitle
        let businessLabel = '';
        try {
          if (data.business_cycles && Array.isArray(data.business_cycles) && data.business_cycles.length > 0) {
            const firstBiz = data.business_cycles[0];
            businessLabel = (firstBiz && firstBiz.business && firstBiz.business.name) ? firstBiz.business.name : '';
          } else if (data.business && data.business.name) {
            businessLabel = data.business.name;
          }
        } catch (e) { businessLabel = ''; }

        let html = '';
        if (periodLabel) html += `<div class="text-lg font-semibold text-purple-200">${periodLabel}</div>`;
        if (businessLabel) html += `<div class="text-sm text-purple-300">${businessLabel}</div>`;
        if (ageRange) html += `<div class="text-sm text-gray-300">Age range: ${ageRange}</div>`;
        // include a short principle/suggestion if available
        const currentPeriod = (data.periods && data.current_period_number) ? (data.periods[data.current_period_number - 1] || {}) : (data.current_period || {});
        if (currentPeriod.start_date && currentPeriod.end_date) {
            html += `<div class="text-sm text-gray-300">From: ${currentPeriod.start_date} To: ${currentPeriod.end_date}</div>`;
        }
        if (currentPeriod.principle) html += `<div class="mt-2 text-gray-300">${currentPeriod.principle}</div>`;
        if (currentPeriod.suggestion) html += `<div class="mt-1 text-sm text-gray-400"><em>Suggestion: ${currentPeriod.suggestion}</em></div>`;
        currentCycleInfoEl.innerHTML = html;
      }
      // if we fetched 'soul' but the API didn't return expected fields, ensure local UI isn't left showing loading
      if (cycleType === 'soul') {
        const soulText = document.getElementById('soulProgressText');
        if (soulText && soulText.textContent.trim() === 'Loading...') {
          soulText.textContent = (progress || 0) + '%';
        }
      }

      // Add click event listeners to period cards
      document.querySelectorAll('.cycle-card, [data-period-details]').forEach(card => {
        card.addEventListener('click', () => {
          const periodDetails = JSON.parse(card.getAttribute('data-period-details'));
          openPeriodModal(periodDetails);
        });
      });
    })
  .catch(err => { console.error('Failed to load cycle', err); });
  }

  // wire cycle switch buttons
  cycleButtons.forEach(b => {
    b.addEventListener('click', (e) => {
      const ct = b.getAttribute('data-cycle');
      // fetch and render selected cycle
  setLastSelected(ct);
  // update visible content areas immediately
  showCycleContent(ct);
  fetchAndRender(ct);
    });
  });

  // when business select changes, re-fetch if business cycle is active
  const businessSelect = document.getElementById('businessSelect');
  if (businessSelect) {
    businessSelect.addEventListener('change', function() {
      // if the business tab is active (tracked), trigger a refresh
      if (lastSelectedCycle === 'business') fetchAndRender('business');
    });
  }

  // Apply data-progress attributes to any server-rendered bars on initial load
  document.querySelectorAll('[data-progress]').forEach(el => {
    const val = parseFloat(el.getAttribute('data-progress')) || 0;
    el.style.width = (Math.min(Math.max(val, 0), 100)) + '%';
  });

  if (closeModalBtn && modal) {
    closeModalBtn.onclick = function() { modal.classList.add('hidden'); modal.classList.remove('flex'); }
  }
  // overlay click to close
  if (modal) {
    modal.onclick = function(e) { if (e.target === modal) { modal.classList.add('hidden'); modal.classList.remove('flex'); } }
  }
  // Escape key to close
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) { modal.classList.add('hidden'); modal.classList.remove('flex'); } });

  // Ensure soul UI isn't left with 'Loading...' — initialize friendly values if empty
  // initialize soul progress from data-progress on the circle/text
  const soulText = document.getElementById('soulProgressText');
  const soulCircle = document.getElementById('soulProgressCircle');
  try {
    const textVal = soulText && soulText.getAttribute('data-progress') ? parseFloat(soulText.getAttribute('data-progress')) : null;
    const circleVal = soulCircle && soulCircle.getAttribute('data-progress') ? parseFloat(soulCircle.getAttribute('data-progress')) : null;
    const useVal = (textVal !== null) ? textVal : ((circleVal !== null) ? circleVal : 0);
    if (soulText) soulText.textContent = `${Math.round(useVal)}%`;
    if (soulCircle) {
      const circumference = 2 * Math.PI * 45;
      const offset = circumference - (Math.min(Math.max(useVal, 0), 100) / 100 * circumference);
      soulCircle.style.strokeDashoffset = offset;
    }
  } catch (e) {
    console.warn('Failed to init soul progress from data-progress', e);
  }

  // Function to open the modal with period details
  function openPeriodModal(details) {
    const modal = document.getElementById('fullTemplateModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');

    if (modal && modalTitle && modalBody) {
      modalTitle.textContent = details.name;
      let html = '';
      if (details.full_description) {
        html += `<p class="mb-2">${details.full_description}</p>`;
      } else {
        if (details.start_date && details.end_date) {
          html += `<p class="mb-2"><strong>From:</strong> ${details.start_date} <strong>To:</strong> ${details.end_date}</p>`;
        } else if (details.start && details.end) {
          html += `<p class="mb-2"><strong>Time:</strong> ${details.start} - ${details.end}</p>`;
        }
        html += `<p class="mb-2"><strong>Principle:</strong> ${details.principle}</p>`;
        html += `<p class="mb-2"><strong>Suggestion:</strong> ${details.suggestion}</p>`;
      }
      modalBody.innerHTML = html;
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }
  }

  // Add click event listeners to period cards
      document.querySelectorAll('.cycle-card, [data-period-details]').forEach(card => {
        card.addEventListener('click', () => {
          const periodDetails = JSON.parse(card.getAttribute('data-period-details'));
          openPeriodModal(periodDetails);
        });
      });

  // initial render
  setLastSelected('human');
  showCycleContent('human');
  fetchAndRender('human');

  // profile modal open/close and AJAX submit
  const profileModal = document.getElementById('profileModal');
  const closeProfileModal = document.getElementById('closeProfileModal');
  const profileForm = document.getElementById('profileModalForm');
  if (profileModal) {
    // open the modal when 'Edit profile' link is clicked
    const editLinks = document.querySelectorAll('a[href$="profile/edit/"]');
    editLinks.forEach(a => a.addEventListener('click', function(e) {
      e.preventDefault();
      profileModal.classList.remove('hidden');
      profileModal.classList.add('flex');
    }));
  }
  if (closeProfileModal) {
    closeProfileModal.addEventListener('click', function() { profileModal.classList.add('hidden'); profileModal.classList.remove('flex'); });
  }
  if (profileForm) {
    profileForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(profileForm);
      const url = profileForm.getAttribute('data-url');
      fetch(url, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData
      }).then(r => r.json()).then(j => {
        if (j.success) {
          // simple feedback and reload part of the page
          profileModal.classList.add('hidden'); profileModal.classList.remove('flex');
          // reload the page to refresh dashboard-derived values
          location.reload();
        } else {
          alert('Failed to update profile.');
        }
      }).catch(err => { console.error(err); alert('Failed to update profile.'); });
    });
  }

  // CSRF helper for AJAX requests
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // AJAX delete for businesses
  const deleteButtons = document.querySelectorAll('.js-delete-business');
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      if (!confirm('Delete this business?')) return;
      const url = btn.getAttribute('data-delete-url');
      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken')
        }
      }).then(r => r.json()).then(j => {
        if (j.success) {
          // fade out the card then remove
          const card = btn.closest('.business-card');
          if (card) {
            card.style.transition = 'opacity 300ms ease, transform 300ms ease';
            card.style.opacity = '0';
            card.style.transform = 'translateY(-8px)';
            setTimeout(() => card.remove(), 320);
          }
          showToast('Business deleted', 'success');
        } else {
          showToast('Failed to delete business', 'error');
        }
      }).catch(err => { console.error(err); alert('Failed to delete business'); });
    });
  });

  // small toast helper
  function showToast(message, level) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'px-4 py-2 rounded shadow ' + (level === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white');
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 200ms ease, transform 200ms ease';
    toast.textContent = message;
    container.appendChild(toast);
    // animate in
    requestAnimationFrame(() => { toast.style.opacity = '1'; toast.style.transform = 'translateY(0)'; });
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-8px)';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Initialize flatpickr on any date inputs present (in dynamic pages)
  if (window.flatpickr) {
    document.querySelectorAll('input[type="date"]').forEach(function(el) {
      try { flatpickr(el, {dateFormat: 'Y-m-d'}); } catch (e) { console.warn('flatpickr init failed', e); }
    });
  }

  // Basic client-side validation for date inputs before profile submit
  const profileModalFormEl = document.getElementById('profileModalForm');
  if (profileModalFormEl) {
    profileModalFormEl.addEventListener('submit', function(e) {
      // simple validations: date_of_birth not in future
      const dob = profileModalFormEl.querySelector('input[name="date_of_birth"]');
      if (dob && dob.value) {
        const dt = new Date(dob.value);
        const now = new Date();
        if (dt > now) {
          e.preventDefault();
          showToast('Date of birth cannot be in the future', 'error');
          return false;
        }
      }
      return true;
    });
  }
});
