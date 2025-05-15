document.addEventListener("DOMContentLoaded", function () {
  function checkInternet() {
    if (!navigator.onLine) {
      alert('No internet connection. Please connect to the internet.');
      checkInternet();
    }
  }

  checkInternet();
});
