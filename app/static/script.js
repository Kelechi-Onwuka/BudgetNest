let incomes = [];
let expenses = [];

// Make showSection async so we can fetch updated totals for dashboard
async function showSection(sectionId) {
  // Hide all pages
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

  // If switching to dashboard, grab fresh totals from the server
  if (sectionId === 'dashboard') {
    try {
      const res = await fetch('/api/totals', { credentials: 'same-origin' });
      if (res.ok) {
        const { total_income, total_expenses, remaining } = await res.json();
        const cards = document.querySelectorAll('#dashboard .card');
        cards[0].textContent = `Income: $${total_income}`;
        cards[1].textContent = `Expenses: $${total_expenses}`;
        cards[2].textContent = `Remaining: $${remaining}`;
      } else {
        console.error('Failed to fetch totals:', res.statusText);
      }
    } catch (err) {
      console.error('Error fetching totals:', err);
    }
  }

  // Show the requested section
  const target = document.getElementById(sectionId);
  if (target) target.classList.add('active');
}

// On load, wire up forms and navigation
document.addEventListener('DOMContentLoaded', () => {
  showSection('home');

  // Display today's date in Dashboard header
  const dateEl = document.getElementById('current-date');
  if (dateEl) {
    const formatted = new Date().toLocaleDateString('en-US', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
    });
    dateEl.textContent = `📅 Today's Date: ${formatted}`;
  }

  // AJAX income form
  const incomeForm = document.querySelector('#addIncome form');
  if (incomeForm) {
    incomeForm.addEventListener('submit', async e => {
      e.preventDefault();
      const fd = new FormData(incomeForm);
      const resp = await fetch('/income', { method: 'POST', body: fd, credentials: 'same-origin' });
      if (resp.ok) {
        updateDashboardCardsLocally(fd);
        showSection('dashboard');
        alert('✅ Income saved!');
        incomeForm.reset();
      } else {
        alert('❌ There was a problem saving your income.');
      }
    });
  }

  // AJAX expense form
  const expenseForm = document.querySelector('#addExpense form');
  if (expenseForm) {
    expenseForm.addEventListener('submit', async e => {
      e.preventDefault();
      const fd = new FormData(expenseForm);
      const resp = await fetch('/expense', { method: 'POST', body: fd, credentials: 'same-origin' });
      if (resp.ok) {
        updateDashboardCardsLocally(fd);
        showSection('dashboard');
        alert('✅ Expense saved!');
        expenseForm.reset();
      } else {
        alert('❌ There was a problem saving your expense.');
      }
    });
  }
});

// If you want to optimistically update cards without refetching
function updateDashboardCardsLocally(formData) {
  const amount = parseFloat(formData.get('amount'));
  const type   = formData.get('category');
  
  // Re-fetch on next dashboard show; this is optional
}
