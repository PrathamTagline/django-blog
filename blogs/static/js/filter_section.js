function filterSelection(category) {
    let cards = document.querySelectorAll(".card");
    let buttons = document.querySelectorAll(".filter-btn");

    // Update active button styling
    buttons.forEach((btn) => btn.classList.remove("active"));
    event.target.classList.add("active");

    // Show/hide blog cards
    cards.forEach((card) => {
      if (category === "all") {
        card.style.display = "block";
      } else {
        card.style.display = card.classList.contains(category)
          ? "block"
          : "none";
      }
    });
  }