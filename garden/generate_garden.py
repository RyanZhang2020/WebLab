import webbrowser
import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Beautiful Garden</title>
    <style>
        body { margin: 0; overflow: hidden; background: linear-gradient(to bottom, #87CEEB 0%, #E0F7FA 50%, #4CAF50 50%, #2E7D32 100%); }
        #canvas { display: block; }
        .controls { position: absolute; top: 10px; left: 10px; background: rgba(255,255,255,0.8); padding: 10px; border-radius: 8px; font-family: sans-serif; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        button { padding: 8px 16px; font-size: 14px; cursor: pointer; background: #E91E63; color: white; border: none; border-radius: 4px; }
        button:hover { background: #D81B60; }
    </style>
</head>
<body>
    <div class="controls">
        <button onclick="drawGarden()">Regenerate Garden</button>
    </div>
    <canvas id="canvas"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        // Resize canvas to fill window
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Seeded random
        let _seed = 1;
        function seed(s) { _seed = s; }
        function seededRandom(min, max) {
            _seed = (_seed * 9301 + 49297) % 233280;
            const rnd = _seed / 233280;
            return min + rnd * (max - min);
        }

        function random(min, max) {
            return min + Math.random() * (max - min);
        }

        function drawPetal(x, y, radius, angle, color, lengthScale) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);
            
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(radius * 0.5, radius * 0.5, radius * lengthScale, radius * lengthScale * 0.5, radius * lengthScale, 0);
            ctx.bezierCurveTo(radius * lengthScale, -radius * lengthScale * 0.5, radius * 0.5, -radius * 0.5, 0, 0);
            
            ctx.fill();
            ctx.strokeStyle = "rgba(0,0,0,0.1)";
            ctx.lineWidth = 1;
            ctx.stroke();
            ctx.restore();
        }

        function drawFlower(f) {
            // Restore seed for consistent flower structure
            seed(f.seed);
            
            const rootX = f.x;
            const rootY = f.y;

            const stemHeight = seededRandom(50, 200);
            const stemHue = seededRandom(100, 140);
            const stemColor = `hsl(${stemHue}, ${seededRandom(60, 80)}%, ${seededRandom(30, 50)}%)`;
            
            // Dynamic Wind calculation
            // Time-based wave + spatial offset
            const time = Date.now() / 1500;
            const wind = Math.sin(time + rootX * 0.005) * 20 + Math.sin(time * 2 + rootX * 0.01) * 8;
            
            const headY = rootY - stemHeight;
            // Static sway (randomness) + Dynamic Wind
            const staticSway = seededRandom(-20, 20); 
            const headX = rootX + staticSway + wind;

            // Draw Stem
            ctx.beginPath();
            ctx.moveTo(rootX, rootY); 
            const ctrlX = rootX + seededRandom(-10, 10) + wind * 0.5; // Stem bends with wind
            ctx.quadraticCurveTo(ctrlX, rootY - stemHeight/2, headX, headY);
            ctx.strokeStyle = stemColor;
            ctx.lineWidth = seededRandom(2, 5);
            ctx.stroke();

            // Leaf
            if (seededRandom(0, 1) > 0.3) {
                ctx.beginPath();
                const leafRatio = seededRandom(0.3, 0.7);
                const leafY = rootY - stemHeight * leafRatio;
                // Simple lerp for X
                const leafX = rootX + (headX - rootX) * leafRatio;
                
                const dir = seededRandom(-1, 1) > 0 ? 1 : -1;
                ctx.moveTo(leafX, leafY);
                ctx.quadraticCurveTo(leafX + (30*dir), leafY - 10, leafX + (40*dir), leafY - 20);
                ctx.quadraticCurveTo(leafX + (20*dir), leafY + 10, leafX, leafY + 5);
                ctx.fillStyle = stemColor;
                ctx.fill();
            }

            // Draw Flower Head
            const petalCount = Math.floor(seededRandom(8, 20));
            const radius = seededRandom(10, 25);
            const hue = seededRandom(0, 360);
            const saturation = seededRandom(70, 100);
            const lightness = seededRandom(40, 70);
            
            const centerColor = `hsl(${seededRandom(30, 60)}, 100%, 50%)`;

            const layers = Math.floor(seededRandom(1, 4));
            
            for(let L=0; L<layers; L++) {
                const layerRadius = radius * (1 - L*0.2);
                const layerColor = `hsl(${hue}, ${saturation}%, ${lightness + L*10}%)`;
                const scale = seededRandom(1.2, 1.8);
                
                for (let i = 0; i < petalCount; i++) {
                    const angle = (Math.PI * 2 / petalCount) * i + (L * 0.1);
                    drawPetal(headX, headY, layerRadius, angle, layerColor, scale);
                }
            }

            // Center
            ctx.beginPath();
            ctx.arc(headX, headY, radius * 0.4, 0, Math.PI * 2);
            ctx.fillStyle = centerColor;
            ctx.fill();
            
            ctx.fillStyle = "rgba(0,0,0,0.2)";
            for(let i=0; i<5; i++){
                ctx.beginPath();
                ctx.arc(headX + seededRandom(-2,2), headY + seededRandom(-2,2), 1, 0, Math.PI*2);
                ctx.fill();
            }
        }

        function drawCloud(x, y, s) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
            ctx.beginPath();
            ctx.arc(x, y, 30*s, 0, Math.PI * 2);
            ctx.arc(x + 25*s, y - 10*s, 35*s, 0, Math.PI * 2);
            ctx.arc(x + 50*s, y, 30*s, 0, Math.PI * 2);
            ctx.fill();
        }

        function drawRabbit(x, y, s, lookingLeft) {
            ctx.save();
            ctx.translate(x, y);
            if (lookingLeft) {
                ctx.scale(-s, s);
            } else {
                ctx.scale(s, s);
            }

            ctx.fillStyle = "#ecf0f1"; // White fur
            
            // Body
            ctx.beginPath();
            ctx.ellipse(0, 5, 20, 15, 0, 0, Math.PI*2);
            ctx.fill();

            // Head
            ctx.beginPath();
            ctx.ellipse(15, -5, 12, 10, 0, 0, Math.PI*2);
            ctx.fill();

            // Ears
            ctx.fillStyle = "#bdc3c7";
            ctx.beginPath();
            ctx.ellipse(12, -20, 4, 15, -0.2, 0, Math.PI*2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(18, -20, 4, 15, 0.2, 0, Math.PI*2);
            ctx.fill();

            // Eye
            ctx.fillStyle = "black";
            ctx.beginPath();
            ctx.arc(18, -8, 1.5, 0, Math.PI*2);
            ctx.fill();

            // Tail
            ctx.fillStyle = "#ecf0f1";
            ctx.beginPath();
            ctx.arc(-20, 5, 6, 0, Math.PI*2);
            ctx.fill();

            ctx.restore();
        }

        function drawButterfly(x, y, s) {
            ctx.save();
            ctx.translate(x, y);
            ctx.scale(s, s);

            const colors = ["#e74c3c", "#f1c40f", "#3498db", "#9b59b6"];
            const color = colors[Math.floor(random(0, colors.length))];
            
            ctx.fillStyle = color;
            
            // Left Wing
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(-15, -20, -25, 0, 0, 0);
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(-10, 20, -20, 5, 0, 0);
            ctx.fill();

            // Right Wing
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(15, -20, 25, 0, 0, 0);
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(10, 20, 20, 5, 0, 0);
            ctx.fill();
            
            // Body
            ctx.strokeStyle = "rgba(0,0,0,0.5)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, -10);
            ctx.lineTo(0, 10);
            ctx.stroke();

            ctx.restore();
        }

        function drawFish(x, y, s, lookingLeft) {
            ctx.save();
            ctx.translate(x, y);
            ctx.scale(lookingLeft ? -s : s, s);

            // Body
            ctx.fillStyle = "#FF7043"; 
            ctx.beginPath();
            ctx.ellipse(0, 0, 10, 6, 0, 0, Math.PI * 2);
            ctx.fill();

            // Tail
            ctx.fillStyle = "#F4511E";
            ctx.beginPath();
            ctx.moveTo(-10, 0);
            ctx.lineTo(-18, -6);
            ctx.lineTo(-18, 6);
            ctx.closePath();
            ctx.fill();

            // Eye
            ctx.fillStyle = "white";
            ctx.beginPath();
            ctx.arc(4, -2, 2, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "black";
            ctx.beginPath();
            ctx.arc(5, -2, 1, 0, Math.PI * 2);
            ctx.fill();
            
            // Fin
            ctx.fillStyle = "#FFAB91";
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(-4, -8);
            ctx.lineTo(4, -2);
            ctx.fill();

            ctx.restore();
        }

        function drawBird(x, y, s, color, lookingLeft) {
            ctx.save();
            ctx.translate(x, y);
            if (lookingLeft) {
                ctx.scale(-s, s); // Flip horizontally
            } else {
                ctx.scale(s, s);
            }
            
            // Body
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(0, 0, 15, 0, Math.PI * 2);
            ctx.fill();
            
            // Belly
            ctx.fillStyle = "rgba(255,255,255,0.6)";
            ctx.beginPath();
            ctx.arc(-5, 5, 10, 0, Math.PI * 2);
            ctx.fill();

            // Eye
            ctx.fillStyle = "white";
            ctx.beginPath();
            ctx.arc(5, -5, 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "black";
            ctx.beginPath();
            ctx.arc(7, -5, 1.5, 0, Math.PI * 2);
            ctx.fill();

            // Beak
            ctx.fillStyle = "orange";
            ctx.beginPath();
            ctx.moveTo(10, -2);
            ctx.lineTo(18, 1);
            ctx.lineTo(10, 4);
            ctx.fill();

            // Wing
            ctx.fillStyle = "rgba(0,0,0,0.1)";
            ctx.beginPath();
            ctx.ellipse(-2, 2, 8, 5, 0.5, 0, Math.PI*2);
            ctx.fill();

            // Legs
            ctx.strokeStyle = "orange";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(-5, 12);
            ctx.lineTo(-5, 20);
            ctx.moveTo(5, 12);
            ctx.lineTo(5, 20);
            ctx.stroke();

            ctx.restore();
        }

        function drawSunrise() {
             const w = canvas.width;
             const h = canvas.height;
             const horizon = h / 2;

             // Sky Gradient
             const sky = ctx.createLinearGradient(0, 0, 0, horizon);
             sky.addColorStop(0, "#2c3e50");      // Deep Blue
             sky.addColorStop(0.5, "#8e44ad");    // Purple
             sky.addColorStop(0.8, "#e74c3c");    // Orange Red
             sky.addColorStop(1.0, "#f1c40f");    // Golden Yellow
             
             ctx.fillStyle = sky;
             ctx.fillRect(0, 0, w, horizon);

             // Sun
             const sunX = w / 2;
             const sunY = horizon - 50; 
             
             ctx.save();
             // Sun Glow
             ctx.shadowBlur = 80;
             ctx.shadowColor = "#f1c40f";
             ctx.fillStyle = "#f39c12";
             
             ctx.beginPath();
             ctx.arc(sunX, sunY, 60, 0, Math.PI*2);
             ctx.fill();
             ctx.restore();

             // Ground Gradient
             const ground = ctx.createLinearGradient(0, horizon, 0, h);
             ground.addColorStop(0, "#2ecc71");   // Lit Grass
             ground.addColorStop(1, "#27ae60");   // Shadowy Grass (near bottom)
             
             ctx.fillStyle = ground;
             ctx.fillRect(0, horizon, w, h - horizon);
        }

        function drawRiver() {
             const h = canvas.height;
             const w = canvas.width;
             const horizon = h / 2;
             
             // River Parameters
             const riverBaseY = horizon + 120; // In front of Villa (Villa is at horizon+30)
             const riverWidth = 50;
             const time = Date.now() / 2000;
             
             ctx.beginPath();
             // Top Bank
             ctx.moveTo(0, riverBaseY);
             for(let x = 0; x <= w; x += 20) {
                 const wave = Math.sin(x * 0.005 + time) * 10;
                 ctx.lineTo(x, riverBaseY + wave);
             }
             
             // Bottom Bank
             for(let x = w; x >= 0; x -= 20) {
                 const wave = Math.sin(x * 0.005 + time) * 10;
                 ctx.lineTo(x, riverBaseY + riverWidth + wave);
             }
             ctx.closePath();
             
             const rGrad = ctx.createLinearGradient(0, riverBaseY, 0, riverBaseY + riverWidth);
             rGrad.addColorStop(0, "#81D4FA"); // Light Blue
             rGrad.addColorStop(1, "#0277BD"); // Deep Blue
             ctx.fillStyle = rGrad;
             ctx.fill();
             
             // Water Glint/Sparkles
             ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
             for(let i=0; i<20; i++) {
                 // Use a pseudo-random position based on time to make them twinkle/move
                 const sparkleSpeed = 50;
                 const sx = (Date.now() / 10 + i * 143) % w; // Prime number spacing
                 const waveAtX = Math.sin(sx * 0.005 + time) * 10;
                 const sy = riverBaseY + waveAtX + (i % 3) * (riverWidth/4) + 10;
                 
                 ctx.beginPath();
                 ctx.arc(sx, sy, 1.5, 0, Math.PI*2);
                 ctx.fill();
             }
        }

        function drawVilla() {
             const h = canvas.height;
             const w = canvas.width;
             const horizon = h / 2;
             
             // Villa Position
             const vx = w * 0.7;
             const vy = horizon + 30;
             const scale = 0.8;
             
             ctx.save();
             ctx.translate(vx, vy);
             ctx.scale(scale, scale);
             
             const cFront = "#fdf5e6"; 
             const cSide = "#e0d6c8"; // Slight shadow
             const cRoofFront = "#c0392b";
             const cRoofSide = "#922b21";
             const cOutline = "#5d4037"; // Dark brown outline

             ctx.lineJoin = "round";
             ctx.lineWidth = 2;
             ctx.strokeStyle = cOutline;

             // --- Dimensions ---
             const wFront = 150;
             const hWall = 120;
             const depthX = 60;
             const depthY = -25; // vanishing perspective upwards

             // --- Side Wall (Receding) ---
             ctx.fillStyle = cSide;
             ctx.beginPath();
             ctx.moveTo(wFront, -hWall);       // Top-Right Front
             ctx.lineTo(wFront + depthX, -hWall + depthY); // Top-Right Back
             ctx.lineTo(wFront + depthX, 0 + depthY);      // Bottom-Right Back
             ctx.lineTo(wFront, 0);            // Bottom-Right Front
             ctx.closePath();
             ctx.fill();
             ctx.stroke();

             // --- Front Wall ---
             ctx.fillStyle = cFront;
             ctx.fillRect(0, -hWall, wFront, hWall);
             ctx.strokeRect(0, -hWall, wFront, hWall);

             // --- Roof (Side Plane) ---
             ctx.fillStyle = cRoofSide;
             ctx.beginPath();
             ctx.moveTo(wFront/2, -190);       // Front Peak
             ctx.lineTo(wFront + 20, -hWall);  // Front Right Overhang
             ctx.lineTo(wFront + 20 + depthX, -hWall + depthY); // Back Right Overhang
             ctx.lineTo(wFront/2 + depthX, -190 + depthY); // Back Peak
             ctx.closePath();
             ctx.fill();
             ctx.stroke();

             // --- Roof (Front Triangle) ---
             ctx.fillStyle = cRoofFront;
             ctx.beginPath();
             ctx.moveTo(-20, -hWall); // Overhang Left
             ctx.lineTo(wFront/2, -190);   // Peak
             ctx.lineTo(wFront + 20, -hWall);  // Overhang Right
             ctx.closePath();
             ctx.fill();
             ctx.stroke();

             // --- Door (3D recessed?) ---
             // Just flat on front is fine, maybe a small step?
             ctx.fillStyle = "#5d4037"; // Brown
             ctx.fillRect(60, -60, 40, 60);
             ctx.strokeRect(60, -60, 40, 60);
             
             // Step
             ctx.fillStyle = "#95a5a6";
             ctx.beginPath();
             ctx.moveTo(55, 0);
             ctx.lineTo(105, 0);
             ctx.lineTo(110, 10);
             ctx.lineTo(50, 10);
             ctx.closePath();
             ctx.fill();
             ctx.stroke();

             // Door knob
             ctx.fillStyle = "gold";
             ctx.beginPath();
             ctx.arc(90, -30, 3, 0, Math.PI*2);
             ctx.fill();
             
             // --- Windows with 3D frames ---
             
             function drawWindow3D(wx, wy, ww, wh) {
                 // Glass
                 ctx.fillStyle = "#87ceeb";
                 ctx.fillRect(wx, wy, ww, wh);
                 ctx.strokeRect(wx, wy, ww, wh);
                 
                 // Bottom Sill (3D)
                 ctx.fillStyle = "white";
                 ctx.beginPath();
                 ctx.moveTo(wx - 5, wy + wh);
                 ctx.lineTo(wx + ww + 5, wy + wh);
                 ctx.lineTo(wx + ww + 5, wy + wh + 5);
                 ctx.lineTo(wx - 5, wy + wh + 5);
                 ctx.closePath();
                 ctx.fill();
                 ctx.stroke();
                 
                 // Cross bars
                 ctx.strokeStyle = "white";
                 ctx.lineWidth = 3;
                 ctx.beginPath();
                 ctx.moveTo(wx + ww/2, wy);
                 ctx.lineTo(wx + ww/2, wy + wh);
                 ctx.moveTo(wx, wy + wh/2);
                 ctx.lineTo(wx + ww, wy + wh/2);
                 ctx.stroke();
                 
                 // Reset stroke
                 ctx.strokeStyle = cOutline;
                 ctx.lineWidth = 2;
             }

             drawWindow3D(20, -90, 30, 40);
             drawWindow3D(100, -90, 30, 40);
             
             // Side Window (distorted for perspective)
             ctx.save();
             // Simple skew for side window
             ctx.fillStyle = "#6ca6c1"; // Darker glass
             ctx.beginPath();
             ctx.moveTo(wFront + 20, -80);
             ctx.lineTo(wFront + 40, -80 + (depthY * (20/depthX))); // Skewed Y
             ctx.lineTo(wFront + 40, -50 + (depthY * (20/depthX)));
             ctx.lineTo(wFront + 20, -50);
             ctx.closePath();
             ctx.fill();
             ctx.stroke();
             ctx.restore();

             // --- Chimney (3D) ---
             const cx = 110, cy = -160, cw = 20, ch = 40;
             // Side
             ctx.fillStyle = "#555";
             ctx.beginPath();
             ctx.moveTo(cx + cw, cy);
             ctx.lineTo(cx + cw + 10, cy - 5);
             ctx.lineTo(cx + cw + 10, cy + ch - 5);
             ctx.lineTo(cx + cw, cy + ch);
             ctx.closePath();
             ctx.fill();
             ctx.stroke();
             // Front
             ctx.fillStyle = "#7f8c8d";
             ctx.fillRect(cx, cy, cw, ch);
             ctx.strokeRect(cx, cy, cw, ch);
             // Top
             ctx.fillStyle = "#333";
             ctx.beginPath();
             ctx.moveTo(cx, cy);
             ctx.lineTo(cx + 10, cy - 5);
             ctx.lineTo(cx + cw + 10, cy - 5);
             ctx.lineTo(cx + cw, cy);
             ctx.closePath();
             ctx.fill();
             ctx.stroke();

             // Smoke
             ctx.fillStyle = "rgba(255,255,255,0.5)";
             const time = Date.now() / 1000;
             for(let i=0; i<5; i++) {
                 const offset = (time + i) % 4;
                 if (offset < 0.5) continue;
                 const sx = cx + 10 + offset * 10;
                 const sy = cy - 10 - offset * 25;
                 ctx.beginPath();
                 ctx.arc(sx, sy, 5 + offset*6, 0, Math.PI*2);
                 ctx.fill();
             }
             
             ctx.restore();
        }

        let flowers = [];
        let animals = [];
        let clouds = [];
        let grass = [];

        function initData() {
            flowers = [];
            animals = [];
            clouds = [];
            grass = [];
            
            const horizon = canvas.height / 2;
            const riverTop = horizon + 110;
            const riverBottom = horizon + 190;

            // Clouds
            for(let i=0; i<5; i++) {
                clouds.push({
                    x: random(0, canvas.width),
                    y: random(50, canvas.height/2 - 50),
                    s: random(0.5, 1.5)
                });
            }

            // Grass
            for(let i=0; i<1000; i++) {
                let y = random(horizon, canvas.height);
                // Don't grow grass in the river
                if (y > riverTop && y < riverBottom) continue;
                
                grass.push({
                    x: random(0, canvas.width),
                    y: y,
                    h: random(5, 20),
                    opacity: random(0.1, 0.3)
                });
            }

            // Flowers
            const count = 100;
            for(let i=0; i<count; i++) {
                let y = random(horizon + 50, canvas.height - 50);
                if (y > riverTop && y < riverBottom) continue;
                
                const x = random(50, canvas.width - 50);
                // Assign a consistent seed for this flower
                flowers.push({x, y, seed: Math.floor(random(0, 999999))});
            }
            flowers.sort((a, b) => a.y - b.y);

            // Birds
            const birdCount = 15;
            for(let i=0; i<birdCount; i++) {
                 const y = random(canvas.height/2 + 50, canvas.height - 20);
                 const x = random(50, canvas.width - 50);
                 const horizon = canvas.height/2;
                 const progress = (y - horizon) / (canvas.height - horizon);
                 const s = 0.5 + progress * 0.5;
                 const birdColors = ["#E91E63", "#2196F3", "#FFEB3B", "#00E676", "#9C27B0"];
                 const color = birdColors[Math.floor(random(0, birdColors.length))];
                 const lookingLeft = random(0, 1) > 0.5;
                 
                 animals.push({
                     type: 'bird', x, y, s, color, lookingLeft,
                     running: false,
                     speed: random(4, 9) * (lookingLeft ? -1 : 1)
                 });
            }

            // Rabbits
            const rabbitCount = 5;
            for(let i=0; i<rabbitCount; i++) {
                const y = random(canvas.height/2 + 50, canvas.height - 20);
                const x = random(50, canvas.width - 50);
                const horizon = canvas.height/2;
                const progress = (y - horizon) / (canvas.height - horizon);
                const s = 0.5 + progress * 0.5; 
                const lookingLeft = random(0, 1) > 0.5;
                
                animals.push({
                    type: 'rabbit', x, y, s, lookingLeft,
                    running: false,
                    speed: random(5, 10) * (lookingLeft ? -1 : 1)
                });
            }

            // Butterflies
            const butterflyCount = 20;
            for(let i=0; i<butterflyCount; i++) {
                const y = random(50, canvas.height - 100); 
                const x = random(50, canvas.width - 50);
                const s = random(0.5, 1.0);
                animals.push({
                    type: 'butterfly', x, y, s,
                    running: true, 
                    vx: random(-1, 1), vy: random(-0.5, 0.5)
                });
            }

            // Fish
            const fishCount = 10;
            for(let i=0; i<fishCount; i++) {
                const y = random(riverTop + 10, riverBottom - 10);
                const x = random(0, canvas.width);
                const s = random(0.6, 1.2);
                const lookingLeft = random(0, 1) > 0.5;
                animals.push({
                    type: 'fish', x, y, s, lookingLeft,
                    running: true,
                    speed: random(1, 3) * (lookingLeft ? -1 : 1),
                    baseY: y,
                    offset: random(0, Math.PI * 2)
                });
            }
        }

        function drawGarden() {
            // Re-render loop
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            drawSunrise();
            
            drawRiver();
            
            drawVilla();

            // Draw Clouds
            clouds.forEach(c => drawCloud(c.x, c.y, c.s));

            // Draw Grass
            grass.forEach(g => {
                ctx.beginPath();
                ctx.moveTo(g.x, g.y);
                const wind = Math.sin(Date.now() / 2000 + g.x * 0.01) * 6;
                ctx.lineTo(g.x + wind, g.y - g.h); 
                ctx.strokeStyle = `rgba(0, 100, 0, ${g.opacity})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            });

            // Draw Flowers
            flowers.forEach(f => drawFlower(f));

            // Update & Draw Animals
            animals.forEach(anim => {
                // Update Logic
                if (anim.running) {
                     if (anim.type === 'bird' || anim.type === 'rabbit') {
                         anim.x += anim.speed;
                         // Wrap around screen
                         if (anim.x > canvas.width + 50) anim.x = -50;
                         if (anim.x < -50) anim.x = canvas.width + 50;
                         
                         // Rabbit Hop
                         if (anim.type === 'rabbit') {
                             anim.y += Math.sin(Date.now() / 50) * 1.5;
                         }
                     } else if (anim.type === 'butterfly') {
                        anim.x += anim.vx + Math.sin(Date.now() / 300);
                        anim.y += anim.vy + Math.cos(Date.now() / 300);
                        if (anim.x > canvas.width) anim.x = 0;
                        if (anim.x < 0) anim.x = canvas.width;
                     } else if (anim.type === 'fish') {
                        anim.x += anim.speed;
                        anim.y = anim.baseY + Math.sin(Date.now() / 500 + anim.offset) * 5;
                        if (anim.x > canvas.width + 20) anim.x = -20;
                        if (anim.x < -20) anim.x = canvas.width + 20;
                     }
                }

                // Draw Logic
                if (anim.type === 'bird') drawBird(anim.x, anim.y, anim.s, anim.color, anim.lookingLeft);
                else if (anim.type === 'rabbit') drawRabbit(anim.x, anim.y, anim.s, anim.lookingLeft);
                else if (anim.type === 'butterfly') drawButterfly(anim.x, anim.y, anim.s);
                else if (anim.type === 'fish') drawFish(anim.x, anim.y, anim.s, anim.lookingLeft);
            });

            requestAnimationFrame(drawGarden);
        }

        // Click Handler
        canvas.addEventListener('mousedown', (e) => {
             const rect = canvas.getBoundingClientRect();
             const mx = e.clientX - rect.left;
             const my = e.clientY - rect.top;

             animals.forEach(anim => {
                 if (anim.type === 'butterfly') return;
                 
                 const dx = mx - anim.x;
                 const dy = my - anim.y;
                 const dist = Math.sqrt(dx*dx + dy*dy);
                 
                 // If clicked nearby an animal
                 if (dist < 50 * anim.s) {
                     anim.running = true;
                     anim.speed = 10 * (anim.lookingLeft ? -1 : 1);
                 }
             });
        });

        window.addEventListener('resize', () => {
             canvas.width = window.innerWidth;
             canvas.height = window.innerHeight;
             initData(); 
        });

        // Init
        initData();
        drawGarden();
    </script>
</body>
</html>
"""

filepath = os.path.abspath("beautiful_garden.html")

with open(filepath, "w") as f:
    f.write(html_content)

print(f"Created {filepath}")
print("Opening in browser...")
webbrowser.open(f"file://{filepath}")
