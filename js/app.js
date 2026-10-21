let breeds = [];

const grid = document.getElementById('grid');
const searchInput = document.getElementById('search');
const countEl = document.getElementById('count');
const emptyEl = document.getElementById('empty');

const modal = document.getElementById('modal');
const modalImg = document.getElementById('modal-img');

async function loadBreeds() {
  try {
    const response = await fetch('data/breeds.json');
    if (!response.ok) {
      throw new Error('HTTP ' + response.status);
    }
    breeds = await response.json();
  } catch (err) {
    // Fallback gdy strona jest otwarta jako plik (file://) bez lokalnego serwera
    breeds = window.BREEDS_DATA || [];
  }
  if (!breeds.length) {
    countEl.textContent = 'Błąd ładowania danych';
    emptyEl.hidden = false;
    emptyEl.textContent = 'Nie udało się wczytać katalogu. Uruchom lokalny serwer (np. Live Server) albo odśwież stronę.';
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
    const matchesSize = sizes.length === 0 || sizes.indexOf(b.size) !== -1;
    const matchesActivity = activities.length === 0 || activities.indexOf(b.activity) !== -1;
    return matchesName && matchesSize && matchesActivity;
  });
}

function render() {
  const list = getFiltered();
  grid.innerHTML = '';

  list.forEach(function (b) {
    const card = document.createElement('article');
    card.className = 'card';
    card.innerHTML =
      '<img src="' + b.image + '" alt="' + b.name + '">' +
      '<div class="card-body">' +
        '<h3>' + b.name + '</h3>' +
        '<span class="badge">' + b.size + '</span> ' +
        '<span class="badge badge-activity">' + b.activity + '</span>' +
      '</div>';
    card.addEventListener('click', function () { openModal(b); });
    grid.appendChild(card);
  });

  countEl.textContent = 'Znaleziono: ' + list.length;
  emptyEl.hidden = list.length !== 0;
}

function openModal(b) {
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
}

function closeModal() {
  modal.hidden = true;
}

searchInput.addEventListener('input', render);
document.querySelectorAll('input[name="size"], input[name="activity"]').forEach(function (el) {
  el.addEventListener('change', render);
});
document.getElementById('modal-close').addEventListener('click', closeModal);
modal.addEventListener('click', function (e) {
  if (e.target === modal) closeModal();
});
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closeModal();
});

loadBreeds();
