// ------------------ Mobile Menu Toggle ------------------
document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.querySelector(".menu_icon");
    const navbar = document.querySelector(".navbar");

    menuIcon.addEventListener("click", () => {
        navbar.classList.toggle("active");
    });
});

// ------------------ Contact Form Demo Handler ------------------
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contact-form");
    const statusMsg = document.getElementById("msg");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        // Get input values
        const name = form.NAME.value.trim();
        const email = form.EMAIL.value.trim();
        const message = form.MESSAGE.value.trim();

        // Validation
        if (!name || !email || !message) {
            statusMsg.style.color = "orange";
            statusMsg.textContent = "⚠️ Please fill all fields.";
            return;
        }

        // Demo Success Message
        statusMsg.style.color = "#9fe29f";
        statusMsg.textContent = "✔️ Thanks! This is a demo contact form. Configure EmailJS to receive messages.";

        form.reset();

        setTimeout(() => {
            statusMsg.textContent = "";
        }, 5000);
    });
});
