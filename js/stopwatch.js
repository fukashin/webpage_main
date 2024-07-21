let startTime;
let elapsedTime = 0;
let timerInterval;

function timeToString(time) {
    let diffInHrs = time / 3600000;
    let hh = Math.floor(diffInHrs);

    let diffInMin = (diffInHrs - hh) * 60;
    let mm = Math.floor(diffInMin);

    let diffInSec = (diffInMin - mm) * 60;
    let ss = Math.floor(diffInSec);

    let diffInMs = (diffInSec - ss) * 100;
    let ms = Math.floor(diffInMs);

    let formattedHH = hh.toString().padStart(2, '0');
    let formattedMM = mm.toString().padStart(2, '0');
    let formattedSS = ss.toString().padStart(2, '0');

    return `${formattedHH}:${formattedMM}:${formattedSS}`;
}

function print(txt) {
    document.getElementById("time").innerHTML = txt;
}

function start() {
    startTime = Date.now() - elapsedTime;
    timerInterval = setInterval(function printTime() {
        elapsedTime = Date.now() - startTime;
        print(timeToString(elapsedTime));
    }, 10);
    showButton("PAUSE");
}

function pause() {
    clearInterval(timerInterval);
    showButton("PLAY");
}

function reset() {
    clearInterval(timerInterval);
    print("00:00:00");
    elapsedTime = 0;
    showButton("PLAY");
    sessionStorage.removeItem("storedTime");  // セッションストレージから時間を削除
}

function showButton(buttonKey) {
    const buttonToShow = buttonKey === "PLAY" ? start : pause;
    const buttonToHide = buttonKey === "PLAY" ? pause : start;
    buttonToShow.style.display = "block";
    buttonToHide.style.display = "none";
}

// セッションストレージから時間を読み込む
window.onload = function() {
    if (sessionStorage.getItem("storedTime")) {
        elapsedTime = parseInt(sessionStorage.getItem("storedTime"));
        print(timeToString(elapsedTime));
    }
    showButton("PLAY");
}

document.getElementById("startStop").addEventListener("click", function() {
    if (timerInterval) {
        pause();
        sessionStorage.setItem("storedTime", elapsedTime.toString());  // セッションストレージに時間を保存
    } else {
        start();
    }
});

document.getElementById("reset").addEventListener("click", reset);
