const darkSwitch = document.querySelector(".dark-switch");
const lightSwitch = document.querySelector(".light-switch");
const body = document.querySelector("body");
const section2 = document.querySelector(".section-2");

if (localStorage.getItem("darkMode")) {
    body.classList.add("dark-mode");
    section2.classList.add("dark-bg");
    darkSwitch.classList.remove("active");
    lightSwitch.classList.add("active");
    localStorage.setItem("darkMode", "true");
}

darkSwitch.addEventListener("click", () => {
    body.classList.add("dark-mode");
    section2.classList.add("dark-bg");
    darkSwitch.classList.remove("active");
    lightSwitch.classList.add("active");
    localStorage.setItem("darkMode", "true");
})

lightSwitch.addEventListener("click", () => {
    body.classList.remove("dark-mode");
    section2.classList.remove("dark-bg");
    darkSwitch.classList.add("active");
    lightSwitch.classList.remove("active");
    localStorage.removeItem("darkMode");
})