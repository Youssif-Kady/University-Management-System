/* ================================================================
   UniManage – Dashboard Chart.js Visualizations
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

  Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
  Chart.defaults.color       = '#64748b';

  /* ── 1. Student Enrollment Line Chart ──────────────────────── */
  const enrollCanvas = document.getElementById('enrollmentChart');
  if (enrollCanvas) {
    const ctx = enrollCanvas.getContext('2d');

    const monthlyData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      values: [14, 22, 18, 30, 25, 34, 42, 110, 65, 24, 18, 12]
    };

    const yearlyData = {
      labels: ['2020', '2021', '2022', '2023', '2024', '2025'],
      values: [210, 290, 380, 490, 620, 710]
    };

    function createGradient(chartCtx, colorStart, colorEnd) {
      const gradient = chartCtx.createLinearGradient(0, 0, 0, 260);
      gradient.addColorStop(0, colorStart);
      gradient.addColorStop(1, colorEnd);
      return gradient;
    }

    const enrollChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: monthlyData.labels,
        datasets: [{
          label: 'Enrollments',
          data: monthlyData.values,
          fill: true,
          backgroundColor: createGradient(ctx, 'rgba(37,99,235,0.22)', 'rgba(37,99,235,0.0)'),
          borderColor: '#2563eb',
          borderWidth: 2.5,
          tension: 0.38,
          pointBackgroundColor: '#2563eb',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f172a',
            titleFont: { size: 12, weight: '600' },
            bodyFont: { size: 13 },
            padding: 10,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              label: (ctx) => `  ${ctx.parsed.y} students enrolled`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { font: { size: 11, weight: '500' } }
          },
          y: {
            grid: { color: '#f1f5f9' },
            border: { dash: [4, 4] },
            ticks: { font: { size: 11 } },
            beginAtZero: true
          }
        }
      }
    });

    // Toggle Monthly / Yearly
    const btnMonthly = document.getElementById('btnMonthly');
    const btnYearly  = document.getElementById('btnYearly');

    btnMonthly?.addEventListener('click', () => {
      btnMonthly.classList.add('active');
      btnYearly.classList.remove('active');
      enrollChart.data.labels = monthlyData.labels;
      enrollChart.data.datasets[0].data = monthlyData.values;
      enrollChart.data.datasets[0].borderColor = '#2563eb';
      enrollChart.data.datasets[0].backgroundColor = createGradient(ctx, 'rgba(37,99,235,0.22)', 'rgba(37,99,235,0.0)');
      enrollChart.update();
    });

    btnYearly?.addEventListener('click', () => {
      btnYearly.classList.add('active');
      btnMonthly.classList.remove('active');
      enrollChart.data.labels = yearlyData.labels;
      enrollChart.data.datasets[0].data = yearlyData.values;
      enrollChart.data.datasets[0].borderColor = '#8b5cf6';
      enrollChart.data.datasets[0].backgroundColor = createGradient(ctx, 'rgba(139,92,246,0.22)', 'rgba(139,92,246,0.0)');
      enrollChart.update();
    });
  }

  /* ── 2. Department Doughnut Chart ──────────────────────────── */
  const deptCanvas = document.getElementById('deptChart');
  if (deptCanvas && typeof deptData !== 'undefined') {
    const labels = Object.keys(deptData);
    const values = Object.values(deptData);
    const palette = [
      '#2563eb', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444',
      '#06b6d4', '#ec4899', '#6366f1', '#14b8a6', '#f97316',
      '#3b82f6', '#a855f7', '#84cc16', '#eab308', '#64748b'
    ];

    new Chart(deptCanvas.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: palette.slice(0, labels.length),
          borderWidth: 2,
          borderColor: '#ffffff',
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 10,
              usePointStyle: true,
              pointStyle: 'circle',
              font: { size: 11, weight: '500' },
              padding: 12
            }
          },
          tooltip: {
            backgroundColor: '#0f172a',
            titleFont: { size: 12, weight: '600' },
            bodyFont: { size: 13 },
            padding: 10,
            cornerRadius: 8
          }
        }
      }
    });
  }

  /* ── 3. Status Overview Doughnut Chart ─────────────────────── */
  const statusCanvas = document.getElementById('statusChart');
  if (statusCanvas) {
    const activeVal = typeof statActive   !== 'undefined' ? statActive   : 0;
    const inactVal  = typeof statInactive !== 'undefined' ? statInactive : 0;
    const gradVal   = typeof statGrad     !== 'undefined' ? statGrad     : 0;
    const suspVal   = typeof statSusp     !== 'undefined' ? statSusp     : 0;

    new Chart(statusCanvas.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Active', 'Inactive', 'Graduated', 'Suspended'],
        datasets: [{
          data: [activeVal, inactVal, gradVal, suspVal],
          backgroundColor: ['#10b981', '#ef4444', '#2563eb', '#f59e0b'],
          borderWidth: 2,
          borderColor: '#ffffff',
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f172a',
            titleFont: { size: 12, weight: '600' },
            bodyFont: { size: 13 },
            padding: 10,
            cornerRadius: 8
          }
        }
      }
    });
  }

});

