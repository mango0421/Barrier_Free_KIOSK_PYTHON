let timer = setTimeout(() => {
  window.location.href = '/home';
}, 120000);

document.addEventListener('click', () => {
  clearTimeout(timer);
  timer = setTimeout(() => { window.location.href = '/home'; }, 120000);
});

function playTTS(text) {
  fetch(`/tts?text=${encodeURIComponent(text)}`)
    .then((res) => res.blob())
    .then((blob) => {
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.play();
    });
}

function openMap() {
  window.open('/static/images/map/clinic_map.png', '_blank');
}
