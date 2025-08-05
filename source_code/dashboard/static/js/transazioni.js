
const API_URL = '/api/transactions/';
const PAGE_SIZE = 10;
let allTransazioni = [];
let allCategoriesList = [];
let currentPage = 1;
let currentSearch = '';
let currentCategory = '';
let selectedCategories = [];

window.updateFilterBtn = function() {
  const filterBtn = document.getElementById('transazioni-filter-btn');
  const n = selectedCategories.length;
  filterBtn.innerHTML = n > 0 ? `Filtra categorie <span style='background:var(--blue-500);color:#fff;border-radius:8px;padding:0 7px;margin-left:7px;font-size:0.98em;'>${n}</span> ▼` : 'Filtra categorie ▼';
};

document.addEventListener('DOMContentLoaded', () => {
  if (!window.authUtils.requireAuth()) {
    return; // User will be redirected to login
  }

  fetchTransazioni();
  document.getElementById('transazioni-search').addEventListener('input', function(e) {
    filterAndRender();
  });
  const filterBtn = document.getElementById('transazioni-filter-btn');
  const filterMenu = document.getElementById('transazioni-filter-menu');
  filterBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    if (filterMenu.innerHTML.trim() === '') return;
    filterMenu.classList.toggle('show');
  });
  document.addEventListener('click', function(e) {
    if (!filterMenu.contains(e.target) && e.target !== filterBtn) {
      filterMenu.classList.remove('show');
    }
  });

  const profileToggle = document.getElementById('profileToggle');
  const profileMenu = document.getElementById('profileMenu');
  if (profileToggle && profileMenu) {
    profileToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      const isOpen = !profileMenu.classList.contains('hidden');
      profileMenu.classList.toggle('hidden', isOpen);
      profileToggle.setAttribute('aria-expanded', String(!isOpen));
    });
    document.addEventListener('click', function() {
      if (!profileMenu.classList.contains('hidden')) {
        profileMenu.classList.add('hidden');
        profileToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
});

async function fetchTransazioni(page = 1, search = '', categories = []) {
  let url = `${API_URL}?page=${page}`;
  if (search) url += `&search=${encodeURIComponent(search)}`;
  if (categories && categories.length > 0) {
    url += `&category=${categories.map(encodeURIComponent).join(',')}`;
  }

  const { response, data } = await window.authUtils.authFetch(url);
  if (response.ok && data) {
    allTransazioni = data.results || [];
    renderTransazioniTable(allTransazioni, data.count || 0, page);
    renderPagination(data.count || 0, page);
    if (data.results) extractCategories(data.results);
  }
}

function renderTransazioniTable(transazioni, totalCount, page) {
  const tbody = document.getElementById('transazioni-tbody');
  tbody.innerHTML = '';
  let startNum = totalCount - (page - 1) * PAGE_SIZE;
  transazioni.forEach((tx, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td title="${tx.id}">${startNum - idx}</td>
      <td>${tx.transaction_name}</td>
      <td>${tx.date || '-'}</td>
      <td>${tx.amount} ${tx.currency || ''}</td>
      <td>${tx.destinatario_nome || ''}</td>
      <td>${tx.category_name || '-'}</td>
      <td><button class="scarica-btn" data-id="${tx.id}">Scarica</button></td>
    `;
    tbody.appendChild(tr);
  });

  document.querySelectorAll('.scarica-btn').forEach((btn) => {
    btn.addEventListener('click', async function() {
      const id = btn.getAttribute('data-id');
      const { response, data } = await window.authUtils.authFetch(`/api/transactions/${id}/`);
      if (response.ok && data) {
        generateAndPreviewPDF(data);
      }
    });
  });
}

function renderPagination(total, page) {
  const pagDiv = document.getElementById('transazioni-pagination');
  pagDiv.innerHTML = '';
  const totalPages = Math.ceil(total / PAGE_SIZE);
  if (totalPages <= 1) return;

  const prevBtn = document.createElement('button');
  prevBtn.textContent = '<';
  prevBtn.disabled = page === 1;
  prevBtn.addEventListener('click', () => {
    if (page > 1) {
      currentPage = page - 1;
      fetchTransazioni(currentPage, currentSearch, currentCategory);
    }
  });
  pagDiv.appendChild(prevBtn);


  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement('button');
    btn.textContent = i;
    if (i === page) btn.classList.add('active');
    btn.addEventListener('click', () => {
      currentPage = i;
      fetchTransazioni(currentPage, currentSearch, currentCategory);
    });
    pagDiv.appendChild(btn);
  }


  const nextBtn = document.createElement('button');
  nextBtn.textContent = '>';
  nextBtn.disabled = page === totalPages;
  nextBtn.addEventListener('click', () => {
    if (page < totalPages) {
      currentPage = page + 1;
      fetchTransazioni(currentPage, currentSearch, currentCategory);
    }
  });
  pagDiv.appendChild(nextBtn);
}

function extractCategories(transazioni) {
  const menu = document.getElementById('transazioni-filter-menu');
  const cats = Array.from(new Set(transazioni.map(tx => tx.category_name).filter(Boolean)));
  menu.innerHTML = cats.map(c => `
    <label style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;cursor:pointer;">
      <input type="checkbox" class="transazioni-filter-checkbox" value="${c}">
      <span>${c}</span>
    </label>
  `).join('');

  menu.querySelectorAll('.transazioni-filter-checkbox').forEach(cb => {
    cb.addEventListener('change', function() {
      selectedCategories = Array.from(menu.querySelectorAll('.transazioni-filter-checkbox:checked')).map(cb => cb.value);
      filterAndRender();
      window.updateFilterBtn();
    });
  });

  window.updateFilterBtn();
}

function filterAndRender() {
  let filtered = allTransazioni;
  if (selectedCategories.length > 0) {
    filtered = filtered.filter(tx => selectedCategories.includes(tx.category_name));
  }
  const searchVal = document.getElementById('transazioni-search').value.toLowerCase();
  if (searchVal) {
    filtered = filtered.filter(tx =>
      (tx.transaction_name && tx.transaction_name.toLowerCase().includes(searchVal)) ||
      (tx.destinatario_nome && tx.destinatario_nome.toLowerCase().includes(searchVal)) ||
      (tx.category_name && tx.category_name.toLowerCase().includes(searchVal)) ||
      (tx.amount && String(tx.amount).toLowerCase().includes(searchVal)) ||
      (tx.date && tx.date.toLowerCase().includes(searchVal))
    );
  }
  renderTransazioniTable(filtered, filtered.length, 1);
}

document.addEventListener('DOMContentLoaded', function() {
  fetchTransazioni();
  document.getElementById('transazioni-search').addEventListener('input', function(e) {
    filterAndRender();
  });
  const filterBtn = document.getElementById('transazioni-filter-btn');
  const filterMenu = document.getElementById('transazioni-filter-menu');
  filterBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    if (filterMenu.innerHTML.trim() === '') return;
    filterMenu.classList.toggle('show');
  });
  document.addEventListener('click', function(e) {
    if (!filterMenu.contains(e.target) && e.target !== filterBtn) {
      filterMenu.classList.remove('show');
    }
  });

  const profileToggle = document.getElementById('profileToggle');
  const profileMenu = document.getElementById('profileMenu');
  if (profileToggle && profileMenu) {
    profileToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      const isOpen = !profileMenu.classList.contains('hidden');
      profileMenu.classList.toggle('hidden', isOpen);
      profileToggle.setAttribute('aria-expanded', String(!isOpen));
    });
    document.addEventListener('click', function() {
      if (!profileMenu.classList.contains('hidden')) {
        profileMenu.classList.add('hidden');
        profileToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
});

function getBase64FromImageUrl(url, callback) {
  var img = new window.Image();
  img.crossOrigin = 'Anonymous';
  img.onload = function() {
    var canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    var dataURL = canvas.toDataURL('image/png');
    callback(dataURL);
  };
  img.src = url;
}

function generateAndPreviewPDF(data) {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  getBase64FromImageUrl('/static/image/logo.png', function(logoBase64) {
    const pageWidth = doc.internal.pageSize.getWidth();
    doc.addImage(logoBase64, 'PNG', pageWidth/2-20, 10, 40, 20);
    let y = 35;
    doc.setFontSize(18);
    doc.text('Ricevuta Transazione', pageWidth/2, y, {align: 'center'});
    y += 10;
    doc.setFontSize(12);
    doc.text(`Data: ${data.date || ''}`, 20, y+=10);
    doc.text(`Stato: ${data.stato || ''}`, 20, y+=10);
    y += 5;
    doc.setFontSize(14);
    doc.text('Dati Mittente', 20, y+=10);
    doc.setFontSize(12);
    doc.text(`Nome: ${data.mittente_nome || '-'}`, 20, y+=8);
    doc.text(`Email: ${data.mittente_email || '-'}`, 20, y+=8);
    doc.text(`IBAN: ${data.mittente_iban || '-'}`, 20, y+=8);
    doc.text(`Città: ${data.mittente_citta || '-'}`, 20, y+=8);
    y += 5;
    doc.setFontSize(14);
    doc.text('Dati Destinatario', 20, y+=10);
    doc.setFontSize(12);
    doc.text(`Nome: ${data.destinatario_nome || '-'}`, 20, y+=8);
    doc.text(`Email: ${data.destinatario_email || '-'}`, 20, y+=8);
    doc.text(`IBAN: ${data.destinatario_iban || '-'}`, 20, y+=8);
    doc.text(`Città: ${data.destinatario_citta || '-'}`, 20, y+=8);
    y += 5;
    doc.setFontSize(14);
    doc.text('Dettagli Transazione', 20, y+=10);
    doc.setFontSize(12);
    doc.text(`Clausola/Motivazione: ${data.clausola || '-'}`, 20, y+=8);
    doc.text(`Nota: ${data.notes || '-'}`, 20, y+=8);
    doc.text(`Importo: ${data.amount || ''} ${data.currency || ''}`, 20, y+=8);
    doc.text(`Categoria: ${data.category_name || '-'}`, 20, y+=8);
    y += 5;
    doc.text(`ID Transazione: ${data.id || ''}`, 20, y+=10);
    doc.setFontSize(10);
    doc.text('Questa ricevuta è stata generata automaticamente dal sistema FinHub.', 20, y+=10);
    window.open(doc.output('bloburl'), '_blank');
  });
} 