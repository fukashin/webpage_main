let startTime;
let elapsedTime = 0;
let timerInterval;
let initialOffset = 0;


function timeToString(time) {
    let totalSeconds = time / 1000;
    let positive = totalSeconds >= 0;
    let absSeconds = Math.floor(Math.abs(totalSeconds));
    let hours = Math.floor(absSeconds / 3600);
    let minutes = Math.floor((absSeconds % 3600) / 60);
    let seconds = Math.floor(absSeconds % 60);
    let milliseconds = Math.abs(time % 1000);

    let formattedHH = hours.toString().padStart(2, '0');
    let formattedMM = minutes.toString().padStart(2, '0');
    let formattedSS = seconds.toString().padStart(2, '0');
    let formattedMS = milliseconds.toString().padStart(3, '0');

    return (positive ? "" : "-") + `${formattedHH}:${formattedMM}:${formattedSS}.${formattedMS}`;
}

function print(txt) {
    document.getElementById("time").innerHTML = txt;
}

function start() {
    startTime = Date.now() - elapsedTime;
    timerInterval = setInterval(function printTime() {
        elapsedTime = Date.now() - startTime + initialOffset;
        print(timeToString(elapsedTime));
    }, 100);  // 100ミリ秒ごとに更新
    document.getElementById("startStop").textContent = "一時停止";
}

function pause() {
    clearInterval(timerInterval);
    document.getElementById("startStop").textContent = "スタート";
}

function reset() {
    clearInterval(timerInterval);
    elapsedTime = 0;
    print(timeToString(0));
    document.getElementById("startStop").textContent = "スタート";
}

document.getElementById("startStop").addEventListener("click", function() {
    if (this.textContent === "スタート") {
        start();
    } else {
        pause();
    }
});

document.getElementById("reset").addEventListener("click", reset);
