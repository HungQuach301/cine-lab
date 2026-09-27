// Đạo cụ dùng chung Cổng 3 v2: cột đèn khí (luật thế giới mục 2: lồng kính trên cột ~3,4 m).
import * as THREE from './node_modules/three/build/three.module.js';

// buildGasLamp({height, mat}) → Group; userData.flame = điểm lửa (Object3D), userData.glassY = tâm lồng kính.
export function buildGasLamp({ height = 3.4, mat } = {}) {
  mat = mat || ((role, c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.7, metalness: role === 'iron' ? 0.4 : 0 }));
  const g = new THREE.Group(); g.name = 'gas_lamp';
  const iron = '#23252b';
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.085, height - 0.45, 12), mat('iron', iron)); post.position.y = (height - 0.45) / 2; g.add(post);
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.17, 0.35, 12), mat('iron', iron)); base.position.y = 0.175; g.add(base);
  const arm = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.04, 0.04), mat('iron', iron)); arm.position.y = height - 0.75; g.add(arm); // thanh ngang tựa thang
  const cage = new THREE.Group(); cage.position.y = height - 0.45; g.add(cage);
  const bot = new THREE.Mesh(new THREE.CylinderGeometry(0.10, 0.06, 0.08, 4), mat('iron', iron)); bot.rotation.y = Math.PI / 4; cage.add(bot);
  const glass = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.11, 0.42, 4, 1, true), mat('glass', '#ffcf86')); glass.rotation.y = Math.PI / 4; glass.position.y = 0.25; cage.add(glass);
  const roof = new THREE.Mesh(new THREE.ConeGeometry(0.27, 0.22, 4), mat('iron', iron)); roof.rotation.y = Math.PI / 4; roof.position.y = 0.57; cage.add(roof);
  const fin = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 6), mat('iron', iron)); fin.position.y = 0.72; cage.add(fin);
  const flame = new THREE.Mesh(new THREE.SphereGeometry(0.035, 10, 8), mat('flame', '#fff0c8')); flame.scale.set(0.8, 1.7, 0.8); flame.position.y = 0.22; cage.add(flame);
  g.traverse((o) => { if (o.isMesh) { o.castShadow = o !== flame && o !== glass; o.receiveShadow = true; } });
  g.userData = { flame, glassY: height - 0.45 + 0.25, height };
  return g;
}
