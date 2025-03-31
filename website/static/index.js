function deleteNote(noteId) {
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = '/'; // Redirect to home page
  });
}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

document.addEventListener("DOMContentLoaded", function () {
    const deleteCardModal = document.getElementById("deleteCardModal");
    const deleteCardIdInput = document.getElementById("deleteCardId");

    deleteCardModal.addEventListener("show.bs.modal", function (event) {
      const button = event.relatedTarget;  // Button that triggered the modal
      const cardName = button.getAttribute("data-card-name");
      const cardId = button.getAttribute("data-card-id");

      // Update modal text
      document.getElementById("modalCardName").textContent = cardName;

      // Update form hidden input
      document.getElementById("modalCardId").value = cardId;
  });

    document.querySelectorAll(".delete-card-btn").forEach(button => {
        button.addEventListener("click", function () {
            const cardId = this.getAttribute("data-card-id");
            const cardName = this.getAttribute("data-card-name");

            // Set the hidden input value
            deleteCardIdInput.value = cardId;

            // Update the modal text
            document.querySelector("#deleteCardModal .modal-body strong").textContent = cardName;
        });
    });
});


// document.addEventListener("DOMContentLoaded", function () {
//     // Toggle sub-decks when clicking the arrow
//     document.querySelectorAll(".deck-toggle").forEach(button => {
//         button.addEventListener("click", function () {
//             const subDecks = this.closest(".deck-item").querySelector(".sub-decks");
//             if (subDecks) {
//                 subDecks.classList.toggle("d-none");
//                 this.classList.toggle("rotated"); // Optional: Add rotation animation to arrow
//             }
//         });
//     });
// });