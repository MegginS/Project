const alternativeButtons = document.getElementsByClassName("saveAlternativeButton")
console.log(alternativeButtons)

function saved(e) {
  let paragraph = document.getElementById("SAVED" + e.target.value)
  paragraph.textContent = " *Saved to profile";
}

for(let i=0; i<alternativeButtons.length; i++){
  alternativeButtons[i].addEventListener("click", function(e) { 
    e.preventDefault();

    fetch('/saving-product', {
      method: 'POST',
      body: JSON.stringify({productId: e.target.value}),
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.json())
    .then(saved(e)
    );
  })
}


