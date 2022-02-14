document.getElementById("save-product").addEventListener("click", evt => {
    evt.preventDefault();

    const input = {
      ids: document.getElementById('save-product').value,
    };

    fetch('/saving-products', {
      method: 'POST',
      body: JSON.stringify(input),
      headers: {
      'Content-Type': 'application/json',
    },
    })
      .then(response => {}
      );
  });

