// Arte de marca de Mi Primer Acuario: un tetra cardenal estilizado.
// design/render.py usa estas funciones para generar el ícono, el splash y el gráfico de la tienda.
const DEFS = `
<linearGradient id="gBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6FAFC"/><stop offset=".55" stop-color="#A9D3DE"/><stop offset="1" stop-color="#7FA9B8"/></linearGradient>
<linearGradient id="gNeon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2AB8E8"/><stop offset=".6" stop-color="#5EF3FF"/><stop offset="1" stop-color="#9AFBFF"/></linearGradient>
<linearGradient id="gRed" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E23B4E"/><stop offset="1" stop-color="#FF6B6B"/></linearGradient>
<linearGradient id="gFin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D8F4F8" stop-opacity=".95"/><stop offset="1" stop-color="#8FC3D1" stop-opacity=".75"/></linearGradient>
<radialGradient id="gSea" cx=".5" cy=".3" r=".85"><stop offset="0" stop-color="#13798A"/><stop offset=".5" stop-color="#073543"/><stop offset="1" stop-color="#03111A"/></radialGradient>
<radialGradient id="gGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#40E0E8" stop-opacity=".35"/><stop offset="1" stop-color="#40E0E8" stop-opacity="0"/></radialGradient>
<clipPath id="cBody"><path d="M300 512C352 404 486 352 620 372C712 386 776 446 812 512C776 578 712 638 620 652C486 672 352 620 300 512Z"/></clipPath>`;

const FISH = `
<g>
  <path d="M332 512C292 468 252 420 200 388C226 448 232 480 232 512C232 544 226 576 200 636C252 604 292 556 332 512Z" fill="url(#gFin)"/>
  <path d="M540 384C556 320 598 298 652 292C630 328 622 358 624 380Z" fill="url(#gFin)"/>
  <path d="M300 512C352 404 486 352 620 372C712 386 776 446 812 512C776 578 712 638 620 652C486 672 352 620 300 512Z" fill="url(#gBody)"/>
  <g clip-path="url(#cBody)">
    <path d="M290 522C430 554 590 560 692 536C704 572 700 612 680 652L270 712Z" fill="url(#gRed)"/>
    <path d="M332 522C452 462 622 446 792 482C624 482 456 500 332 522Z" fill="url(#gNeon)"/>
    <path d="M380 438C470 396 590 382 700 410" fill="none" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="12" stroke-linecap="round"/>
    <path d="M702 428C680 480 682 548 706 600" fill="none" stroke="#03111A" stroke-opacity=".16" stroke-width="7" stroke-linecap="round"/>
  </g>
  <path d="M566 636C586 688 614 712 654 718C634 690 628 664 630 644Z" fill="url(#gFin)" opacity=".85"/>
  <circle cx="744" cy="486" r="25" fill="#F4FBFC"/><circle cx="750" cy="487" r="14" fill="#03111A"/><circle cx="755" cy="481" r="4.5" fill="#FFFFFF"/>
</g>`;

const BUBBLES = `<g fill="none" stroke="#CFF7FA" stroke-width="7"><circle cx="836" cy="372" r="30" opacity=".75"/><circle cx="866" cy="288" r="20" opacity=".6"/><circle cx="836" cy="222" r="12" opacity=".5"/></g>`;

function sea() {
  return `<rect width="1024" height="1024" fill="url(#gSea)"/>
  <g fill="#FFFFFF" opacity=".05"><path d="M300 0L420 0L250 1024L120 1024Z"/><path d="M560 0L640 0L560 1024L470 1024Z"/><path d="M800 0L860 0L900 1024L820 1024Z"/></g>
  <path d="M0 880C190 840 360 900 540 868C720 836 870 884 1024 852L1024 1024L0 1024Z" fill="#0B3A44" opacity=".9"/>
  <path d="M0 930C220 900 380 950 600 924C780 902 900 940 1024 918L1024 1024L0 1024Z" fill="#082B33"/>`;
}

// Ícono completo (Play Store 512, iOS, icon-only)
function iconFull() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024"><defs>${DEFS}</defs>${sea()}
  <circle cx="520" cy="512" r="330" fill="url(#gGlow)"/>
  <g transform="translate(512 512) scale(1.02) translate(-528 -500)">${FISH}${BUBBLES}</g></svg>`;
}
// Capa delantera del ícono adaptativo de Android (@capacitor/assets ya la encoge a la zona segura)
function iconFg() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024"><defs>${DEFS}</defs>
  <g transform="translate(512 512) scale(.9) translate(-528 -500)">${FISH}${BUBBLES}</g></svg>`;
}
function iconBg() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024"><defs>${DEFS}</defs>${sea()}<circle cx="512" cy="512" r="300" fill="url(#gGlow)"/></svg>`;
}
function fishOnly(scale) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><defs>${DEFS}</defs><circle cx="512" cy="512" r="380" fill="url(#gGlow)"/>
  <g transform="translate(512 512) scale(${scale || 1}) translate(-528 -500)">${FISH}${BUBBLES}</g></svg>`;
}
window.ART = { iconFull, iconFg, iconBg, fishOnly };
