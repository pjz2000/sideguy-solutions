document.addEventListener("DOMContentLoaded",()=>{
  const targets=document.querySelectorAll("main, .hero, section");
  const memes=[
    "Google finds the problem. AI explains it. PJ finishes the mission.",
    "The internet debates. SideGuy resolves.",
    "Forums create chaos. We route clarity.",
    "Your HVAC guy, payment guy, and AI guy finally shook hands."
  ];

  targets.forEach((el,i)=>{
    if(i===0){
      const wrap=document.createElement("div");
      wrap.className="meme-wow-band reveal-up";
      wrap.innerHTML=`
        <div class="wow-ticker"><span>🌊 SIDEGUY SIGNAL • MEMES • HUMAN RESOLUTION • WOW FACTOR • TEXT PJ • COASTAL FUTURE • </span></div>
        <div class="meme-grid">
          ${memes.map(m=>`<div class="meme-card">${m}</div>`).join("")}
        </div>
      `;
      el.appendChild(wrap);
    }
  });

  const io=new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting) e.target.classList.add("visible");
    });
  });
  document.querySelectorAll(".reveal-up").forEach(el=>io.observe(el));
});
