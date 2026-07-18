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
            //icon.classList.replace("fa-eye", "fa-eye-slash");
            icon.classList.replace("fa-eye-slash", "fa-eye");

        } else {

            password.type = "password";
            //icon.classList.replace("fa-eye-slash", "fa-eye");
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

        }, 3000);   // disappears after 3 seconds

    }

});

// ==========================
// Theme Toggle
// ==========================

const themeBtn = document.getElementById("themeToggle");

if(themeBtn){

    const icon = themeBtn.querySelector("i");

    const savedTheme = localStorage.getItem("theme");

    if(savedTheme === "dark"){

        document.body.classList.add("dark");

        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");

    }

    themeBtn.addEventListener("click", function(){

        document.body.classList.toggle("dark");

        if(document.body.classList.contains("dark")){

            localStorage.setItem("theme","dark");

            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");

        }else{

            localStorage.setItem("theme","light");

            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");

        }

    });

}