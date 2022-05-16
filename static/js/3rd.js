const darkSwitch = document.querySelector(".dark-switch");
const lightSwitch = document.querySelector(".light-switch");
const body = document.querySelector("body");
const btn = document.querySelector(".main-btn")
//const btn_back = document.querySelector(".btn-back")
const section3 = document.querySelector(".section-3");

if (localStorage.getItem("darkMode")) {
    body.classList.add("dark-mode");
    section3.classList.add("dark-bg");
    darkSwitch.classList.remove("active");
    lightSwitch.classList.add("active");
    btn.classList.add("dark");
    //btn_back.classList.add("dark-2");
    localStorage.setItem("darkMode", "true");
}

darkSwitch.addEventListener("click", () => {
    body.classList.add("dark-mode");
    section3.classList.add("dark-bg");
    darkSwitch.classList.remove("active");
    lightSwitch.classList.add("active");
    btn.classList.add("dark");
    //btn_back.classList.add("dark");
    localStorage.setItem("darkMode", "true");
})

lightSwitch.addEventListener("click", () => {
    body.classList.remove("dark-mode");
    section3.classList.remove("dark-bg");
    darkSwitch.classList.add("active");
    lightSwitch.classList.remove("active");
    btn.classList.remove("dark");
    //btn_back.classList.remove("dark");
    localStorage.removeItem("darkMode");
})

// Image
document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");
  
    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });
  
    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });
  
    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });
  
    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });
  
    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();
  
      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }
  
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });
  
  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
  
    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }
  
    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }
  
    thumbnailElement.dataset.label = file.name;
  
    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
  
      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }