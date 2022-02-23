console.log("js is working")

// document.getElementById("save-product").addEventListener("click", evt => {
//     evt.preventDefault();
// })

const alternativeButtons = document.getElementsByClassName("saveAlternativeButton")
console.log(alternativeButtons)

for(let i=0; i<alternativeButtons.length; i++){
  alternativeButtons[i].addEventListener("click", function(e) { 
    e.preventDefault();
    // console.log("clicked")
    // console.log(e.target.value)

    fetch('/saving-product', {
      method: 'POST',
      body: JSON.stringify({productId: e.target.value}),
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then((response) => {console.log(response)})
    .catch((error) => {console.log(error)})
  })
}

// Array.prototype.forEach.call(alternativeButtons, (element) => {
//   element.addEventListener("submit", (evt) => {
//     evt.preventDefault();
//     console.log("alternative button is working")
//     console.log(evt.target.value)
//   })
// })


    // const input = {
    //   ids: document.getElementById('save-product').value,
    // };

    // fetch('/saving-products', {
    //   method: 'POST',
    //   body: JSON.stringify(input),
    //   headers: {
    //   'Content-Type': 'application/json',
    // },
    // })
    //   .then(response => {}
    //   );


