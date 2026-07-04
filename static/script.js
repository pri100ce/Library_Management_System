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