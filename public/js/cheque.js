const downloadBtn = document.querySelector(".download-btn");
const fileLink = "https://files.africa-laws.org/contracts/Arabic/%D8%B7%D9%84%D8%A8-%D8%AA%D8%B4%D8%B7%D9%8A%D8%A8-%D9%85%D9%86-%D9%84%D8%A7%D8%A6%D8%AD%D8%A9-%D8%A7%D9%84%D9%85%D9%82%D8%A7%D9%88%D9%84-%D8%A7%D9%84%D8%B0%D8%A7%D8%AA%D9%8A.docx";

const initTimer = () => {
    if(downloadBtn.classList.contains("disable-timer")) {
        return location.href = fileLink;
    }
    let timer = downloadBtn.dataset.timer;
    downloadBtn.classList.add("timer");
    downloadBtn.innerHTML = `Your download will begin in <b>${timer}</b> seconds`;
    const initCounter = setInterval(() => {
        if(timer > 0) {
            timer--;
            return downloadBtn.innerHTML = `Your download will begin in <b>${timer}</b> seconds`;
        }
        clearInterval(initCounter);
        location.href = fileLink;
        downloadBtn.innerText = "Your file is downloading...";
        setTimeout(() => {
            downloadBtn.classList.replace("timer", "disable-timer");
            downloadBtn.innerHTML = `<span class="icon material-symbols-rounded">vertical_align_bottom</span>
                                     <span class="text">Download Again</span>`;
        }, 3000);
    }, 1000);
}

downloadBtn.addEventListener("click", initTimer);