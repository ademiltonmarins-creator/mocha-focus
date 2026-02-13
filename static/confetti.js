function confetti() {
  for (let i = 0; i < 30; i++) {
    const el = document.createElement("div");
    el.style.position = "fixed";
    el.style.left = Math.random() * 100 + "vw";
    el.style.top = "-10px";
    el.style.width = "8px";
    el.style.height = "8px";
    el.style.background = ["#00ff99","#00ccff","#6a5cff"][Math.floor(Math.random()*3)];
    el.style.opacity = 0.8;
    document.body.appendChild(el);

    let fall = setInterval(() => {
      el.style.top = (el.offsetTop + 5) + "px";
      if (el.offsetTop > window.innerHeight) {
        el.remove();
        clearInterval(fall);
      }
    }, 20);
  }
}
