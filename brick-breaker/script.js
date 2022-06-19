const canvas = document.getElementById("game-board");
const ctx = canvas.getContext("2d");
const dpr = window.devicePixelRatio;

let window_height = window.innerHeight;
let window_width = window.innerWidth;

let height = window_width/2;
let width = window_height/2;

// Set the canvas box
canvas.height = width * dpr;
canvas.width = width * dpr;

ctx.scale(dpr, dpr)

let platform_pos = [(canvas.width/2) - 25, canvas.height - 10]

render();

setInterval(()=>{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    render();
}, 1000);

function render(){
    ctx.fillRect(platform_pos[0], platform_pos[1], 50, 3);
    console.log(platform_pos)
};

document.addEventListener("keypress", (key)=>{
    if(key.key == "a") platform_pos[0] -= 5;
    if(key.key == "d") platform_pos[0] += 5;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    render();
});