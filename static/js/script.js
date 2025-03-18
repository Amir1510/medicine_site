document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinksContainer = document.querySelector(
      ".nav-links-container"
    );

    menuToggle.addEventListener("click", function () {
      navLinksContainer.classList.toggle("active");
    });

    // Закрывать меню при клике на ссылку
    const navLinks = document.querySelectorAll(".nav-links a");
    navLinks.forEach((link) => {
      link.addEventListener("click", function () {
        navLinksContainer.classList.remove("active");
      });
    });

    // Функционал карты
    const showMapBtn = document.getElementById("showMapBtn");
    const mapContainer = document.getElementById("map");
    let map;

    showMapBtn.addEventListener("click", function () {
      if (mapContainer.style.display === "none") {
        mapContainer.style.display = "block";
        if (!map) {
          ymaps.ready(initMap);
        }
      } else {
        mapContainer.style.display = "none";
      }
    });

    function initMap() {
      map = new ymaps.Map("map", {
        center: [55.807754, 37.495313], // Координаты ГКБ №52
        zoom: 15,
      });

      const placemark = new ymaps.Placemark([55.807754, 37.495313], {
        balloonContent: "ГКБ №52, Отделение переливания крови",
      });

      map.geoObjects.add(placemark);
    }
  });

  function logout() {
    fetch("{% url 'logout' %}", {
      method: "POST",
      headers: {
        "X-CSRFToken": "{{ csrf_token }}",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      credentials: "include",
    }).then((response) => {
      if (response.ok) {
        window.location.href = "/";
      }
    });
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    var messages = document.querySelectorAll(".alert");
    messages.forEach(function (message) {
      setTimeout(function () {
        message.style.display = "none";
      }, 5000);
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
    var dateInput = document.getElementById('donation_date');
    dateInput.addEventListener('change', function() {
      var selectedDate = new Date(this.value);
      if (selectedDate.getDay() === 0) {
        alert('Донации не проводятся по воскресеньям. Пожалуйста, выберите другой день.');
        this.value = '';
      }
    });
  });
