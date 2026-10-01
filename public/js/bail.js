const downloadBtn = document.querySelector(".download-btn");
const fileLink = "https://files.africa-laws.org/contracts/Lease-agreement/%D8%B9%D9%82%D8%AF-%D9%83%D8%B1%D8%A7%D8%A1-%D8%B4%D9%82%D8%A9-%D8%B3%D9%83%D9%86%D9%8A%D8%A9.docx";

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