// ======================================
// Library Management System
// Global JavaScript
// ======================================

// Confirm before deleting

document.addEventListener("DOMContentLoaded", function () {

    const deleteButtons = document.querySelectorAll(
        "button[value='delete']"
    );

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (e) {

            const confirmDelete = confirm(
                "Are you sure you want to delete this record?"
            );

            if (!confirmDelete) {

                e.preventDefault();

            }

        });

    });

});

// ================================
// Show / Hide Password
// ================================

const togglePassword = document.getElementById("togglePassword");

if (togglePassword) {

    togglePassword.addEventListener("click", function () {

        const password = document.getElementById("password");
        const icon = this.querySelector("i");

        if (password.type === "password") {

            password.type = "text";
            icon.classList.replace("fa-eye", "fa-eye-slash");

        } else {

            password.type = "password";
            icon.classList.replace("fa-eye-slash", "fa-eye");

        }

    });

}

// ======================================
// Auto Hide Flash Messages
// ======================================

document.addEventListener("DOMContentLoaded", function () {

    const flash = document.querySelector(".flash-message");

    if (flash) {

        setTimeout(function () {

            flash.style.transition = "0.5s";
            flash.style.opacity = "0";

            setTimeout(function () {
                flash.remove();
            }, 500);

        }, 3000);   // disappears after 3 seconds

    }

});

