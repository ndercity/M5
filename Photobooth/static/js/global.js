document.addEventListener("DOMContentLoaded", function () {  
console.log("global,js is running");
	const timerEl = document.getElementById('timer');
	if (!timerEl) return;
	const interval = setInterval(() => {
		let endTime =localStorage.getItem('countdownEnd');
		if (endTime) {		
		      const remaining = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
		      	const minutes = String(Math.floor(remaining /60)).padStart(2, '0');
			const seconds = String(remaining % 60).padStart(2, '0');
			timerEl.textContent = `Time: ${minutes}:${seconds}`;
			
			if (remaining === 0) {
				clearInterval(interval);
				localStorage.removeItem('countdownEnd');
				alert("Times Up! Session terminated.");
				window.location.href = "/";
			}
		} else {
			timerEl.textContent = 'Time Left: 10:00';
		}
		}, 1000);

  function checkInternet() {
    if (!navigator.onLine) {
      alert('No internet connection. Please connect to the internet.');
      checkInternet();
    }
  }

  checkInternet();

});
