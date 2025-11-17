// --------- THREE.JS OCEAN (FULL BACKGROUND) ----------
let renderer, scene, camera, oceanMesh, oceanMaterial, oceanClock;
let targetWaveAmp = 1.0;

function initOcean() {
  const container = document.getElementById("ocean-container");
  if (!container || !window.THREE) return;

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio || 1);
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000814, 1);
  container.appendChild(renderer.domElement);

  scene = new THREE.Scene();

  const fov = 55;
  const aspect = window.innerWidth / window.innerHeight;
  const near = 0.1;
  const far = 100;
  camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
  camera.position.set(0, 7.2, 11.5);
  camera.lookAt(0, 0, 0);

  oceanClock = new THREE.Clock();

  const geometry = new THREE.PlaneGeometry(40, 40, 260, 260);
  geometry.rotateX(-Math.PI / 2);

  const vertexShader = `
    varying vec2 vUv;
    uniform float uTime;
    uniform float uWaveAmp;

    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
    }

    float noise(vec2 p) {
      vec2 i = floor(p);
      vec2 f = fract(p);

      float a = hash(i);
      float b = hash(i + vec2(1.0, 0.0));
      float c = hash(i + vec2(0.0, 1.0));
      float d = hash(i + vec2(1.0, 1.0));

      vec2 u = f * f * (3.0 - 2.0 * f);

      return mix(a, b, u.x) +
             (c - a) * u.y * (1.0 - u.x) +
             (d - b) * u.x * u.y;
    }

    void main() {
      vUv = uv;
      vec3 pos = position;

      float t = uTime * 0.5;

      float waveBig = sin(pos.x * 0.16 + t * 0.7) * 0.6;
      float waveCross = sin((pos.x + pos.z) * 0.14 - t * 0.9) * 0.5;
      float waveLong = sin(pos.z * 0.1 + t * 0.35) * 0.75;

      float n = noise(vec2(pos.x * 0.24 + t * 0.5, pos.z * 0.22 - t * 0.35));
      float n2 = noise(vec2(pos.x * 0.55 - t * 0.8, pos.z * 0.6 + t * 0.65));
      float choppy = (n - 0.5) * 1.2 + (n2 - 0.5) * 0.9;

      float height = (waveBig + waveCross + waveLong) * 0.32 + choppy * 0.55;
      height *= uWaveAmp;

      pos.y += height;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `;

  const fragmentShader = `
    varying vec2 vUv;
    uniform float uTime;

    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
    }

    float noise(vec2 p) {
      vec2 i = floor(p);
      vec2 f = fract(p);

      float a = hash(i);
      float b = hash(i + vec2(1.0, 0.0));
      float c = hash(i + vec2(0.0, 1.0));
      float d = hash(i + vec2(1.0, 1.0));

      vec2 u = f * f * (3.0 - 2.0 * f);

      return mix(a, b, u.x) +
             (c - a) * u.y * (1.0 - u.x) +
             (d - b) * u.x * u.y;
    }

    void main() {
      float t = uTime * 0.06;

      float n1 = noise(vUv * 8.0 + vec2(t * 2.0, t * -1.5));
      float n2 = noise(vUv * 14.0 + vec2(-t * 2.7, t * 2.2));
      float nFine = noise(vUv * 32.0 + vec2(t * 4.0, -t * 3.5));

      float depth = smoothstep(0.0, 1.0, vUv.y + n1 * 0.12);

      vec3 deep = vec3(0.0, 0.10, 0.22);
      vec3 mid = vec3(0.02, 0.45, 0.78);
      vec3 surf = vec3(0.78, 0.97, 1.0);

      vec3 col = mix(deep, mid, depth);
      col = mix(col, surf, pow(1.0 - depth, 3.0));

      float horizonGlow = smoothstep(0.45, 1.05, vUv.y + n1 * 0.08);
      col += vec3(0.03, 0.07, 0.13) * horizonGlow * 1.8;

      float rayPattern = sin((vUv.x * 3.4 + vUv.y * 1.35) - t * 4.0 + n2 * 3.0);
      float rays = smoothstep(0.72, 1.0, rayPattern);
      col += vec3(0.08, 0.13, 0.18) * rays * 0.9;

      float shimmer = smoothstep(0.78, 1.0, sin((vUv.x + vUv.y + t * 4.0) * 18.0 + n2 * 6.0));
      col += shimmer * 0.1;

      float caustic = noise(vUv * 22.0 + vec2(t * 5.0, -t * 4.0));
      caustic = smoothstep(0.65, 1.0, caustic);
      col += caustic * 0.09;

      float spark = smoothstep(0.92, 1.0, nFine);
      col += vec3(0.14, 0.2, 0.24) * spark * 0.65;

      vec2 center = vUv - 0.5;
      float dist = length(center);
      float vignette = smoothstep(0.8, 0.25, dist);
      col *= mix(0.74, 1.24, vignette);

      gl_FragColor = vec4(col, 1.0);
    }
  `;

  oceanMaterial = new THREE.ShaderMaterial({
    uniforms: {
      uTime: { value: 0 },
      uWaveAmp: { value: 1.0 },
    },
    vertexShader,
    fragmentShader,
    side: THREE.DoubleSide,
  });

  oceanMesh = new THREE.Mesh(geometry, oceanMaterial);
  scene.add(oceanMesh);

  const fogColor = new THREE.Color(0x000817);
  scene.fog = new THREE.Fog(fogColor, 12, 45);
  renderer.setClearColor(fogColor, 1);

  window.addEventListener("resize", onWindowResize, false);

  animateOcean();
}

function onWindowResize() {
  if (!camera || !renderer) return;
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animateOcean() {
  requestAnimationFrame(animateOcean);

  if (!oceanClock || !oceanMaterial || !camera || !renderer || !scene) return;

  const elapsed = oceanClock.getElapsedTime();
  oceanMaterial.uniforms.uTime.value = elapsed;

  const current = oceanMaterial.uniforms.uWaveAmp.value;
  oceanMaterial.uniforms.uWaveAmp.value =
    current + (targetWaveAmp - current) * 0.03;

  const sway = Math.sin(elapsed * 0.18) * 0.4;
  camera.position.x = sway;
  camera.lookAt(0, 0, 0);

  renderer.render(scene, camera);
}
