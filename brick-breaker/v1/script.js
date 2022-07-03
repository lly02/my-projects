import { Ball } from "./classes/Ball.js"
import { Platform } from "./classes/Platform.js"
import { Block } from "./classes/Block.js";
import { Brick } from "./classes/Brick.js";
import { Obstacle } from "./classes/obstacle.js";

const canvas = document.getElementById("game-board");
const bricks_canvas = document.getElementById("bricks");

const ctx = canvas.getContext("2d");
const bricks_ctx = bricks_canvas.getContext("2d");

const dpr = window.devicePixelRatio;

let window_height = window.innerHeight;
let window_width = window.innerWidth;

let height = window_width/2;
let width = window_height/2;

// Set the canvas box
canvas.height = width * dpr;
canvas.width = width * dpr;
bricks_canvas.height = width * dpr;
bricks_canvas.width = width * dpr;

ctx.scale(dpr, dpr);
bricks_ctx.scale(dpr, dpr);

// Platform setup
let platform = new Platform(50, 5, [(canvas.width/2) - (50/2), canvas.height - 10], 10);

// Ball setup
let ball = new Ball(7, [canvas.width/2, canvas.height/1.5], 100);

// Blocks setup
let block = new Block(canvas.width/20, canvas.width/20, 20, 9);
let bricks = [];

let lastTimeDrawn = 0;
let stopID;

for(let i = 0; i < block.getMaxRow(); i++){
    for(let k = 0; k < block.getMaxCol(); k++){
        bricks.push(new Brick(block, k, i));
    };
};
console.log(bricks.length)

render();
bricksRender();

function gameLoop(currentTime){
    stopID = window.requestAnimationFrame(gameLoop);

    let deltaTime = currentTime - lastTimeDrawn;
    lastTimeDrawn = currentTime;

    ball.setNextPos(deltaTime);
    collisionDetection();
    let brick = bricks[0];

    for(const index in bricks){
        let brick = bricks[index];
        
        if(ball.getPos()[1] - ball.getRadius() >= brick.getHeight() * (brick.getRow()) && 
        ball.getPos()[1] - ball.getRadius() <= brick.getHeight() * (brick.getRow()) + brick.getHeight() &&
        ball.getPos()[0] >= brick.getLength() * (brick.getCol()) &&
        ball.getPos()[0] <= brick.getLength() * (brick.getCol()) + brick.getLength()){
            bricks.splice(index, 1);
            brickCollisionDetection("bottom");
            bricksRender();
            return;
        };
    };  

    render();
};

stopID = window.requestAnimationFrame(gameLoop);

function render(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw platform
    ctx.beginPath();

    ctx.fillStyle = "#F4C2C2";
    ctx.rect(platform.getPos()[0], platform.getPos()[1], platform.getLength(), platform.getHeight());
    ctx.fill();
    ctx.stroke();

    
    // Draw ball
    ctx.beginPath();

    ctx.fillStyle = "#F2B8C6";
    ctx.arc(ball.getPos()[0], ball.getPos()[1], ball.getRadius(), 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();

};

function bricksRender(){
    bricks_ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw brick
    for(const prop in bricks){
        bricks_ctx.beginPath();
        bricks_ctx.fillStyle = "#FCBACB";
        
        let brick = bricks[prop];
        bricks_ctx.rect(brick.getLength() * brick.getCol(), brick.getHeight() * brick.getRow(), brick.getLength(), brick.getHeight());

        bricks_ctx.fill();
        bricks_ctx.stroke();
    };
};

function collisionDetection(){
    // Check if ball touches platform
    if(ball.getPos()[1] + ball.getRadius() >= platform.getPos()[1] && ball.getPos()[1] + ball.getRadius() <= platform.getPos()[1] + platform.getHeight() && ball.getPos()[0] >= platform.getPos()[0] && ball.getPos()[0] <= platform.getPos()[0] + platform.getLength()){
        ball.setDirection(2 * Math.PI - ball.getDirection());
    }; 

    // Check bottom of ball touches edge
    if(ball.getPos()[1] + ball.getRadius() >= canvas.height) {
        window.cancelAnimationFrame(stopID);
    };

    // Check top of ball touches edge
    if(ball.getPos()[1] - ball.getRadius() <= 0) {
        ball.setDirection(2 * Math.PI - ball.getDirection());
    };

    // Check right of ball touches edge
    if(ball.getPos()[0] + ball.getRadius() >= canvas.width) {
        ball.setDirection(Math.PI - ball.getDirection());
    };

    // Check left of ball touches edge
    if(ball.getPos()[0] - ball.getRadius() <= 0) {
        ball.setDirection(Math.PI - ball.getDirection());
    };
};

function brickCollisionDetection(direction){
    // Check bottom of ball touches brick
    if(direction == "bottom") {
        ball.setDirection(2 * Math.PI - ball.getDirection());
    };

    // Check top of ball touches brick
    if(direction == "top") {
        ball.setDirection(2 * Math.PI - ball.getDirection());
    };

    // Check right of ball touches brick
    if(direction == "right") {
        ball.setDirection(Math.PI - ball.getDirection());
    };

    // Check left of ball touches brick
    if(direction == "left") {
        ball.setDirection(Math.PI - ball.getDirection());
    };
};

document.addEventListener("keydown", (key)=>{
    // Control the platform
    if(key.key == "a") {
        if(platform.getPos()[0] >= 0){
            platform.setPos([platform.getPos()[0] - platform.getSpeed(), platform.getPos()[1]]);
        };
    };

    if(key.key == "d") {
        if(platform.getPos()[0] <= canvas.width - platform.getLength()){
            platform.setPos([platform.getPos()[0] + platform.getSpeed(), platform.getPos()[1]]);
        };
    };

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    render();
});