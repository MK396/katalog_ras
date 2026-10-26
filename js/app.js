let breeds = [];
let grid, searchInput, countEl, emptyEl, modal, modalImg, modalClose;
let lastFocusedBeforeModal = null;

async function loadBreeds() {
  try {
    const response = await fetch('data/breeds.json');
    if (!response.ok) {
      throw new Error('HTTP ' + response.status);
    }
    breeds = await response.json();
  } catch (err) {
    breeds = window.BREEDS_DATA || [];
  }
  if (!breeds.length) {
    countEl.textContent = 'Błąd ładowania danych';
    emptyEl.hidden = false;
    emptyEl.textContent =
      'Nie udało się wczytać katalogu. Uruchom lokalny serwer (np. Live Server) albo odśwież stronę.';
    return;
  }
  render();
}

function selectedValues(name) {
  return Array.from(document.querySelectorAll('input[name="' + name + '"]:checked')).map(function (el) {
    return el.value;
  });
}

function getFiltered() {
  const query = searchInput.value.trim().toLowerCase();
  const sizes = selectedValues('size');
  const activities = selectedValues('activity');

  return breeds.filter(function (b) {
    const matchesName = b.name.toLowerCase().includes(query);
    const matchesSize = sizes.length === 0 || sizes.includes(b.size);
    const matchesActivity = activities.length === 0 || activities.includes(b.activity);
    return matchesName && matchesSize && matchesActivity;
  });
}

function createCard(b) {
  const card = document.createElement('article');
  card.className = 'card';
  card.setAttribute('role', 'listitem');
  card.tabIndex = 0;
  card.setAttribute('aria-label', b.name + ', wielkość ' + b.size + ', aktywność ' + b.activity);

  const img = document.createElement('img');
  img.src = b.image;
  img.alt = b.name;
  img.loading = 'lazy';
  img.decoding = 'async';

  const body = document.createElement('div');
  body.className = 'card-body';

  const title = document.createElement('h3');
  title.textContent = b.name;

  const badgeSize = document.createElement('span');
  badgeSize.className = 'badge';
  badgeSize.textContent = b.size;

  const badgeActivity = document.createElement('span');
  badgeActivity.className = 'badge badge-activity';
  badgeActivity.textContent = b.activity;

  body.appendChild(title);
  body.appendChild(badgeSize);
  body.appendChild(badgeActivity);

  card.appendChild(img);
  card.appendChild(body);

  function activate() {
    openModal(b);
  }
  card.addEventListener('click', activate);
  card.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      activate();
    }
  });

  return card;
}

function render() {
  const list = getFiltered();
  grid.replaceChildren();

  list.forEach(function (b) {
    grid.appendChild(createCard(b));
  });

  countEl.textContent = 'Znaleziono: ' + list.length;
  emptyEl.hidden = list.length !== 0;
}

function openModal(b) {
  if (modal.hidden) {
    lastFocusedBeforeModal = document.activeElement;
  }
  modalImg.src = b.image;
  modalImg.alt = b.name;
  document.getElementById('modal-name').textContent = b.name;
  document.getElementById('modal-desc').textContent = b.description;
  document.getElementById('modal-size').textContent = b.size;
  document.getElementById('modal-activity').textContent = b.activity;
  document.getElementById('modal-origin').textContent = b.origin;
  document.getElementById('modal-weight').textContent = b.weight;
  document.getElementById('modal-lifespan').textContent = b.lifespan;
  modal.hidden = false;
  document.body.classList.add('modal-open');
  modalClose.focus();
}

function closeModal() {
  if (modal.hidden) {
    return;
  }
  modal.hidden = true;
  document.body.classList.remove('modal-open');
  modalImg.removeAttribute('src');
  modalImg.alt = '';
  if (lastFocusedBeforeModal && typeof lastFocusedBeforeModal.focus === 'function') {
    lastFocusedBeforeModal.focus();
  }
  lastFocusedBeforeModal = null;
}

function init() {
  grid = document.getElementById('grid');
  searchInput = document.getElementById('search');
  countEl = document.getElementById('count');
  emptyEl = document.getElementById('empty');
  modal = document.getElementById('modal');
  modalImg = document.getElementById('modal-img');
  modalClose = document.getElementById('modal-close');

  searchInput.addEventListener('input', render);
  document.querySelectorAll('input[name="size"], input[name="activity"]').forEach(function (el) {
    el.addEventListener('change', render);
  });
  modalClose.addEventListener('click', closeModal);
  modal.addEventListener('click', function (e) {
    if (e.target === modal) {
      closeModal();
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) {
      closeModal();
    }
  });

  loadBreeds();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
