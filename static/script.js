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
            icon.classList.replace("fa-eye-slash", "fa-eye");

        } else {

            password.type = "password";
            icon.classList.replace("fa-eye", "fa-eye-slash");

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

        }, 3000);

    }

});

// ==========================
// Theme Toggle
// ==========================

const themeBtn = document.getElementById("themeToggle");

if (themeBtn) {

    const icon = themeBtn.querySelector("i");

    // Set correct icon based on current theme
    if (document.body.classList.contains("dark")) {

        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");

    }

    themeBtn.addEventListener("click", function () {

        document.body.classList.toggle("dark");

        const theme = document.body.classList.contains("dark")
            ? "dark"
            : "light";

        // Change icon
        if (theme === "dark") {

            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");

        } else {

            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");

        }

        // Save theme in database
        fetch("/save-theme", {

            method: "POST",

            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },

            body: "theme=" + encodeURIComponent(theme)

        })
        .then(response => response.json())
        .then(data => {

            if (!data.success) {

                console.error("Theme could not be saved.");

            }

        })
        .catch(error => {

            console.error("Error saving theme:", error);

        });

    });

}