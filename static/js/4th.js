const darkSwitch = document.querySelector(".dark-switch");
const lightSwitch = document.querySelector(".light-switch");
const body = document.querySelector("body");
const section4 = document.querySelector(".section-4");
const card = document.querySelectorAll(".card")

if (localStorage.getItem("darkMode")) {
    body.classList.add("dark-mode");
    section4.classList.add("dark-bg");
    darkSwitch.classList.remove("active");
    lightSwitch.classList.add("active");
    for (var i = 0; i < card.length; ++i) {
        card[i].classList.add('dark');
    }
    localStorage.setItem("darkMode", "true");
}

darkSwitch.addEventListener("click", () => {
    body.classList.add("dark-mode");
    section4.classList.add("dark-bg");
    darkSwitch.classList.remove("active");
    lightSwitch.classList.add("active");
    for (var i = 0; i < card.length; ++i) {
        card[i].classList.add('dark');
    }
    localStorage.setItem("darkMode", "true");
})

lightSwitch.addEventListener("click", () => {
    body.classList.remove("dark-mode");
    section4.classList.remove("dark-bg");
    darkSwitch.classList.add("active");
    lightSwitch.classList.remove("active");
    for (var i = 0; i < card.length; ++i) {
        card[i].classList.remove('dark');
    }
    localStorage.removeItem("darkMode");
})