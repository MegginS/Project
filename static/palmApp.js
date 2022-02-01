


// document.querySelector('ul').insertAdjacentHTML('beforeend', '<li> whatever you what to add</li>")')

const searchButton = document.querySelector('form');

searchButton.addEventListener('submit', (evt) =>{
  const searchInput = document.querySelector('input[name="searchedItem"]');

  if (searchInput.value.length < 2) {
    evt.preventDefault();
  }
}
);

// document.querySelector('ul').insertAdjacentHTML('beforeend', '<li> whatever you what to add</li>")')