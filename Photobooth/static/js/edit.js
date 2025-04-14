document.addEventListener("DOMContentLoaded", function () {
    console.log("edit selection page loaded.");

    const modeButtons = document.querySelectorAll('.mode-selection-buttons')
    const modeFilter = document.querySelectorAll('.mode-set')
    const imageFeed = document.getElementById("image-feed");

    //test functions
    function startCamera(){
        imageFeed.src = "/video_feed?" + new Date().getTime();
    }

    function stopCamera(){
        videoFeed.src = "";
        fetch("/stop_camera");
    }

    window.addEventListener("load", startCamera);
    window.addEventListener("beforeunload", stopCamera);
    //end of test functions

    modeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            modeButtons.forEach(b => b.classList.remove('active'));  
            btn.classList.add('active'); 

            modeFilter.forEach(set=>set.classList.remove('visible'));
            const target = btn.getAttribute('data-target');
            document.getElementById(target).classList.add('visible');
        });
    });
});
